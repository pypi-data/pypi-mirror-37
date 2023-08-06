def get_schema():
    schema = {
        "setpoint-controller": {
            "description": "changes the set-point of the current program",
            "type": "object",
            "properties": {
                "topic-sub-down": {
                    "description": "reduce temperature topic",
                    "type": "string"
                },
                "command-down": {
                    "description": "down command - if this value is published to topic-sub-down, temp is reduced.",
                    "type": "string"
                },
                "topic-sub-up": {
                    "description": "increase temperature topic",
                    "type": "string"
                },
                "command-up": {
                    "description": "up command - if this value is published to topic-sub-up, temp is increased.",
                    "type": "string"
                },
                "topic-sub-reset": {
                    "description": "incoming event to reset temperature to default (optional together with "
                                   "command-reset)",
                    "type": "string"
                },
                "command-reset": {
                    "description": "command for topic-sub-reset / reset to default (optional together with "
                                   "topic-sub-reset)",
                    "type": "string"
                },
                "step-size": {
                    "description": "Temperature is changed by step size for each rotation step.",
                    "type": "number"
                },
                "max-temp": {
                    "description": "Maximum value for temperature",
                    "type": "number"
                },
                "min-temp": {
                    "description": "Minimum value for temperature",
                    "type": "number"
                },
            },
            "required": ["topic-sub-down", "command-down", "topic-sub-up", "command-up", "step-size",
                         "max-temp", "min-temp"],
            "additionalProperties": False
        }
    }

    return schema
