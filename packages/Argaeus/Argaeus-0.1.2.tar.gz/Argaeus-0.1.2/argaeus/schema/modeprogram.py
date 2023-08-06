def get_schema():
    schema = {
        "description": "program entry",
        "type": "object",
        "properties": {
            "name": {
                "description": "unique name for mode entry",
                "type": "string"
            },
            "type": {
                "description": "type - must be 'program'",
                "type": "string",
                "enum": ["program"]
            },
            "selectable": {
                "description": "can be selected using the gui",
                "type": "boolean"
            },
            "set-point": {
                "description": "target temperature of this mode",
                "type": "number"
            }
        },
        "required": ["name", "type", "selectable", "set-point"],
        "additionalItems": False

    }

    return schema
