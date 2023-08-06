import Adafruit_DHT
from copreus.baseclasses.adriver import ADriver
from copreus.baseclasses.apolling import APolling
from copreus.baseclasses.calibratedvalue import CalibratedValue
from copreus.schema.dht import get_schema


class DHT(ADriver, APolling):
    """Driver for the DHT temperature/humidity sensor family.

    The driver entry in the yaml file consists of:
      * ADriver entries
        * topics_pub: temperature, humidity
      * APolling entries
      * CalibratedValue entries in a sub-block named 'calibration_temperature'
      * CalibratedValue entries in a sub-block named 'calibration_humidity'
      * DHT entries
        * pin: gpio @ raspberry
        * sensor-type: DHT11, DHT22, AM2302

    Example:
    device:
        type: dht
        sensor-type: DHT22
        poll-interval: 30
        pin: 26
        topics-pub:
            temperature: /dht22/temperature/raw
            humidity: /dht22/humidity/raw
        topics-sub:
            poll-now: /dht22/pollnow
        mqtt-translations:
            poll-now: True
        use-calibration-temperature: True
        calibration-temperature:
        # - [ref_value, raw_value]
        use-calibration-humidity: True
        calibration-humidity:
        # - [ref_value, raw_value]
    """

    _pin = -1  # gpio pin id
    _sensor_type = None  # sensor type (one of the values in dict _sensor_type_list)
    _sensor_type_list = {  # list of valid sensor types. the sensor-type entry in yaml must be one of the keys.
        "DHT11": Adafruit_DHT.DHT11,
        "DHT22": Adafruit_DHT.DHT22,
        "AM2302": Adafruit_DHT.AM2302,
    }
    _calibrated_t = None  # copreus.baseclasses.CalibratedValue for temperature
    _calibrated_h = None  # copreus.baseclasses.CalibratedValue for humidity

    def __init__(self, config, mqtt_client=None, logger=None):
        ADriver.__init__(self, config, mqtt_client, logger, logger_name=__name__)
        APolling.__init__(self, self._config, self._mqtt_client, self._logger)
        self._pin = self._config["pin"]

        if self._config["sensor-type"] not in self._sensor_type_list.keys():
            self._logger.error("Wrong parameter. Value for 'sensor-type': {} is not in list of accepted values {}.".
                               format(self._config["sensor-type"], self._sensor_type_list.keys()))
            raise ValueError("Wrong parameter. Value for 'sensor-type': {} is not in list of accepted values {}.".
                             format(self._config["sensor-type"], self._sensor_type_list.keys()))
        self._sensor_type = self._sensor_type_list[self._config["sensor-type"]]

        self._calibrated_t = CalibratedValue(self._logger, self._config["calibration-temperature"], 1)
        self._calibrated_h = CalibratedValue(self._logger, self._config["calibration-humidity"], 1)

    def _poll_device(self):
        """APolling._poll_device"""
        humidity, temperature = None, None
        while humidity is None or temperature is None:
            humidity, temperature = Adafruit_DHT.read_retry(self._sensor_type, self._pin)

        t = self._calibrated_t.value(temperature)
        h = self._calibrated_t.value(humidity)

        self._publish_value(self._topics_pub["temperature"], t)
        self._publish_value(self._topics_pub["humidity"], h)

    def _driver_start(self):
        """ADriver._driver_start"""
        self._start_polling()

    def _driver_stop(self):
        """ADriver._driver_stop"""
        self._stop_polling()

    @classmethod
    def _get_schema(cls):
        return get_schema()


def standalone():
    """Calls the static method DHT.standalone()."""
    DHT.standalone()


if __name__ == "__main__":
    DHT.standalone()