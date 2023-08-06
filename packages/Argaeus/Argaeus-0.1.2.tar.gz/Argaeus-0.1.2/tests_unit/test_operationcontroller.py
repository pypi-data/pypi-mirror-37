import unittest
import os
import sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from pelops.mylogger import create_logger
from pelops.mymqttclient import MyMQTTClient
from pelops.myconfigtools import read_config, validate_config
from argaeus.controller.operationcontroller import OperationController
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
        pass

    def test_0init(self):
        oc = OperationController(self.config["controller"]["operation-controller"], self.mqtt_client, self.logger)
        self.assertIsNotNone(oc)
        self.assertEqual(oc._default_is_active, oc.active_operation)
        self.assertEqual(oc._default_is_active, self.config["controller"]["operation-controller"]["default-is-active"])
        self.assertEqual(oc._topic_pub, self.config["controller"]["operation-controller"]["topic-pub"])
        self.assertEqual(oc._command_active, self.config["controller"]["operation-controller"]["command-active"])
        self.assertEqual(oc._command_passive, self.config["controller"]["operation-controller"]["command-passive"])
        self.assertEqual(oc._topic_sub_toggle, self.config["controller"]["operation-controller"]["topic-sub-toggle"])
        self.assertEqual(oc._command_sub_toggle, self.config["controller"]["operation-controller"]["command-toggle"])

    def test_1start_stop(self):
        ch = threading.Event()
        ch.clear()

        def _command_handler(value):
            value = value.decode("UTF-8")
            self.assertEqual(value, oc._command_active)
            ch.set()

        self.mqtt_client.subscribe(self.config["controller"]["operation-controller"]["topic-pub"], _command_handler)
        oc = OperationController(self.config["controller"]["operation-controller"], self.mqtt_client, self.logger)
        self.assertIsNotNone(oc)

        oc.start()
        ch.wait()
        oc.stop()

    def test_2behavior(self):
        ch = threading.Event()
        ch.clear()

        states = []

        def _command_handler(value):
            value = value.decode("UTF-8")
            self.assertTrue(value == oc._command_active or value == oc._command_passive)
            states.append(value)
            ch.set()

        self.mqtt_client.subscribe(self.config["controller"]["operation-controller"]["topic-pub"], _command_handler)
        oc = OperationController(self.config["controller"]["operation-controller"], self.mqtt_client, self.logger)
        self.assertIsNotNone(oc)

        oc.start()
        ch.wait()
        ch.clear()

        for i in range(4):
            self.mqtt_client.publish(self.config["controller"]["operation-controller"]["topic-sub-toggle"],
                                     self.config["controller"]["operation-controller"]["command-toggle"])
            ch.wait()
            ch.clear()

        oc.stop()
        self.assertListEqual(states, ['ON', 'OFF', 'ON', 'OFF', 'ON'])

    def test_3behavior_inverse(self):
        ch = threading.Event()
        ch.clear()

        states = []

        def _command_handler(value):
            value = value.decode("UTF-8")
            self.assertTrue(value == oc._command_active or value == oc._command_passive)
            states.append(value)
            ch.set()

        self.mqtt_client.subscribe(self.config["controller"]["operation-controller"]["topic-pub"], _command_handler)
        self.config["controller"]["operation-controller"]["default-is-active"] = False
        oc = OperationController(self.config["controller"]["operation-controller"], self.mqtt_client, self.logger)
        self.assertIsNotNone(oc)

        oc.start()
        ch.wait()
        ch.clear()

        for i in range(4):
            self.mqtt_client.publish(self.config["controller"]["operation-controller"]["topic-sub-toggle"],
                                     self.config["controller"]["operation-controller"]["command-toggle"])
            ch.wait()
            ch.clear()

        oc.stop()
        self.assertListEqual(states, ['OFF', 'ON', 'OFF', 'ON', 'OFF'])


if __name__ == '__main__':
    unittest.main()
