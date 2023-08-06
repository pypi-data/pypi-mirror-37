def get_schema():
    schema = {
        "description": "schedule entry",
        "type": "object",
        "properties": {
            "name": {
                "description": "unique name for mode entry",
                "type": "string"
            },
            "type": {
                "description": "type - must be 'schedule'",
                "type": "string",
                "enum": ["schedule"]
            },
            "selectable": {
                "description": "can be selected using the rotary encoder",
                "type": "boolean"
            },
            "image": {
                "description": "generate image for nikippe",
                "type": "object",
                "properties": {
                    "width": {
                        "description": "width of image",
                        "type": "integer",
                        "minimum": 0
                    },
                    "height": {
                        "description": "height of image",
                        "type": "integer",
                        "minimum": 0
                    },
                    "foreground-color": {
                        "description": "foreground color",
                        "type": "integer",
                        "minimum": 0,
                        "maximum": 255
                    },
                    "background-color": {
                        "description": "background color",
                        "type": "integer",
                        "minimum": 0,
                        "maximum": 255
                    },
                    "patters": {
                        "description": "each property name must match one program-mode",
                        "type": "object",
                        "patternProperties": {
                            "^.*$": {
                                "description": "0 (draw nothing), 1 (lower dot), 2 (upper dot), 3 (both dots).",
                                "type": "integer",
                                "enum": [0, 1, 2, 3]
                            }
                        },
                    }
                },
                "required": ["width", "height", "foreground-color", "background-color", "patterns"],
                "additionalItems": False
            },
            "schedule": {
                "description": "definition which program is active in each 15 minute slot of a day",
                "type": "object",
                "properties": {},
                "required": [],
                "additionalItems": False
            },

        },
        "required": ["name", "type", "selectable", "image", "schedule"],
        "additionalItems": False
    }

    for hour in range(24):
        for minute in range(0, 60, 15):
            name = "{:02d}:{:02d}".format(hour, minute)
            schema["properties"]["schedule"]["properties"][name] = {
                "description": "Name of active program - must be taken from modes list.",
                "type": "string"
            }
            schema["properties"]["schedule"]["required"].append(name)

    return schema
