from pelops.mylogger import get_child


class AMode:
    """
    Abstract mode - a mode defines the current behavior of the thermostat.

    yaml config:
        name: Name  # name for this mode
        selectable: True  # True/False - if set to False it cannot be selected via GUI
        type: program  # ["program", "schedule"] - needed for mode factory.
    """

    _config = None  # config yaml structure
    _logger = None  # logger instance
    _mqtt_client = None  # mqtt_client instance

    name = None  # name of this mode
    selectable = None  # can this mode be activated via GUI

    def __init__(self, config, mqtt_client, logger):
        """
        Constructor

        :param config: config yaml structure
        :param mqtt_client: mqtt_client instance
        :param logger: logger instance - a child will be spawned with the name defined in the config
        """

        self._config = config
        self._mqtt_client = mqtt_client
        self.name = self._config["name"]
        self._logger = get_child(logger, self.name)

        self._logger.info("{}.__init__ - initializing".format(self.name))
        self._logger.debug("{}.__init__ - config: '{}'.".format(self.name, self._config))

        self.selectable = bool(self._config["selectable"])

    def publish(self):
        """
        Publish your current state. abstract method.
        """
        raise NotImplementedError
