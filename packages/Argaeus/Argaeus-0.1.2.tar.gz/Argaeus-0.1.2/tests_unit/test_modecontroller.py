import unittest
import os
import sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from pelops.mylogger import create_logger
from pelops.mymqttclient import MyMQTTClient
from pelops.myconfigtools import read_config, validate_config
from argaeus.controller.modes.modecontroller import ModeController
from PIL import Image, ImageChops
from io import BytesIO
import time, datetime
import math
import threading


class Test_ModeController(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.config = read_config(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')) +
                                 "/tests_unit/config.yaml")
        cls.logger = create_logger(cls.config["logger"], "Test_ModeController")
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

    @staticmethod
    def _equal(im1, im2):
        return ImageChops.difference(im1, im2).getbbox() is None

    def test_0init(self):
        mc = ModeController(self.config["controller"]["mode-controller"], self.mqtt_client, self.logger)
        self.assertIsNotNone(mc)
        self.assertEqual(len(mc._modes), 5)
        self.assertEqual(mc.current_mode.name, "Schedule")
        self.assertEqual(len(mc.current_schedule), 96)

        now = datetime.datetime.now().time()
        pos = math.floor(datetime.timedelta(hours=now.hour, minutes=now.minute)  / datetime.timedelta(minutes=15))
        current_program = list(mc.current_schedule.values())[pos]
        self.assertEqual(mc.current_program.name, current_program)

        self.assertEqual(mc._topic_sub_prev, self.config["controller"]["mode-controller"]["topics-sub"]["to-prev"])
        self.assertEqual(mc._command_prev, self.config["controller"]["mode-controller"]["topics-sub"]["command-prev"])
        self.assertEqual(mc._topic_sub_next, self.config["controller"]["mode-controller"]["topics-sub"]["to-next"])
        self.assertEqual(mc._command_next, self.config["controller"]["mode-controller"]["topics-sub"]["command-next"])
        self.assertEqual(mc._topic_pub_schedule_image,
                         self.config["controller"]["mode-controller"]["topics-pub"]["display-server-schedule-image"])
        self.assertEqual(mc._topic_sub_to_default,
                         self.config["controller"]["mode-controller"]["topics-sub"]["to-default"])
        self.assertEqual(mc._command_default,
                         self.config["controller"]["mode-controller"]["topics-sub"]["command-default"])

    def test_1start_stop(self):
        hsi = threading.Event()
        hsi.clear()
        hmi = threading.Event()
        hmi.clear()
        hsp = threading.Event()
        hsp.clear()

        def _handler_schedule_image(value):
            self.assertTrue(len(value)>0)
            mqtt_image = Image.open(BytesIO(value))
            mqtt_image = mqtt_image.convert("L")
            Test_ModeController._equal(mqtt_image, mc.current_mode.img)
            hsi.set()

        def _handler_mode_icon(value):
            self.assertEqual(value.decode("UTF-8"), mc.current_program.name.lower())
            hmi.set()

        def _handler_set_point(value):
            self.assertEqual(float(value), mc.current_program.set_point)
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

        mc = ModeController(self.config["controller"]["mode-controller"], self.mqtt_client, self.logger)
        self.assertIsNotNone(mc)
        mc.start()

        hsi.wait()
        hsp.wait()
        hmi.wait()

        mc.stop()

    def test_2prev_next(self):
        self._wait()

        def _clear_all():
            hmi.clear()
            hsi.clear()
            hsp.clear()

        def _wait_all():
            hmi.wait()
            hsi.wait()
            hsp.wait()

        hsi = threading.Event()
        hmi = threading.Event()
        hsp = threading.Event()

        _clear_all()

        schedule_images = []
        mode_icons = []
        set_points = []

        def _handler_schedule_image(value):
            if len(value)>0:
                mqtt_image = Image.open(BytesIO(value))
                mqtt_image = mqtt_image.convert("L")
                self.assertIsNotNone(mqtt_image)
                schedule_images.append(mqtt_image)
            else:
                schedule_images.append(None)
            hsi.set()

        def _handler_mode_icon(value):
            self.assertEqual(value.decode("UTF-8"), mc.current_program.name.lower())
            mode_icons.append(value.decode("UTF-8"))
            hmi.set()

        def _handler_set_point(value):
            self.assertEqual(float(value), mc.current_program.set_point)
            set_points.append(float(value))
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

        mc = ModeController(self.config["controller"]["mode-controller"], self.mqtt_client, self.logger)
        self.assertIsNotNone(mc)
        default_program = mc.current_program.name.lower()
        default_setpoint = mc.current_program.set_point
        mc.start()
        _wait_all()
        _clear_all()

        # turn counter-clockwise
        self.mqtt_client.publish(mc._topic_sub_prev, mc._command_prev)
        _wait_all()
        _clear_all()
        self.mqtt_client.publish(mc._topic_sub_prev, mc._command_prev)
        _wait_all()
        _clear_all()
        self.mqtt_client.publish(mc._topic_sub_prev, mc._command_prev)
        _wait_all()
        _clear_all()
        self.mqtt_client.publish(mc._topic_sub_prev, mc._command_prev)
        _wait_all()
        _clear_all()

        # turn clockwise
        self.mqtt_client.publish(mc._topic_sub_next, mc._command_next)
        _wait_all()
        _clear_all()
        self.mqtt_client.publish(mc._topic_sub_next, mc._command_next)
        _wait_all()
        _clear_all()
        self.mqtt_client.publish(mc._topic_sub_next, mc._command_next)
        _wait_all()
        _clear_all()
        self.mqtt_client.publish(mc._topic_sub_next, mc._command_next)
        _wait_all()
        _clear_all()

        mc.stop()

        self.assertListEqual(set_points, [default_setpoint, 21.5, 23.0, 19.5, default_setpoint, 19.5, 23.0, 21.5,
                                          default_setpoint])
        self.assertListEqual(mode_icons, [default_program, 'morning', 'day', 'night', default_program, 'night', 'day',
                                          'morning', default_program])
        self.assertIsNotNone(schedule_images[0])
        self.assertIsNone(schedule_images[1])
        self.assertIsNone(schedule_images[2])
        self.assertIsNone(schedule_images[3])
        self.assertIsNotNone(schedule_images[4])
        self.assertIsNone(schedule_images[5])
        self.assertIsNone(schedule_images[6])
        self.assertIsNone(schedule_images[7])
        self.assertIsNotNone(schedule_images[8])

    def test_3to_default_mode(self):
        self._wait()

        def _clear_all():
            hmi.clear()
            hsi.clear()
            hsp.clear()

        def _wait_all():
            hmi.wait()
            hsi.wait()
            hsp.wait()

        hsi = threading.Event()
        hmi = threading.Event()
        hsp = threading.Event()

        _clear_all()

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

        mc = ModeController(self.config["controller"]["mode-controller"], self.mqtt_client, self.logger)
        self.assertIsNotNone(mc)
        default_program = mc.current_program.name.lower()
        default_setpoint = mc.current_program.set_point

        mc.start()
        _wait_all()
        _clear_all()

        # turn counter-clockwise
        self.mqtt_client.publish(mc._topic_sub_prev, mc._command_prev)
        _wait_all()
        _clear_all()
        self.assertNotEqual(default_program, mc.current_program.name.lower())
        self.assertNotEqual(default_setpoint, mc.current_program.set_point)

        self.mqtt_client.publish(self.config["controller"]["mode-controller"]["topics-sub"]["to-default"],
                                 self.config["controller"]["mode-controller"]["topics-sub"]["command-default"])
        _wait_all()
        _clear_all()

        self.assertEqual(default_program, mc.current_program.name.lower())
        self.assertEqual(default_setpoint, mc.current_program.set_point)

        mc.stop()


if __name__ == '__main__':
    unittest.main()
