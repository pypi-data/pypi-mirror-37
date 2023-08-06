import unittest
import os
import sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from pelops.mylogger import create_logger
from pelops.mymqttclient import MyMQTTClient
from pelops.myconfigtools import read_config, validate_config
from argaeus.thermostatguicontroller import ThermostatGUIController
import time
import threading


class Test_ThermostatGUIController(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.config = read_config(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')) +
                                 "/tests_unit/config.yaml")
        cls.logger = create_logger(cls.config["logger"], "Test_ThermostatGUIController")
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
        self._wait()

    def _wait(self, minimum_seconds_to_next_minute=5):
        # guarantee that we will not have a racing condidtion like timestamp init is "00:14:59" and timestmap
        # assertion is "00:15:01" which could result in different schedule entries being used.
        wait = (60 - time.time() % 60) + 0.1
        if wait > minimum_seconds_to_next_minute:
            wait = 0  # everything is fine
        elif wait > 1:
            print("... waiting {} seconds before test starts.".format(wait))
        else:
            pass  # wait time is short enough - no need to bother user
        time.sleep(wait)

    def test_0init(self):
        tgc = ThermostatGUIController(self.config, self.mqtt_client, self.logger)
        self.assertIsNotNone(tgc)
        self.assertIsNotNone(tgc._operation_controller)
        self.assertIsNotNone(tgc._set_point_controller)
        self.assertIsNotNone(tgc._mode_controller)

    def test_1start_stop(self):
        self._wait(10)

        hsi = threading.Event()
        hmi = threading.Event()
        hsp = threading.Event()
        ch = threading.Event()
        hsi.clear()
        hmi.clear()
        hsp.clear()
        ch.clear()

        def _handler_schedule_image(value):
            hsi.set()

        def _handler_mode_icon(value):
            hmi.set()

        def _handler_set_point(value):
            hsp.set()

        def _command_handler(value):
            ch.set()

        self.mqtt_client.subscribe(self.config["controller"]["operation-controller"]["topic-pub"], _command_handler)
        self.mqtt_client.subscribe(
            self.config["controller"]["mode-controller"]["topics-pub"]["display-server-schedule-image"],
            _handler_schedule_image)
        self.mqtt_client.subscribe(
            self.config["controller"]["mode-controller"]["topics-pub"]["display-server-mode-icon"],
            _handler_mode_icon)
        self.mqtt_client.subscribe(
            self.config["controller"]["mode-controller"]["topics-pub"]["temperature-set-point"],
            _handler_set_point)

        tgc = ThermostatGUIController(self.config, self.mqtt_client, self.logger)
        tgc.start()

        hsi.wait()
        hmi.wait()
        hsp.wait()
        ch.wait()

        t = time.time()
        tgc.stop()
        diff = time.time() - t
        self.assertLess(diff, 2)  # stopping should be relatively fast - faster than the next poll intervall at least

    def test_1start_stop(self):
        self._wait(10)

        hsi = threading.Event()
        hmi = threading.Event()
        hsp = threading.Event()
        hsi.clear()
        hmi.clear()
        hsp.clear()

        def _handler_schedule_image(value):
            hsi.set()

        def _handler_mode_icon(value):
            hmi.set()

        def _handler_set_point(value):
            hsp.set()

        self.mqtt_client.subscribe(
            self.config["controller"]["mode-controller"]["topics-pub"]["display-server-schedule-image"],
            _handler_schedule_image)
        self.mqtt_client.subscribe(
            self.config["controller"]["mode-controller"]["topics-pub"]["display-server-mode-icon"],
            _handler_mode_icon)
        self.mqtt_client.subscribe(
            self.config["controller"]["mode-controller"]["topics-pub"]["temperature-set-point"],
            _handler_set_point)

        tgc = ThermostatGUIController(self.config, self.mqtt_client, self.logger)
        tgc.start()
        start_time = time.time()

        hsi.wait()
        hmi.wait()
        hsp.wait()
        hsi.clear()
        hmi.clear()
        hsp.clear()
        hsi.wait()
        hmi.wait()
        hsp.wait()
        hsi.clear()
        hmi.clear()
        hsp.clear()

        wait_time = (60 - start_time) % 60  # seconds to next update loop
        print("waiting for {} seconds for next event.".format(wait_time))
        hsi.wait(timeout=wait_time+0.1)  # add safety seconds
        hmi.wait()
        hsp.wait()
        self.assertTrue(hsi.is_set())
        self.assertTrue(hmi.is_set())
        self.assertTrue(hsp.is_set())

        self.assertLess(time.time(), start_time+wait_time+0.1)
        self.assertGreater(time.time(), start_time+wait_time-0.1)

        tgc.stop()


if __name__ == '__main__':
    unittest.main()

