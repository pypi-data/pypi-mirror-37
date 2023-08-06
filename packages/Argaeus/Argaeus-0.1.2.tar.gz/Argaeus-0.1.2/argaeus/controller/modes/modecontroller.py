import datetime
from argaeus.controller.modes.modefactory import ModeFactory
from argaeus.controller.modes.modeschedule import ModeSchedule
from argaeus.controller.acontroller import AController


class ModeController(AController):
    """
    The core controller for the gui - it provides the current mode, program, and schedule:
      * current mode - either a program or a schedule. can be changed via GUI interaction
      * current program - if current mode is a program, then current program equals current mode. otherwise, the program
      that is currently active in the schedule defined by current mode is used as current program
      * current schedule - if current mode is of type ModeSchedule, current schedule is the raw schedule from current
      mode. 'None' oterwise.

    It registers to three topics:
      * prev - select the previous entry in the list of selectable modes as current mode
      * next - select the next entry in the list of selectable modes as current mode
      * default - select the default mode from config as current mode

    After each update, the current schedule chart (or None if no schedule is active) is published.

    config yaml entries:
        default-mode: Schedule  # default mode - must be a name from modes list
        topics-sub:  # incoming topics
            to-prev: /test/r2/rotate  # select previous mode
            command-prev: LEFT  # to previous command - if this value is published to to-prev, the previous entry in the mode list is selected
            to-next: /test/r2/rotate  # select next mode
            command-next: RIGHT  # to next command - if this value is published to to-next, the next entry in the mode list is selected
            to-default: /test/r1/button/pressed  # incoming event to reset to default mode (optional together with command-default)
            command-default: PRESSED  # command for topic-sub / reset to default mode (optional together with to-default)
        topics-pub:  # outgoing topics
            display-server-schedule-image: /test/display/schedule  # topic of an nikippe-mqttimage instance
            display-server-mode-icon: /test/display/mode  # topic of an nikippe-imagelist instance
            temperature-set-point: /test/temperature/set-point  # topic of e.g. epidaurus (=pid temperature control) set-point listener
        modes:  # list of modes
            - name: Night  # unique name for mode entry
              type: program  # program or schedule - a schedule consists of programms
              selectable: True  # can be selected using the gui
              set-point: 19.5  # target temperature of this mode

            - name: Day  # unique name for mode entry
              type: program  # program or schedule - a schedule consists of programms
              selectable: True  # can be selected using the gui
              set-point: 23.0  # target temperature of this mode

            - ...
    """

    _modes = None  # dict of modes with mode.name as key - result from ModeFactory
    _selectable_modes = None  # list of modes that can be selected via GUI
    _selectable_pos = None  # position of currently selected mode
    _default_mode = None  # default mode as specified in the config yaml

    _topic_sub_prev = None  # select previous mode
    _command_prev = None  # command expected on _topic_sub_prev
    _topic_sub_next = None  # select next mode
    _command_next = None  # command expected on _topic_sub_next
    _topic_sub_to_default = None  # reset to default mode - can be None
    _command_default = None  # command expected on _topic_sub_to_default - can be None

    _topic_pub_schedule_image = None  # publish current schedule chart to this topic

    current_mode = None  # current mode (program or schedule)
    current_program = None  # current program (either =current_mode or the current entry in schedule)
    current_schedule = None  # current schedule (either =current schedule or None)

    def __init__(self, config, mqtt_client, logger):
        """
        Constructor

        :param config: config yaml structure
        :param mqtt_client: mymqttclient instance
        :param logger: logger instance - a child instance will be spawned with name=__name__
        """
        AController.__init__(self, config, mqtt_client, logger, logger_name=__name__)

        self._modes, self._selectable_modes = ModeFactory.create_modes(self._config["modes"],
                                                                       self._config["topics-pub"], mqtt_client, logger)

        self._default_mode = self._modes[self._config["default-mode"]]
        self._activate_default_mode()

        self._topic_sub_prev = self._config["topics-sub"]["to-prev"]
        self._command_prev = self._config["topics-sub"]["command-prev"]
        self._topic_sub_next = self._config["topics-sub"]["to-next"]
        self._command_next = self._config["topics-sub"]["command-next"]
        self._topic_pub_schedule_image = self._config["topics-pub"]["display-server-schedule-image"]

        try:
            self._topic_sub_to_default = self._config["topics-sub"]["to-default"]
        except KeyError:
            pass

        if self._topic_sub_to_default is not None:
            try:
                self._command_default = self._config["topics-sub"]["command-default"]
            except KeyError:
                self._logger.error("OperationController.__init__ - 'to-default' is set but 'command-default' "
                                   "is missing.")
                raise KeyError("OperationController.__init__ - 'to-default' is set but 'command-default' "
                               "is missing.")

        self._logger.info("ModeController.__init__ - done")

    def _activate_default_mode(self):
        """
        Set current mode/program/schedule to the default mode specified in config
        """

        self._logger.info("ModeController._activate_default_mode")
        self._selectable_pos = self._selectable_modes.index(self._default_mode)
        self.current_mode = self._default_mode

        if isinstance(self.current_mode, ModeSchedule):
            dt = datetime.datetime.time(datetime.datetime.now())
            self.current_program = self.current_mode.get_program_at_time(dt)
            self.current_schedule = self.current_mode.schedule_raw
        else:
            self.current_program = self.current_mode
            self.current_schedule = None

    def _to_default_handler(self, value):
        """
        Check if the incoming message on _topic_sub_to_default is equivalent to _topic_sub_to_default. Activate
        default mode if yes.

        :param value: mqtt message
        """
        if len(value) > 0 and value.decode("UTF-8") == self._command_default:
            self._logger.info("ModeController._to_default_handler - activate default mode")
            self._activate_default_mode()
            self.update()
        else:
            self._logger.warning("ModeController._to_default_handler - dont know how to handle "
                                 "message '{}'".format(value))

    def _topic_handler_prev(self, value):
        """
        Check if the incoming message on _topic_sub_prev is equivalent to _command_prev. Adapt selectable pos
        accordingly and call post topic handler.

        :param value: mqtt message
        """

        if value.decode("utf-8") == self._command_prev:
            self._logger.info("ModeController._topic_handler - command prev.")
            self._selectable_pos = self._selectable_pos - 1
            self._post_topic_handler()

    def _topic_handler_next(self, value):
        """
        Check if the incoming message on _topic_sub_next is equivalent to _command_next. Adapt selectable pos
        accordingly and call post topic handler.

        :param value: mqtt message
        """

        if value.decode("utf-8") == self._command_next:
            self._logger.info("ModeController._topic_handler - command next.")
            self._selectable_pos = self._selectable_pos + 1
            self._post_topic_handler()

    def _post_topic_handler(self):
        """
        Make sure that the selectable pos has a valid value and call update
        """
        self._selectable_pos = self._selectable_pos % len(self._selectable_modes)
        self.current_mode = self._selectable_modes[self._selectable_pos]
        self._logger.info("ModeController._topic_handler - selected mode '{}' at pos '{}'.".
                          format(self.current_mode.name, self._selectable_pos))
        self.update()

    def update(self):
        """
        fill current program and current schedule according to current mode and publish the program and the mode.
        if mode is not ModeSchedule publish an empty message to _topic_pub_schedule_image.
        """

        self._logger.info("ModeController.update")
        if isinstance(self.current_mode, ModeSchedule):
            dt = datetime.datetime.now().time()
            self.current_program = self.current_mode.get_program_at_time(dt)
            self.current_schedule = self.current_mode.schedule_raw
            self.current_program.publish()
            self.current_mode.publish()
        else:
            self.current_program = self.current_mode
            self.current_schedule = None
            self.current_program.publish()
            # no schedule active - publish empty message instead
            self._mqtt_client.publish(self._topic_pub_schedule_image, "")

    def start(self):
        """
        Subscribe to prev, next, and default
        """
        self._logger.info("ModeController.start - starting")
        self._mqtt_client.subscribe(self._topic_sub_prev, self._topic_handler_prev)
        self._mqtt_client.subscribe(self._topic_sub_next, self._topic_handler_next)
        if self._topic_sub_to_default is not None:
            self._mqtt_client.subscribe(self._topic_sub_to_default, self._to_default_handler)
        self.update()
        self._logger.info("ModeController.start - started")

    def stop(self):
        """
        Unsubscribe from prev, next, and default
        """
        self._logger.info("ModeController.start - stopping")
        self._mqtt_client.unsubscribe(self._topic_sub_prev, self._topic_handler_prev)
        self._mqtt_client.unsubscribe(self._topic_sub_next, self._topic_handler_next)
        if self._topic_sub_to_default is not None:
            self._mqtt_client.unsubscribe(self._topic_sub_to_default, self._to_default_handler)
        self._logger.info("ModeController.start - stopped")

