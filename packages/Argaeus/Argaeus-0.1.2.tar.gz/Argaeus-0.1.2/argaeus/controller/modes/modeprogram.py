from argaeus.controller.modes.amode import AMode


class ModeProgram(AMode):
    """
    A mode program sets the current temperature. It can either be selected via GUI or activated via a mode schedule.

    addtitional yaml config entry:
          set-point: 19.5  # target temperature of this mode
    """

    set_point = None  # current set_point for temperature
    default_set_point = None  # default set_point for temperature (=value taken from config)
    _topic_pub_set_point = None  # publish topic for set_point
    _topic_pub_mode_icon = None  # publish topic for mode_icon

    def __init__(self, config, config_topics_pub, mqtt_client, logger):
        """
        Constructor

        :param config: config yaml structure
        :param config_topics_pub: a dict with all topics that can be published to
        :param mqtt_client: mqtt_client instance
        :param logger: logger instance
        """

        AMode.__init__(self, config, mqtt_client, logger)
        self.set_point = float(self._config["set-point"])
        self.default_set_point = self.set_point
        self._topic_pub_set_point = config_topics_pub["temperature-set-point"]
        self._topic_pub_mode_icon = config_topics_pub["display-server-mode-icon"]

    def publish(self):
        """Publish set_point and name as mode_icon."""
        self._mqtt_client.publish(self._topic_pub_set_point, self.set_point)
        self._mqtt_client.publish(self._topic_pub_mode_icon, self.name.lower())

