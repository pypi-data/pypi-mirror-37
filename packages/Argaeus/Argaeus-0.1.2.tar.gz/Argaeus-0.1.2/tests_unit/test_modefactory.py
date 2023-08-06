import unittest
import os
import sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from pelops.mylogger import create_logger
from pelops.mymqttclient import MyMQTTClient
from pelops.myconfigtools import read_config, validate_config
from argaeus.controller.modes.modeprogram import ModeProgram
from argaeus.controller.modes.modeschedule import ModeSchedule
from argaeus.controller.modes.modefactory import ModeFactory
import collections


class Test_ModeFactory(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.config = read_config(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')) +
                                 "/tests_unit/config.yaml")
        cls.logger = create_logger(cls.config["logger"], "Test_ModeFactory")
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
        mode_program_base = {
            "name": "",
            "type": "program",
            "selectable": True,
            "set-point": 19.5
        }

        topics_sub_config = {
            "to-left": "/test/rotate",
            "command-left": "LEFT",
            "to-right": "/test/rotate",
            "command-right": "RIGHT"
        }

        topics_pub_config = {
            "display-server-schedule-image": "/test/schedule",
            "display-server-mode-icon": "/test/modeicon",
            "temperature-set-point": "/test/setpoint"
        }

        img_config = {
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

        mode_names = ["A", "B", "C", "D"]

        modes_config = []
        for name in mode_names:
            mode_program_base["name"] = name
            modes_config.append(mode_program_base.copy())

        modes_config[3]["selectable"] = False

        schedule_config = collections.OrderedDict()
        counter = 0
        for hour in range(24):
            for minute in range(0, 60, 15):
                name = "{:02d}:{:02d}".format(hour, minute)
                if counter < 96/4:
                    schedule_config[name] = mode_names[0]
                elif counter < 96/2:
                    schedule_config[name] = mode_names[1]
                elif counter < 96/4*3:
                    schedule_config[name] = mode_names[2]
                else:
                    schedule_config[name] = mode_names[3]
                counter += 1

        mode_schedule = {
            "name": "S",
            "type": "schedule",
            "selectable": True,
            "image": img_config,
            "schedule": schedule_config
        }
        modes_config.append(mode_schedule)

        self.config_base = {
            "default-mode": "S",
            "topics-sub": topics_sub_config,
            "topics-pub": topics_pub_config,
            "modes": modes_config
        }

    def test_0init(self):
        modes, modes_selectable = ModeFactory.create_modes(self.config_base["modes"], self.config_base["topics-pub"],
                                                           self.mqtt_client, self.logger)
        self.assertIsNotNone(modes)
        self.assertEqual(len(modes), 5)

        self.assertIsNotNone(modes_selectable)
        self.assertEqual(len(modes_selectable), 4)
        for mode in modes_selectable:
            self.assertNotEqual(mode.name, "D")
            self.assertNotEqual(mode.name, "d")

        self.assertListEqual(list(modes.keys()), ["A", "B", "C", "D", "S"])
        self.assertEqual(type(list(modes.values())[0]), ModeProgram)
        self.assertEqual(type(list(modes.values())[1]), ModeProgram)
        self.assertEqual(type(list(modes.values())[2]), ModeProgram)
        self.assertEqual(type(list(modes.values())[3]), ModeProgram)
        self.assertEqual(type(list(modes.values())[4]), ModeSchedule)
        self.assertEqual(type(modes["S"]), ModeSchedule)
        self.assertEqual(len(modes["S"].schedule_raw), 96)
        self.assertEqual(len(modes["S"].schedule), 96)
        self.assertIsNotNone(modes["S"].img)


if __name__ == '__main__':
    unittest.main()
