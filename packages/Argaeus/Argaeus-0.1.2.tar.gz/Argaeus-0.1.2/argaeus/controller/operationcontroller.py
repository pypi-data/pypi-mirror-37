from argaeus.controller.acontroller import AController


class OperationController(AController):
    """
    This controller is responsible whether the Themostat is operating in observation or in control mode. Thus, if the
    output of the DAC is connected to the heating system or not.

    It registers to this topic:
      * toggle - toggles the output between True and False

    Each change is published to the copreus controlled relay with the corresponding commands active and passive.

    Config yaml entries:
        default-is-active: True  # Is the controller active or passive initially
        topic-pub: /test/relais/closed  # Topic that controls the output behavior relais of the thermostat.
        command-active: ON  # set to active command - publish this value to topic-pub, to set the controller to
        active operation.
        command-passive: OFF  # set to passive command - publish this value to topic-pub, to set the controller to
        passive operation.
        topic-sub-toggle: /test/r1/button/pressed  # incoming event to toggle active/passive operation (optional
        together with command-toggle)
        command-toggle: PRESSED  # command for topic-sub-toggle / toggle active/passive operation (optional together
        with topic-sub-toggle)
    """
    _default_is_active = None  # default state as defined in the config
    active_operation = None  # current state
    
    _topic_pub = None  # publish state for relay to this topic
    _command_active = None  # activate DAC output
    _command_passive = None  # deactivate DAC output

    _topic_sub_toggle = None  # subscribe for incoming toggle trigger events
    _command_sub_toggle = None  # command expected to initiate trigger

    def __init__(self, config, mqtt_client, logger):
        """
        Constructor

        :param config: config yaml structure
        :param mqtt_client: mymqttclient instance
        :param logger: logger instance - a child instance will be spawned with name=__name__
        """

        AController.__init__(self, config, mqtt_client, logger, logger_name=__name__)

        self._default_is_active = bool(self._config["default-is-active"])
        self.active_operation = self._default_is_active

        self._topic_pub = self._config["topic-pub"]
        self._command_active = self._config["command-active"]
        self._command_passive = self._config["command-passive"]

        try:
            self._topic_sub_toggle = self._config["topic-sub-toggle"]
        except KeyError:
            pass

        if self._topic_sub_toggle is not None:
            try:
                self._command_sub_toggle = self._config["command-toggle"]
            except KeyError:
                self._logger.error("OperationController.__init__ - 'topic-sub-toggle' is set but 'command-toggle' is "
                                   "missing.")
                raise KeyError("OperationController.__init__ - 'topic-sub-toggle' is set but 'command-toggle' "
                               "is missing.")

        self._logger.info("OperationController.__init__ - done")

    def _toggle_operation_handler(self, value):
        """
        Check if the incoming message on _topic_sub_toggle is equivalent to _command_sub_toggle. Toggle
        operation if yes.

        :param value: mqtt message
        """

        if len(value) > 0 and value.decode("UTF-8") == self._command_sub_toggle:
            self._toggle_operation()
        else:
            self._logger.warning("OperationController._toggle_operation_handler - dont know how to handle "
                                 "message '{}'".format(value))

    def _toggle_operation(self):
        """Change operation state to not previous state and initialize publish."""
        self.active_operation = not self.active_operation
        self._logger.info("OperationController._toggle_operation - toggle active/passive (now: '{}').".
                          format(self.active_operation))
        self._publish()

    def _publish(self):
        """
        publish current operation state (command_active or command_passive) to _topic_pub
        """
        if self.active_operation:
            self._mqtt_client.publish(self._topic_pub, self._command_active)
        else:
            self._mqtt_client.publish(self._topic_pub, self._command_passive)

    def start(self):
        """
        Subscribe topic_sub_toggle and publish initial state.
        """
        if self._topic_sub_toggle is not None:
            self._mqtt_client.subscribe(self._topic_sub_toggle, self._toggle_operation_handler)
        self._publish()

    def stop(self):
        """unsubcribe _topic_sub_toggle."""
        if self._topic_sub_toggle is not None:
            self._mqtt_client.unsubscribe(self._topic_sub_toggle, self._toggle_operation_handler)
