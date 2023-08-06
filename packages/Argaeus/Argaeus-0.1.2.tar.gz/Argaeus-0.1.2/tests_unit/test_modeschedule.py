import unittest
import os
import sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from pelops.mylogger import create_logger
from pelops.mymqttclient import MyMQTTClient
from pelops.myconfigtools import read_config, validate_config
from argaeus.controller.modes.modeprogram import ModeProgram
from argaeus.controller.modes.modeschedule import ModeSchedule
import collections
import datetime
import threading
from io import BytesIO
from PIL import Image


class Test_ModeSchedule(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.config = read_config(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')) +
                                 "/tests_unit/config.yaml")
        cls.logger = create_logger(cls.config["logger"], "Test_ModeSchedule")
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

        self.topics_pub_config = {
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

        self.program_modes = {}
        modes_config = []
        for name in mode_names:
            mode_program_base["name"] = name
            mp = ModeProgram(mode_program_base, self.topics_pub_config, self.mqtt_client, self.logger)
            self.program_modes[name] = mp
            modes_config.append(mode_program_base.copy())

        schedule_config = collections.OrderedDict()
        counter = 0
        for hour in range(24):
            for minute in range(0, 60, 15):
                name = "{:02d}:{:02d}".format(hour, minute)
                if counter < 96/4:
                    schedule_config[name] = self.program_modes["A"].name
                elif counter < 96/2:
                    schedule_config[name] = self.program_modes["B"].name
                elif counter < 96/4*3:
                    schedule_config[name] = self.program_modes["C"].name
                else:
                    schedule_config[name] = self.program_modes["D"].name
                counter += 1

        self.mode_schedule = {
            "name": "S",
            "type": "schedule",
            "selectable": True,
            "image": img_config,
            "schedule": schedule_config
        }

    def test_0init(self):
        ms = ModeSchedule(self.mode_schedule, self.topics_pub_config, self.mqtt_client, self.logger)
        self.assertIsNotNone(ms)
        self.assertEqual(ms._topic_pub, self.topics_pub_config["display-server-schedule-image"])
        self.assertEqual(len(ms.schedule), 0)
        self.assertEqual(len(ms.schedule_raw), 96)

        for k, value in ms.schedule_raw.items():
            key = "{:02d}:{:02d}".format(k.hour, k.minute)
            self.assertEqual(self.mode_schedule["schedule"][key], value)

        self.assertEqual(ms.selectable, True)
        self.assertEqual(ms.name, "S")
        self.assertIsNone(ms.img)

    def test_1sort_dict(self):
        sr_source = self.mode_schedule["schedule"].copy()
        self.assertEqual(len(sr_source), 96)

        # reverse order of entries
        sr_reverse = {}
        while len(sr_source) > 0:
            key, value = sr_source.popitem()
            sr_reverse[key] = value
        self.assertEqual(len(sr_reverse), 96)

        # check that order of entries is in fact reversed
        sr = self.mode_schedule["schedule"].copy()
        self.assertEqual(type(sr), collections.OrderedDict)
        self.assertEqual(type(sr_reverse), dict)
        self.assertNotEqual(list(sr.keys())[0], list(sr_reverse.keys())[0])
        self.assertNotEqual(list(sr.keys())[95], list(sr_reverse.keys())[95])
        self.assertEqual(list(sr.keys())[0], list(sr_reverse.keys())[95])
        self.assertEqual(list(sr.keys())[95], list(sr_reverse.keys())[0])

        # get ordered dict
        sr_target = ModeSchedule._sort_dict(sr_reverse)
        self.assertEqual(len(sr_target), 96)

        # check that order of entries is in fact ordered
        sr = self.mode_schedule["schedule"].copy()
        self.assertEqual(type(sr), collections.OrderedDict)
        self.assertEqual(type(sr_target), collections.OrderedDict)

        prev_key = None
        for key, value in sr_target.items():
            if prev_key is not None:
                self.assertTrue(prev_key<key)
            prev_key = key

    def test_2map(self):
        ms = ModeSchedule(self.mode_schedule, self.topics_pub_config, self.mqtt_client, self.logger)
        self.assertIsNotNone(ms)
        self.assertEqual(len(ms.schedule), 0)
        ms.map_schedule_modes(self.program_modes)
        self.assertEqual(len(ms.schedule), 96)
        self.assertIsNotNone(ms.img)

        for k,value in ms.schedule.items():
            key = "{:02d}:{:02d}".format(k.hour, k.minute)
            self.assertEqual(self.mode_schedule["schedule"][key], value.name)
            self.assertIn(value, self.program_modes.values())

    def test_3get_program_at_time(self):
        ms = ModeSchedule(self.mode_schedule, self.topics_pub_config, self.mqtt_client, self.logger)
        ms.map_schedule_modes(self.program_modes)

        counter = 0
        max_counter = 24*60
        for hour in range(24):
            for minute in range(60):
                key = datetime.time(hour=hour, minute=minute)
                program = ms.get_program_at_time(key)
                if counter < max_counter/4:
                    self.assertEqual(program, self.program_modes["A"])
                elif counter < max_counter/2:
                    self.assertEqual(program, self.program_modes["B"])
                elif counter < max_counter/4*3:
                    self.assertEqual(program, self.program_modes["C"])
                else:
                    self.assertEqual(program, self.program_modes["D"])
                counter += 1

    def test_4mqtt(self):
        on_message_event = threading.Event()
        on_message_event.clear()

        def _on_message(value):
            try:
                os.mkdir("modeschedule")
            except FileExistsError:
                pass

            mqtt_image = Image.open(BytesIO(value))
            mqtt_image = mqtt_image.convert("L")

            self.assertEqual(mqtt_image.size[0], 192)
            self.assertEqual(mqtt_image.size[1], 2)

            mqtt_image.save("modeschedule/modeschedule_0.png")
            on_message_event.set()

        self.mqtt_client.subscribe(self.topics_pub_config["display-server-schedule-image"], _on_message)

        ms = ModeSchedule(self.mode_schedule, self.topics_pub_config, self.mqtt_client, self.logger)
        ms.map_schedule_modes(self.program_modes)

        ms.publish()
        on_message_event.wait(0.5)
        self.assertTrue(on_message_event.is_set())


if __name__ == '__main__':
    unittest.main()
