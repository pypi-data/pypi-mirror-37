from pelops.mylogger import get_child


class AController:
    """
    Abstract controller - provides the minimum functionality a controller must implement
    """

    _config = None  # config yaml structure
    _mqtt_client = None  # mqtt_client instance
    _logger = None  # logger instance

    def __init__(self, config, mqtt_client, logger, logger_name=__name__):
        """
        Constructor

        :param config: yaml structure
        :param mqtt_client: mqtt_client instance
        :param logger: logger instance - a child logger will be spawned
        :param logger_name: name for child logger
        """
        self._mqtt_client = mqtt_client
        self._config = config
        self._logger = get_child(logger, logger_name)

    def start(self):
        """Start operation - abstract method"""
        raise NotImplementedError

    def stop(self):
        """Stop operation - abstract method"""
        raise NotImplementedError
