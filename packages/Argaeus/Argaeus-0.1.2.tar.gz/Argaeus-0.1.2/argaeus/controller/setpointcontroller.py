from argaeus.controller.acontroller import AController


class SetPointController(AController):
    """
    The current set-point temperature can be changed with this controller. It subscribes to incoming events and increases
    /decreases the set-point of current_program from the mode_controller and initiates that the new value is published
    by the mode program itself. Optionally a button can be used to reset the current set-point to the default value
    specified in the config yaml.

    It registers to this topic:
      * down - reduces the set-point value
      * up - increases the set-point value
      * reset - reset to default value

    Each change is published to the pid controller.

    Config yaml entries:
        topic-sub-down: /test/r1/rotate  # reduce temperature topic
        command-down: LEFT  # down command - if this value is published to topic-sub-down, temp is reduced.
        topic-sub-up: /test/r1/rotate  # increase temperature topic
        command-up: RIGHT  # up command - if this value is published to topic-sub-up, temp is increased.
        topic-sub-reset: /test/r1/button/pressed  # incoming event to reset temperature to default (optional together with command-reset)
        command-reset: PRESSED  # command for topic-sub-reset / reset to default (optional together with topic-sub-reset)
        step-size: 0.5  # Temperature is changed by step size for each rotation step.
        max-temp: 30.0  # Maximum value for temperature
        min-temp: 10.0  # Minimum value for temperature
    """

    _step_size = None  # change of set_point per event
    _min_temp = None  # minimum value for set point
    _max_temp = None  # maximum value for set point

    _topic_sub_down = None  # topic for down event
    _command_down = None  # command for down event
    _topic_sub_up = None  # topic for up event
    _command_up = None  # command for up event

    _topic_sub_reset = None  # topic for reset to default event
    _command_reset = None  # command for reset to default event

    _mode_controller = None  # reference to mode controller - needed to get current mode

    def __init__(self, mode_controller, config, mqtt_client, logger):
        """
        Constructor

        :param mode_controller: reference to mode controller - needed to get current mode
        :param config: config yaml structure
        :param mqtt_client: mymqttclient instance
        :param logger: logger instance - a child will be spawned with name=__name__
        """
        AController.__init__(self, config, mqtt_client, logger, logger_name=__name__)

        self._step_size = float(self._config["step-size"])
        self._min_temp = float(self._config["min-temp"])
        self._max_temp = float(self._config["max-temp"])

        self._topic_sub_down = self._config["topic-sub-down"]
        self._command_down = self._config["command-down"]
        self._topic_sub_up = self._config["topic-sub-up"]
        self._command_up = self._config["command-up"]

        try:
            self._topic_sub_reset = self._config["topic-sub-reset"]
        except KeyError:
            pass

        if self._topic_sub_reset is not None:
            try:
                self._command_reset = self._config["command-reset"]
            except KeyError:
                self._logger.error("OperationController.__init__ - 'topic-sub-reset' is set but 'command-reset' "
                                   "is missing.")
                raise KeyError("OperationController.__init__ - 'topic-sub-reset' is set but 'command-reset' is "
                               "missing.")

        self._mode_controller = mode_controller

        self._logger.info("SetPointController.__init__ - done")

    def _reset_temp_handler(self, value):
        """
        Check if the incoming message on _topic_sub_reset is equivalent to _topic_sub_reset. reset to default
        value if yes.

        :param value: mqtt message
        """
        if len(value) > 0 and value.decode("UTF-8") == self._command_reset:
            self._logger.info("SetPointController._reset_temp_handler - reset to default set point.")
            self._post_topic_handler(self._mode_controller.current_program.default_set_point)
        else:
            self._logger.warning("SetPointController._reset_temp_handler - dont know how to handle "
                                 "message '{}'".format(value))

    def _topic_handler_down(self, value):
        """
        if message is equal to command_down - reduce set point and call post processor
        :param value: mqtt message
        """
        if value.decode("utf-8") == self._command_down:
            self._logger.info("SetPointController._topic_handler - command left.")
            set_point = self._mode_controller.current_program.set_point - self._step_size
            self._post_topic_handler(set_point)

    def _topic_handler_up(self, value):
        """
        if message is equal to command_up - increase set point and call post processor
        :param value: mqtt message
        """
        if value.decode("utf-8") == self._command_up:
            self._logger.info("SetPointController._topic_handler - command right.")
            set_point = self._mode_controller.current_program.set_point + self._step_size
            self._post_topic_handler(set_point)

    def _post_topic_handler(self, set_to):
        """
        validate new set point and initialize publishing of the new value
        :param set_to:
        :return:
        """
        set_point = min(self._max_temp, max(self._min_temp, set_to))
        self._logger.info("SetPointController._topic_handler - set temp to '{}'.".
                          format(self._mode_controller.current_mode.name))
        self._mode_controller.current_program.set_point = set_point
        self._mode_controller.current_program.publish()

    def start(self):
        """start by subscribing to down, up, reset"""
        self._mqtt_client.subscribe(self._topic_sub_down, self._topic_handler_down)
        self._mqtt_client.subscribe(self._topic_sub_up, self._topic_handler_up)
        if self._topic_sub_reset is not None:
            self._mqtt_client.subscribe(self._topic_sub_reset, self._reset_temp_handler)

    def stop(self):
        """stop by unsubscribing from down, up, reset"""
        self._mqtt_client.unsubscribe(self._topic_sub_down, self._topic_handler_down)
        self._mqtt_client.unsubscribe(self._topic_sub_up, self._topic_handler_up)
        if self._topic_sub_reset is not None:
            self._mqtt_client.unsubscribe(self._topic_sub_reset, self._reset_temp_handler)
