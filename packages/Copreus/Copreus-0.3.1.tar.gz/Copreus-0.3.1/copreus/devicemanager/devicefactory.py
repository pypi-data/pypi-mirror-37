import copreus.drivers
import importlib
import pelops.mylogger as mylogger


class DeviceFactory:
    @staticmethod
    def create_devices(config, mqtt_client=None, logger=None, spi_lock=None):
        """Static devices factory - takes a list of device configs and creates them."""

        factory_logger = mylogger.get_child(logger, __name__)
        factory_logger.info("creating devices")
        factory_logger.debug("device configs: ".format(config["devices"]))
        devices = []
        for device_config in config["devices"]:
            if not device_config["active"]:
                continue
            config["device"] = device_config
            device = DeviceFactory.create_device(config, mqtt_client, logger, spi_lock)
            devices.append(device)
            factory_logger.info(" - added device '{}.{}'".format(device._type, device._name))
        return devices


    @staticmethod
    def create_device(config, mqtt_client=None, logger=None, spi_lock=None):
        """Static device factory - takes a device entry from json/yaml config and instantiates the corresponding
        Class. Classes that are specializations of ASPI are provided with the spi_lock (if one is provided to this
        factory).

        New implemented driver must be added manually."""
        type_name = config["device"]["type"].upper()

        # it is on purpose that not class names are used to be compared with type_name (as will be done within the
        # constructor of the base class ADriver). This approach allows for late binding - thus, a class is imported
        # if and only if it is needed which results in less dependencies that must be fullfilled although they might
        # not be needed.

        drivers = copreus.drivers.get_drivers()

        try:
            driver = drivers[type_name]
            mod = importlib.import_module(driver["module"])
            klass = getattr(mod, driver["name"])
            if "ASPI" in driver["bases"]:
                result = klass(config, mqtt_client, logger, spi_lock)
            else:
                result = klass(config, mqtt_client, logger)
        except:
            logger = mylogger.get_child(logger, __name__)
            logger.error("unknown type name '{}'.".format(type_name))
            raise ValueError("unknown type name '{}'.".format(type_name))

        return result

    @staticmethod
    def old_create(config, mqtt_client, logger, spi_lock=None):
        type_name = config["type"].upper()
        if type_name == "ADC":
            from copreus.drivers.adc import ADC
            result = ADC(config, mqtt_client, logger, spi_lock)
        elif type_name == "DAC":
            from copreus.drivers.dac import DAC
            result = DAC(config, mqtt_client, logger, spi_lock)
        elif type_name == "BME_280":
            from copreus.drivers.bme_280 import BME_280
            result = BME_280(config, mqtt_client, logger)
        elif type_name == "DHT":
            from copreus.drivers.dht import DHT
            result = DHT(config, mqtt_client, logger)
        elif type_name == "EPAPERDIRECT":
            from copreus.drivers.epaperdirect import EPaperDirect
            result = EPaperDirect(config, mqtt_client, logger, spi_lock)
        elif type_name == "EPAPERSIMPLE":
            from copreus.drivers.epapersimple import EPaperSimple
            result = EPaperSimple(config, mqtt_client, logger, spi_lock)
        elif type_name == "INPUT":
            from copreus.drivers.input import Input
            result = Input(config, mqtt_client, logger)
        elif type_name == "OUTPUT":
            from copreus.drivers.output import Output
            result = Output(config, mqtt_client, logger)
        elif type_name == "ROTARYENCODER":
            from copreus.drivers.rotaryencoder import RotaryEncoder
            result = RotaryEncoder(config, mqtt_client, logger)
        else:
            logger = mylogger.get_child(logger, __name__)
            logger.error("unknown type name '{}'.".format(type_name))
            raise ValueError("unknown type name '{}'.".format(type_name))

        return result


