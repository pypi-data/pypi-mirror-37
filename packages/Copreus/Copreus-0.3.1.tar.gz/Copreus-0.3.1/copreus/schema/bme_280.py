import copreus.schema.adriver as adriver
import copreus.schema.apolling as apolling
import copreus.schema.calibratedvalue as calibratedvalue


def _add_schema_part(schema, schema_part):
    schema["device"]["required"].extend(schema_part["required"])
    schema["device"]["properties"].update(schema_part["properties"])


def get_schema():
    driver_specific_properties = {
        "port": {
            "description": "i2c port",
            "type": "number"
        },
        "address": {
            "description": "i2c address",
            "type": "number"
        },
    }

    topics_pub = {
        "temperature": "raw temperature",
        "humidity": "raw humidity",
        "pressure": "raw pressure"
    }

    apolling_schema_parts, topics_sub, mqtt_translations = apolling.get_schema_parts()
    schema = adriver.get_schema("bme_280", driver_specific_properties, topics_pub, topics_sub, mqtt_translations)
    _add_schema_part(schema, apolling_schema_parts)
    _add_schema_part(schema, calibratedvalue.get_schema_parts("calibration-temperature"))
    _add_schema_part(schema, calibratedvalue.get_schema_parts("calibration-humidity"))
    _add_schema_part(schema, calibratedvalue.get_schema_parts("calibration-pressure"))

    return schema
