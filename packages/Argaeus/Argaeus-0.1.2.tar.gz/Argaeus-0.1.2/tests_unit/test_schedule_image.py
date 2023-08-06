import unittest
import os
import sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from pelops.mylogger import create_logger
from pelops.mymqttclient import MyMQTTClient
from pelops.myconfigtools import read_config, validate_config
from argaeus.controller.modes.schedule_image import ScheduleImage
from argaeus.controller.modes.modeprogram import ModeProgram
import collections


class Test_ScheduleImage(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.config = read_config(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')) +
                                 "/tests_unit/config.yaml")
        cls.logger = create_logger(cls.config["logger"], "Test_ScheduleImage")
        cls.logger.info("start")
        cls.mqtt_client = MyMQTTClient(cls.config["mqtt"], cls.logger)
        cls.mqtt_client.connect()

    @classmethod
    def tearDownClass(cls):
        cls.mqtt_client.disconnect()
        cls.logger.info("end")

    def tearDown(self):
        self.mqtt_client.unsubscribe_all()

    def setUp(self):
        mode_config_base = {
            "name": "",
            "type": "program",
            "selectable": True,
            "set-point": 19.5
        }

        topics_pub_config = {
            "display-server-schedule-image": "/test/schedule",
            "display-server-mode-icon": "/test/modeicon",
            "temperature-set-point": "/test/setpoint"
        }

        mode_names = ["A", "B", "C", "D"]

        modes = {}
        for name in mode_names:
            mode_config_base["name"] = name
            mp = ModeProgram(mode_config_base, topics_pub_config, self.mqtt_client, self.logger)
            modes[name] = mp

        self.schedule_items = collections.OrderedDict()
        id = 0
        for name in mode_names:
            for i in range(int(96/4)):
                self.schedule_items[id] = modes[name]
                id += 1

        self.config_image = {
            "width": 192,
            "height": 2,
            "foreground-color": 255,
            "background-color": 100,
            "patterns": {
                "A": 0,
                "B": 1,
                "C": 2,
                "D": 3
            }
        }

    def _assertEqual_list(self, list, value):
        for entry in list:
            self.assertEqual(entry, value)

    def _get_horizontal_pixel(self, img, x, height):
        upper_pixel = []
        lower_pixel = []

        for y in range(height):
            if y < height/2:
                upper_pixel.append(img.getpixel((x, 0)))
            else:
                lower_pixel.append(img.getpixel((x, height - 1)))

        return lower_pixel, upper_pixel

    def _check_image(self, img, width, height):
        for x in range(width):
            lower_pixel, upper_pixel = self._get_horizontal_pixel(img, x, height)
            if x < width/2:
                self._assertEqual_list(upper_pixel, self.config_image["background-color"])
                if x < width/4:
                    self._assertEqual_list(lower_pixel, self.config_image["background-color"])
                else:
                    self._assertEqual_list(lower_pixel, self.config_image["foreground-color"])
            else:
                self._assertEqual_list(upper_pixel, self.config_image["foreground-color"])
                if x < width/4*3:
                    self._assertEqual_list(lower_pixel, self.config_image["background-color"])
                else:
                    self._assertEqual_list(lower_pixel, self.config_image["foreground-color"])

    def test_0image(self):
        width = self.config_image["width"]
        height = self.config_image["height"]
        si = ScheduleImage(self.schedule_items, self.config_image, self.logger)
        self.assertIsNotNone(si)
        self.assertIsNotNone(si.img)

        try:
            os.mkdir("scheduleimage")
        except FileExistsError:
            pass
        si.img.save("scheduleimage/scheduleimage_0.png")

        self.assertEqual(si.img.size[0], width)
        self.assertEqual(si.img.size[1], height)

        self._check_image(si.img, width, height)

    def test_1image_large(self):
        self.config_image["width"] = 192*2
        self.config_image["height"] = 12
        width = self.config_image["width"]
        height = self.config_image["height"]

        si = ScheduleImage(self.schedule_items, self.config_image, self.logger)
        self.assertIsNotNone(si)
        self.assertIsNotNone(si.img)

        try:
            os.mkdir("scheduleimage")
        except FileExistsError:
            pass
        si.img.save("scheduleimage/scheduleimage_1.png")

        self.assertEqual(si.img.size[0], width)
        self.assertEqual(si.img.size[1], height)

        self._check_image(si.img, width, height)

    def test_2not_enough_patterns(self):
        del self.config_image["patterns"]["D"]
        with self.assertRaises(KeyError):
            si = ScheduleImage(self.schedule_items, self.config_image, self.logger)


if __name__ == '__main__':
    unittest.main()
