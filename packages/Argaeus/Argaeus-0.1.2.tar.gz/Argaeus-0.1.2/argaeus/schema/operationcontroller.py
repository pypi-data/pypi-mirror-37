def get_schema():
    schema = {
        "operation-controller": {
            "description": "turns the outgoing relais on/off",
            "type": "object",
            "properties": {
                "default-is-active": {
                    "description": "Is the controller active or passive initially",
                    "type": "boolean"
                },
                "topic-pub": {
                    "description": "Topic that controls the output behavior relais of the thermostat.",
                    "type": "string"
                },
                "command-active": {
                    "description": "set to active command - publish this value to topic-pub, to set the controller"
                                   "to active operation.",
                    "type": "string"
                },
                "command-passive": {
                    "description": "set to passive command - publish this value to topic-pub, to set the controller"
                                   "to passive operation.",
                    "type": "string"
                },
                "topic-sub-toggle": {
                    "description": "incoming event to toggle active/passive operation (optional together with "
                                   "command-toggle)",
                    "type": "string"
                },
                "command-toggle": {
                    "description": "command for topic-sub-toggle / toggle active/passive operation (optional "
                                   "together with topic-sub-toggle)",
                    "type": "string"
                }
            },
            "required": ["default-is-active", "topic-pub", "command-active", "command-passive"],
            "additionalProperties": False
        }
    }

    return schema
