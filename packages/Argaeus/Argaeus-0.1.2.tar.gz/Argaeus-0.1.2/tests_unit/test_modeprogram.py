import unittest
import os
import sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from pelops.mylogger import create_logger
from pelops.mymqttclient import MyMQTTClient
from pelops.myconfigtools import read_config, validate_config
import threading
import time
from argaeus.controller.modes.modeprogram import ModeProgram


class Test_ModeProgram(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.config = read_config(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')) +
                                 "/tests_unit/config.yaml")
        cls.logger = create_logger(cls.config["logger"], "Test_ModeProgram")
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
        self.mode_config = {
            "name": "Night",
            "type": "program",
            "selectable": True,
            "set-point": 19.5
        }

        self.topics_pub_config = {
            "display-server-schedule-image": "/test/schedule",
            "display-server-mode-icon": "/test/modeicon",
            "temperature-set-point": "/test/setpoint"
            }

    def test_0init(self):
        mp = ModeProgram(self.mode_config, self.topics_pub_config, self.mqtt_client, self.logger)
        self.assertIsNotNone(mp)
        self.assertEqual(mp.name, "Night")
        self.assertEqual(mp.selectable, True)
        self.assertEqual(mp.set_point, 19.5)
        self.assertEqual(mp.default_set_point, 19.5)
        self.assertEqual(mp._topic_pub_mode_icon, "/test/modeicon")
        self.assertEqual(mp._topic_pub_set_point, "/test/setpoint")

    def test_1mqtt(self):
        global modeicon_event
        modeicon_event = threading.Event()
        modeicon_event.clear()
        global setpoint_event
        setpoint_event = threading.Event()
        setpoint_event.clear()

        def setpoint(value):
            self.assertEqual(float(value), 19.5)
            setpoint_event.set()

        def modeicon(value):
            value = value.decode("UTF-8")
            self.assertEqual(value, "Night".lower())
            modeicon_event.set()

        self.mqtt_client.subscribe("/test/modeicon", modeicon)
        self.mqtt_client.subscribe("/test/setpoint", setpoint)

        mp = ModeProgram(self.mode_config, self.topics_pub_config, self.mqtt_client, self.logger)
        mp.publish()

        modeicon_event.wait(0.5)
        setpoint_event.wait(0.5)

        self.assertEqual(modeicon_event.is_set(), True)
        self.assertEqual(setpoint_event.is_set(), True)


if __name__ == '__main__':
    unittest.main()
