import argaeus.schema.setpointcontroller
import argaeus.schema.operationcontroller
import argaeus.schema.modecontroller


def add_property(properties, required, sub_schema):
    for key, value in sub_schema.items():
        properties[key] = value
        required.append(key)
    return properties, required


def get_schema():
    properties = {}
    required = []

    properties, required = add_property(properties, required, argaeus.schema.setpointcontroller.get_schema())
    properties, required = add_property(properties, required, argaeus.schema.operationcontroller.get_schema())
    properties, required = add_property(properties, required, argaeus.schema.modecontroller.get_schema())

    schema = {
        "controller": {
            "description": "Argaeus is the gui controller element for a thermostat.",
            "type": "object",
            "properties": properties,
            "required": required,
            "additionalProperties": False
        }
    }

    return schema
