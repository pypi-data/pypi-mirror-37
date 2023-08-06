from pelops.mylogger import get_child
from PIL import Image
from PIL import ImageDraw


class ScheduleImage:
    """
    Generates a chart, that shows which mode is active at which time slot. It takes a list of 96 mode entries and a
    list of pattern mappings. For each mode entry, a pattern mapping must exist. The resulting image is stored in
    the property img.

    Four patterns exist:
        0 - nothing
        1 - lower dot
        2 - upper and lower dot
        3 - upper dot

    config yaml entries:
        width: 192  # width of image
        height: 2  # height of image
        foreground-color: 255  # from 0 to 255.
        background-color: 0  # from 0 to 255.
        patterns:  # 0, 1, 2, 3 are valid patterns; a pattern can be assigned more than once
            Night: 0    # nothing
            Morning: 1  # lower dot
            Day: 2      # upper and lower dot
            Frost: 3    # upper dot

    """

    _config = None  # yaml config structure
    _logger = None  # logger instance

    img = None  # image

    _width = None  # width of image
    _height = None  # height of image
    _foreground_color = None  # from 0 to 255
    _background_color = None  # from 0 to 255
    _group_by = None  # in minutes - defines the length of one time slot. currently fixed to 15.

    _pixel_per_slot = None  # x-axis
    _pixel_per_dot = None  # y-axis

    _pattern_schedule = None  # list with 96 entries where the modes have been replaced by their corresponding pattern

    def __init__(self, schedule_items, config, logger):
        """
        Constructor

        :param schedule_items: list of 96 mode entries
        :param config: config yaml structure
        :param logger: logger instance - a child with __name__ will be spawned
        """

        self._config = config
        self._logger = get_child(logger, __name__)

        self._logger.info("ScheduleImage - initializing")
        self._logger.debug("ScheduleImage - config: {}".format(self._config))
        self._logger.debug("ScheduleImage - schedule_items: {}".format(schedule_items))

        self._width = int(self._config["width"])
        self._height = int(self._config["height"])
        self._foreground_color = int(self._config["foreground-color"])
        self._background_color = int(self._config["background-color"])

        self.img = Image.new('L', (self._width, self._height), self._background_color)

        self._group_by = 15  # fixed step size for chart. -> 4 steps per hour / 24 hours -> 96 steps
        groups_per_hour = int(60 / self._group_by)
        pixel_per_hour = int(self._width / 24)
        self._pixel_per_slot = int(pixel_per_hour / groups_per_hour)

        if self._height % 2 != 0:
            self._logger.error("ScheduleImage - height ({}) must be dividable by 2.".format(self._height))
            raise ValueError("ScheduleImage - height ({}) must be dividable by 2.".format(self._height))
        self._pixel_per_dot = int(self._height / 2)

        self._set_pattern_schedule(schedule_items, self._config["patterns"])
        self._render_image()

    def _set_pattern_schedule(self, schedule_items, patterns):
        """
        Merge the 96 schedule items with the patterns from the config yaml structure to the pattern schedule needed for
        image generation.

        :param schedule_items: list of 96 mode entries
        :param patterns: dict with mode.entry as key and 0-3 as value
        """

        patterns = dict((k.lower(), v) for k, v in patterns.items())
        self._pattern_schedule = []

        for k,v in schedule_items.items():
            try:
                pattern = patterns[v.name.lower()]
                self._logger.info("ScheduleImage._set_pattern_schedule - [{}]: add pattern {}/{}.".
                                  format(k, v, pattern))
                self._pattern_schedule.append(pattern)
            except KeyError as e:
                self._logger.error("ScheduleImage._set_pattern_schedule - no pattern for schedule item '{}': {}".
                                   format(k, e))
                raise e

    def _render_image(self):
        """
        Generate image. Result is stored in property img.
        """

        self._logger.info("ScheduleImage._render_image() - pixel/dot: {}, pixel/slot: {}.".
                          format(self._pixel_per_dot, self._pixel_per_slot))
        # clear image
        draw = ImageDraw.Draw(self.img)
        draw.rectangle((0, 0, self._width, self._height), fill=self._background_color)
        # draw graph
        count = 0
        for pattern in self._pattern_schedule:
            self._logger.info("ScheduleImage._render_image - {}. pattern is {}.".format(count, pattern))
            x_from = count * self._pixel_per_slot
            x_to = x_from + self._pixel_per_slot - 1
            count = count + 1
            if pattern == 0: # nothing is displayed
                continue
            elif pattern == 1: # lower dot
                y_lower = self._height - 1
                y_upper = self._height - self._pixel_per_dot
            elif pattern == 2:  # upper dot
                y_lower = self._height - self._pixel_per_dot - 1
                y_upper = 0
            elif pattern == 3: # full height
                y_lower = self._height - 1
                y_upper = 0
            else:
                self._logger.error("ScheduleImage.update_image - unknown value for pattern '{}'.".format(pattern))
                raise ValueError("ScheduleImage.update_image - unknown value for pattern '{}'.".format(pattern))
            self._logger.info("ScheduleImage.update_image - rectangle({}/{}-{}/{}).".
                              format(count, pattern, x_from, y_lower, x_to, y_upper))
            draw.rectangle((x_from, y_lower, x_to, y_upper), fill=self._foreground_color)

