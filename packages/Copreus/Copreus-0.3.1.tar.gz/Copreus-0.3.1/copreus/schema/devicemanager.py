import copreus.schema.adc
import copreus.schema.bme_280
import copreus.schema.dac
import copreus.schema.dht
import copreus.schema.epaperdirect
import copreus.schema.epapersimple
import copreus.schema.input
import copreus.schema.output
import copreus.schema.rotaryencoder


def _add_device_schema(schema, device_schema):
    device_schema["device"]["properties"]["active"] = {
        "description": "if set to false, the driver will not be loaded",
        "type": "boolean"
    }
    device_schema["device"]["required"].append("name")
    device_schema["device"]["required"].append("active")
    schema["devices"]["items"]["oneOf"].append(device_schema["device"])


def get_schema():
    schema = {
                "devices": {
                    "description": "Devicemanager configuration.",
                    "type": "array",
                    "items": {
                        "oneOf": [
                        ]
                    },
                    "additionalItems": False
                }
            }

    _add_device_schema(schema, copreus.schema.adc.get_schema())
    _add_device_schema(schema, copreus.schema.bme_280.get_schema())
    _add_device_schema(schema, copreus.schema.dac.get_schema())
    _add_device_schema(schema, copreus.schema.dht.get_schema())
    _add_device_schema(schema, copreus.schema.epaperdirect.get_schema())
    _add_device_schema(schema, copreus.schema.epapersimple.get_schema())
    _add_device_schema(schema, copreus.schema.input.get_schema())
    _add_device_schema(schema, copreus.schema.output.get_schema())
    _add_device_schema(schema, copreus.schema.rotaryencoder.get_schema())

    return schema

