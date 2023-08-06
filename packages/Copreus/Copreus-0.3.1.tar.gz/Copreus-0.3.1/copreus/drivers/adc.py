from time import sleep
from copreus.baseclasses.adriver import ADriver
from copreus.baseclasses.apolling import APolling
from copreus.baseclasses.aspi import ASPI
from copreus.baseclasses.calibratedvalue import CalibratedValue
from copreus.schema.adc import get_schema


class ADC(ADriver, APolling, ASPI):
    """Driver for ADC (analog-digital-converter) that are connected via spi (e.g. TLC548).

    The driver entry in the yaml file consists of:
      * ADriver entries
        * topics_sub: readnow - mqtt-translations.readnow
        * topics_pub: raw (=integer value returned from adc), volt (=converted and calibrated value)
      * APolling entries
      * ASPI entries
      * CalibratedValue entries in a sub-block named 'calibration'
      * ADC own entries are
        * maxvalue: maximum value in volt. result will be normalized towards this value.
        * bit: how many bits are used. typical values are 8, 10, and 12.

    Example:
    device:
        type: adc
        spi:
            pin_cs: 17
            bus: 0
            device: 1
            maxspeed: 500000
        topics-pub:
            raw: /adc/raw
            volt: /adc/volt
        topics-sub:
            poll-now: /adc/pollnow
        mqtt-translations:
            poll-now: True
        maxvalue: 24
        bit: 8
        poll-interval: 30
        calibration:
            use-calibration: False
            values:
            # - [ref_value, raw_value]
              - [0, 0]
              - [7.2, 6.4]
              - [24, 24]
    """

    _max_value = -1  # maximum value in volt
    _resolution = -1  # 2**bit
    _calibrated_value = None  # copreus.baseclasses.CalibratedValue

    def __init__(self, config, mqtt_client=None, logger=None, spi_lock=None):
        ADriver.__init__(self, config, mqtt_client, logger, logger_name=__name__)
        APolling.__init__(self, self._config, self._mqtt_client, self._logger)
        ASPI.__init__(self, self._config, self._logger, spi_lock)

        self._max_value = float(self._config["maxvalue"])
        self._resolution = 2**int(self._config["bit"])
        self._calibrated_value = CalibratedValue(self._logger, self._config["calibration"],
                                                 self._max_value / float(self._resolution))

    def _poll_device(self):
        """APolling._poll_device"""
        self._transfer([0xFF])[0]  # the adc TLC548 has a two step pipeline -> the first read provides the
                                  # value from the last read. this could be a long time ago.
                                  # -> read twice each time -> digitalization and transfer are
                                  # within a guaranteed short period.
        sleep(0.01)
        raw = self._transfer([0xFF])[0]
        value = self._calibrated_value.value(raw)
        self._publish_value(self._topics_pub["raw"], raw)
        self._publish_value(self._topics_pub["volt"], value)

    def _driver_start(self):
        """ADriver._driver_start"""
        self._connect_spi()
        self._start_polling()

    def _driver_stop(self):
        """ADriver._driver_stop"""
        self._stop_polling()
        self._disconnect_spi()

    @classmethod
    def _get_schema(cls):
        return get_schema()


def standalone():
    """Calls the static method ADC.standalone()."""
    ADC.standalone()


if __name__ == "__main__":
    ADC.standalone()
