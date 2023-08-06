import unittest
import os
import sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from pelops.mylogger import create_logger
from pelops.mymqttclient import MyMQTTClient
from pelops.myconfigtools import read_config
from argaeus.controller.setpointcontroller import SetPointController
from argaeus.controller.modes.modecontroller import ModeController
import time, datetime
import math
import threading


class Test_OperationController(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.config = read_config(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')) +
                                 "/tests_unit/config.yaml")
        cls.logger = create_logger(cls.config["logger"], "Test_OperationController")
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
            pass # wait time is short enough - no need to bother user
        time.sleep(wait)

    def test_0init(self):
        mc = ModeController(self.config["controller"]["mode-controller"], self.mqtt_client, self.logger)
        self.assertIsNotNone(mc)
        spc = SetPointController(mc, self.config["controller"]["setpoint-controller"], self.mqtt_client,
                                 self.logger)
        self.assertIsNotNone(spc)
        self.assertEqual(spc._step_size, float(self.config["controller"]["setpoint-controller"]["step-size"]))
        self.assertEqual(spc._min_temp, float(self.config["controller"]["setpoint-controller"]["min-temp"]))
        self.assertEqual(spc._max_temp, float(self.config["controller"]["setpoint-controller"]["max-temp"]))
        self.assertEqual(spc._topic_sub_down, self.config["controller"]["setpoint-controller"]["topic-sub-down"])
        self.assertEqual(spc._command_down, self.config["controller"]["setpoint-controller"]["command-down"])
        self.assertEqual(spc._topic_sub_up, self.config["controller"]["setpoint-controller"]["topic-sub-up"])
        self.assertEqual(spc._command_up, self.config["controller"]["setpoint-controller"]["command-up"])
        self.assertEqual(spc._topic_sub_reset, self.config["controller"]["setpoint-controller"]["topic-sub-reset"])
        self.assertEqual(spc._command_reset, self.config["controller"]["setpoint-controller"]["command-reset"])

    def test_1start_stop(self):
        mc = ModeController(self.config["controller"]["mode-controller"], self.mqtt_client, self.logger)
        self.assertIsNotNone(mc)
        spc = SetPointController(mc, self.config["controller"]["setpoint-controller"], self.mqtt_client,
                                 self.logger)
        self.assertIsNotNone(spc)
        spc.start()
        spc.stop()

    def test_2inc(self):
        sph = threading.Event()
        sph.clear()
        setpoints = []

        def _set_point_handler(value):
            setpoints.append(float(value))
            sph.set()

        mc = ModeController(self.config["controller"]["mode-controller"], self.mqtt_client, self.logger)
        self.assertIsNotNone(mc)
        spc = SetPointController(mc, self.config["controller"]["setpoint-controller"], self.mqtt_client,
                                 self.logger)
        self.assertIsNotNone(spc)

        self.mqtt_client.subscribe(mc.current_program._topic_pub_set_point, _set_point_handler)

        spc.start()

        self.assertLess(mc.current_program.set_point, spc._max_temp-2)
        for i in range((math.ceil(spc._max_temp-mc.current_program.set_point)+1)*math.ceil(1/spc._step_size)):
            self.mqtt_client.publish(spc._topic_sub_up, spc._command_up)
            sph.wait()
            sph.clear()
        self.assertEqual(mc.current_program.set_point, spc._max_temp)

        while setpoints[len(setpoints)-2] == spc._max_temp:
            setpoints.pop()

        self.assertListEqual(setpoints[-7:], [27.0, 27.5, 28.0, 28.5, 29.0, 29.5, 30.0])
        spc.stop()

    def test_3dec(self):
        sph = threading.Event()
        sph.clear()
        setpoints = []

        def _set_point_handler(value):
            setpoints.append(float(value))
            sph.set()

        mc = ModeController(self.config["controller"]["mode-controller"], self.mqtt_client, self.logger)
        self.assertIsNotNone(mc)
        spc = SetPointController(mc, self.config["controller"]["setpoint-controller"], self.mqtt_client,
                                 self.logger)
        self.assertIsNotNone(spc)

        self.mqtt_client.subscribe(mc.current_program._topic_pub_set_point, _set_point_handler)

        spc.start()

        self.assertGreater(mc.current_program.set_point, spc._min_temp+2)
        for i in range((math.ceil(mc.current_program.set_point-spc._min_temp)+1)*math.ceil(1/spc._step_size)):
            self.mqtt_client.publish(spc._topic_sub_down, spc._command_down)
            sph.wait()
            sph.clear()
        self.assertEqual(mc.current_program.set_point, spc._min_temp)

        while setpoints[len(setpoints)-2] == spc._min_temp:
            setpoints.pop()

        self.assertListEqual(setpoints[-7:], [13.0, 12.5, 12.0, 11.5, 11.0, 10.5, 10.0])
        spc.stop()

    def test_4reset(self):
        rh = threading.Event()
        rh.clear()

        def _reset_handler(value):
            rh.set()

        self.mqtt_client.subscribe(self.config["controller"]["setpoint-controller"]["topic-sub-reset"], _reset_handler)

        mc = ModeController(self.config["controller"]["mode-controller"], self.mqtt_client, self.logger)
        self.assertIsNotNone(mc)
        spc = SetPointController(mc, self.config["controller"]["setpoint-controller"], self.mqtt_client,
                                 self.logger)
        self.assertIsNotNone(spc)
        spc.start()
        mc.start()
        mc.current_program.set_point = 10
        self.assertEqual(mc.current_program.set_point, 10)
        self.mqtt_client.publish(self.config["controller"]["setpoint-controller"]["topic-sub-reset"],
                                 self.config["controller"]["setpoint-controller"]["command-reset"])
        rh.wait()
        rh.clear()
        time.sleep(0.1)

        self.assertEqual(mc.current_program.set_point, mc.current_program.default_set_point)
        spc.stop()
        mc.stop()


if __name__ == '__main__':
    unittest.main()
