from argaeus.controller.modes.modecontroller import ModeController
from argaeus.controller.setpointcontroller import SetPointController
from argaeus.controller.operationcontroller import OperationController
from pelops.abstractmicroservice import AbstractMicroservice
import time
from argaeus.schema.thermostatguicontroller import get_schema
import argaeus
import threading


class ThermostatGUIController(AbstractMicroservice):
    """
    Main component of argaeus - initializes the three controller: mode, set-point, and operation and updates the state
    every minute (e.g. check if the current schedule entry is a new mode entry).

    config yaml entries:
        setpoint-controller:
            ...
        mode-controller:
            ...
        operation-controller:
            ...
    """
    _version = argaeus.version  # version of software

    _loop_thread = None  # Thread instance containing _poll_loop

    _mode_controller = None  # mode controller instance
    _set_point_controller = None  # set point controller instance
    _operation_controller = None  # operation controller instance

    def __init__(self, config, mqtt_client=None, logger=None):
        """
        Constructor

        :param config: config yaml structure
        :param mqtt_client: mymqttclient instance (optional)
        :param logger: logger instance (optionale)
        """
        AbstractMicroservice.__init__(self, config, "controller", mqtt_client=mqtt_client, logger=logger,
                                      logger_name=__name__)

        self._mode_controller = ModeController(self._config["mode-controller"], self._mqtt_client, self._logger)
        self._set_point_controller = SetPointController(self._mode_controller, self._config["setpoint-controller"],
                                                        self._mqtt_client, self._logger)
        self._operation_controller = OperationController(self._config["operation-controller"], self._mqtt_client,
                                                         self._logger)

        self._loop_thread = threading.Thread(target=self._poll_loop)

    @staticmethod
    def _calc_sleep_time():
        """
        calculate the seconds.milliseconds until the next full minute
        :return: seconds.milliseconds until next full minute
        """
        current_time = time.time()
        seconds_to_next_full_minute = (60 - current_time % 60)  # next full minute in seconds
        return seconds_to_next_full_minute

    def _poll_loop(self):
        """
        updates mode_controller each excatly each minute until _Stop_Service event.
        """
        self._logger.info("ThermostatGUIController._poll_loop - start")
        while not self._stop_service.isSet():
            self._mode_controller.update()
            sleep_for = ThermostatGUIController._calc_sleep_time()
            self._logger.info("ThermostatGUIController._poll_loop - sleeping for {} seconds.".format(sleep_for))
            self._stop_service.wait(timeout=sleep_for)
        self._logger.info("ThermostatGUIController._poll_loop - end")

    def _start(self):
        """starts the three controller and the loop"""
        self._mode_controller.start()
        self._set_point_controller.start()
        self._operation_controller.start()
        self._loop_thread.start()

    def _stop(self):
        """stops the loop and the three controller"""
        self._loop_thread.join()
        self._mode_controller.stop()
        self._set_point_controller.stop()
        self._operation_controller.stop()

    @classmethod
    def _get_schema(cls):
        return get_schema()

    @classmethod
    def _get_description(cls):
        return "Argaeus is the gui controller element for a thermostat."


def standalone():
    ThermostatGUIController.standalone()


if __name__ == "__main__":
    ThermostatGUIController.standalone()
