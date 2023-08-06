from argaeus.controller.modes.modeprogram import ModeProgram
from argaeus.controller.modes.modeschedule import ModeSchedule
from pelops.mylogger import get_child


class ModeFactory:
    """
    Generation of mode instances
    """

    @staticmethod
    def create_mode(config, config_topics_pub, mqtt_client, logger):
        """
        Create a single mode instance

        :param config: config yaml structure
        :param config_topics_pub: a dict with all topics that can be published to
        :param mqtt_client: mqtt_client instance
        :param logger: logger instance
        :return: the corresponding mode instance
        """
        log = get_child(logger, __name__)
        log.info("ModeFactory.create_mode - creating mode ('{}').".format(config))

        t = config["type"].lower()
        if t == "program":
            mode = ModeProgram(config, config_topics_pub, mqtt_client, logger)
        elif t == "schedule":
            mode = ModeSchedule(config, config_topics_pub, mqtt_client, logger)
        else:
            log.error("ModeFactory.create_mode - unknown type '{}'.".format(t))
            raise ValueError("ModeFactory.create_mode - unknown type '{}'.".format(t))

        return mode

    @staticmethod
    def create_modes(config, config_topics_pub, mqtt_client, logger):
        """
        Takes a list of mode config entries and returns a list of mode instances. Schedules are already properly
        initialized (cp. two step initialization of ModeSchedule.

        :param config: config yaml structure
        :param config_topics_pub:  a dict with all topics that can be published to
        :param mqtt_client: mymqttclient instance
        :param logger: logger instance
        :return: modes (dict with all generated instances - keys are mode.name), modes_selectable (a list with all all
        generated instances that can be selected via gui)
        """

        log = get_child(logger, __name__)
        log.info("ModeFactory.create_modes - creating modes ('{}').".format(config))

        modes = {}
        modes_selectable = []
        for c in config:
            mode = ModeFactory.create_mode(c, config_topics_pub, mqtt_client, logger)
            modes[mode.name] = mode
            if mode.selectable:
                modes_selectable.append(mode)
        log.info("ModeFactory.create_modes - map_schedule_modes")
        for mode in modes.values():
            if isinstance(mode, ModeSchedule):
                mode.map_schedule_modes(modes)

        return modes, modes_selectable
