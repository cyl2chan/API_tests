FORECAST_SCHEMA = {
    "type": "object",
    "required": ["latitude", "longitude", "timezone", "hourly", "hourly_units"],
    "properties": {
        "latitude": {"type": "number", "minimum": -90, "maximum": 90},
        "longitude": {"type": "number", "minimum": -180, "maximum": 180},
        "elevation": {"type": "number"},
        "utc_offset_seconds": {"type": "number"},
        "timezone": {"type": "string"},
        "timezone_abbreviation": {"type": "string"},
        "hourly_units": {
            "type": "object",
            "required": ["time", "temperature_2m"],
            "properties": {
                "time": {"type": "string"},
                "temperature_2m": {"type": "string"},
            },
        },
        "hourly": {
            "type": "object",
            "required": ["time", "temperature_2m"],
            "properties": {
                "time": {"type": "array", "items": {"type": "string"}, "minItems": 1},
                "temperature_2m": {
                    "type": "array",
                    "items": {"type": ["number", "null"]},
                    "minItems": 1,
                },
            },
        },
    },
}
