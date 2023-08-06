import collections
import datetime
from argaeus.controller.modes.amode import AMode
from argaeus.controller.modes.schedule_image import ScheduleImage
from io import BytesIO


class ModeSchedule(AMode):
    """
    A mode schedule provides for each time during a day the defined mode program. A day is divided into 15 minute
    slots. To each slot one of the mode programs is assigned. A schedule entry must not be another schedule. A
    schedule chart (see ScheduleImage) is generated that is published to a nikippe.mqttimage microservice for display
    purposes.

    Note: to create an instance of ModeSchedule, a two step initialisation is necessary: first call to constructor and
    as soon as all mode instances have been created, the method map_schedule_modes must be called. Calling
    get_program_at_time or publish before map_schedule_modes results in runtime errors.

    additional yaml config entries:
        image:
            ... # see schedule_image.py
        schedule:  # 24x4 entries that map the timeslot to a mode program
            "00:00": Night
            "00:15": Night
            "00:30": Night
            "00:45": Night
            ...
            "07:00": Morning
            "07:15": Morning
            "07:30": Morning
            "07:45": Morning
            ...
            "13:00": Day
            "13:15": Day
            "13:30": Day
            "13:45": Day
            ...
            "23:00": Night
            "23:15": Night
            "23:30": Night
            "23:45": Night
    """

    schedule_raw = None  # ordered dict with datetime.time as key and the string from the config as value
    schedule = None  # ordered dict with datetime.time as key and reference to the corresponding mode program as value
    img = None  # img containing the graphical representation of the schedule (see ScheduleImage)
    _mqtt_message = None  # img converted to bytes for mqtt transport
    _topic_pub = None  # publish schedule image to this topic
    _modes_mapped = None  # boolean - set to true as soon as the two step init phase has been finished

    def __init__(self, config, config_topics_pub, mqtt_client, logger):
        """
        Constructor

        :param config: config yaml structure
        :param config_topics_pub: a dict with all topics that can be published to
        :param mqtt_client: mqtt_client instance
        :param logger: logger instance
        """
        AMode.__init__(self, config, mqtt_client, logger)
        self.schedule_raw = ModeSchedule._sort_dict(self._config["schedule"])
        self.schedule = collections.OrderedDict()
        self._topic_pub = config_topics_pub["display-server-schedule-image"]
        self._modes_mapped = False

    @staticmethod
    def _sort_dict(d):
        """
        Takes a dict with "HH:MM" string as keys and any type as values and returns a time sorted ordered dict with
        datetime.time as keys.

        :param d: dict with "HH:MM" string keys and any value type
        :return: ordered dict with datetime.time as keys and any value type. ordered by time ascending.
        """
        result = collections.OrderedDict()
        for h in range (0, 24):
            for m in range(0, 60):
                key = "{:02}:{:02}".format(h, m)
                dt = datetime.time(hour=h, minute=m)
                try:
                    result[dt] = d[key]
                except KeyError:
                    pass
        return result

    def map_schedule_modes(self, modes):
        """
        Takes the raw schedule from the config, generates the final config with mode entry references as values and
        creates the schedule chart. Updates schedule, img and _modes_mapped.

        :param modes: dict with mode.name as key and mode instance as value
        """
        self._logger.info("ModeSchedule.map_schedule_modes - mapping schedule '{}' to mode '{}'.".
                          format(self.schedule_raw, modes))
        for k,v in self.schedule_raw.items():
            program = modes[v]
            if isinstance(program, ModeSchedule):
                self._logger.error("ModeSchedule.map_schedule_modes -  mode must not be of type ModeSchedule ('{}').".
                                   format(type(program)))
                raise ValueError("ModeSchedule.map_schedule_modes -  mode must not be of type ModeSchedule ('{}').".
                                 format(type(program)))
            self.schedule[k] = program

        self._logger.info("ModeSchedule.map_schedule_modes - generate schedule image")
        renderer = ScheduleImage(self.schedule, self._config["image"], self._logger)
        self.img = renderer.img
        bytes_image = BytesIO()
        self.img.save(bytes_image, format="png")
        self._mqtt_message = bytes_image.getvalue()

        self._modes_mapped = True

    def get_program_at_time(self, time):  #
        """
        Get the corresponding mode for any time during a day. Will return the same value for the same time on two
        different days.

        :param time: request time as datetime.time instance
        :return: mode instance from schedule
        """
        if not self._modes_mapped:
            self._logger.error("ModeSchedule.get_program_at_time - prior to calling this method, the method "
                               "'map_schedule_modes' must be called.")
            raise RuntimeError("ModeSchedule.get_program_at_time - prior to calling this method, the method "
                               "'map_schedule_modes' must be called.")

        result = None
        for dt, program in self.schedule.items():
            if dt > time:
                break
            result = program
        self._logger.info("ModeSchedule.get_program_at_time - program '{}' at time '{}'.".format(result.name, time))
        return result

    def publish(self):
        """
        Send the schedule image to a nikippe.mqttimage microservice.
        """
        self._logger.info("ModeSchedule.publish - sending schedule image")

        if not self._modes_mapped:
            self._logger.error("ModeSchedule.publish - prior to calling this method, the method "
                               "'map_schedule_modes' must be called.")
            raise RuntimeError("ModeSchedule.publish - prior to calling this method, the method "
                               "'map_schedule_modes' must be called.")

        self._logger.debug("ModeSchedule.publish - mqtt_message: {}".format(self._mqtt_message))
        self._mqtt_client.publish(self._topic_pub, self._mqtt_message)
