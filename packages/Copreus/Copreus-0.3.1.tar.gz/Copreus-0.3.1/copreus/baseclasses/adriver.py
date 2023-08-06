from threading import Event
from copreus import version
from pelops.abstractmicroservice import AbstractMicroservice


class ADriver(AbstractMicroservice):
    """Base class that all drivers must implement.

     * Provides MQtt-related functionality like subcribe to topics, publish to topics, start/stop mqtt client.
     * start/stop the service.
     * apply basic configuration from json object
     * standalone enabling methods - each driver can be used on its own from the command line.

    A yaml file must contain two root blocks:
     * mqtt - mqtt-address, mqtt-port, and path to credentials file credentials-file (a file consisting of two entries:
     mqtt-user, mqtt-password)
     * device or devices. devices is a list of device entries with two additional parameters per device: active and
     name. a device entry contains at least (driver implementation might add additional ones): type, name, topic-pub
     (list of key/value pairs), topic-sub (list of key/value pairs), and mqtt-translations (what are the
     commands/states-values that are transmitted via mqtt. only where necessary).
    """

    _version = version

    _topics_pub = None  # list of topics this driver publishes to
    _topics_sub = None  # list of topics this driver listens to
    _type = None  # unique identifier of driver class. usually the class name.
    _name = None  # name of driver instance. should be unique in combination with _type.
    _is_stopped = None  # threading.Event that is true if the driver is not running. False between start() and stop().
    _mqtt_translations = None  # contains all mqtt commands/states and their mqtt.payload representations.

    def __init__(self, config, mqtt_client=None, logger=None, logger_name=None):
        AbstractMicroservice.__init__(self, config, "device", mqtt_client, logger, logger_name)

        self._type = self.__class__.__name__
        if self._type.upper() != self._config["type"].upper():
            self._logger.error("ADriver.__init__ - Type of class ({}) is different than type of config ({}).".format(self._type.upper(), self._config["type"].upper()))
            raise TypeError("Type of class ({}) is different than type of config ({}).".format(self._type.upper(), self._config["type"].upper()))

        try:
            self._name = self._config["name"]
        except KeyError:
            self._name = self._type

        self._topics_pub = {}
        try:
            for k,v in self._config["topics-pub"].items():
                self._topics_pub[k] = v
        except KeyError:
            pass

        self._topics_sub = {}
        try:
            for k,v in self._config["topics-sub"].items():
                self._topics_sub[k] = v
        except KeyError:
            pass

        try:
            self._mqtt_translations = {}
            for k, v in self._config["mqtt-translations"].items():
                self._mqtt_translations[k] = str(v).encode('UTF-8')
        except KeyError:
            pass

        self._is_stopped = Event()
        self._is_stopped.set()

    def _publish_value(self, topic, value):
        """Wrapper method to publish a value to the given topic."""
        self._mqtt_client.publish(topic, value)
        self._logger.info("ADriver._publish_value - {}: {}".format(topic, str(value)))

    @classmethod
    def _get_description(cls):
        return "Device driver for '{}'\n" \
               "In Greek mythology, Copreus (Κοπρεύς) was King Eurystheus' herald. He announced Heracles' Twelve " \
               "Labors. This script starts a device driver on a raspberry pi and connects the device to MQTT. " \
               "Thus, copreus takes commands from the king (MQTT) and tells the hero (Device) what its labors " \
               "are. Further, copreus reports to the king whatever the hero has to tell him.".format(cls.__name__)

    def _start(self):
        """AbstractMicroservice._start"""
        self._driver_start()
        print("Driver '{}.{}' started".format(self._type, self._name))

    def _stop(self):
        """AbstractMicroservice._stop"""
        self._driver_stop()
        print("Driver '{}.{}' stopped".format(self._type, self._name))
