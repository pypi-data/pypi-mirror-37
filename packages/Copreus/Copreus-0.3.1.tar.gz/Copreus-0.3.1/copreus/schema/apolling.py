def get_schema_parts():
    schema = {
        "properties": {
            "poll-interval": {
                "description": "poll time in seconds"
            },
        },
        "required": ["poll-interval"],
    }

    topics_sub = {
        "poll-now": "listen to this topic to start spontaneus polling"
    }

    mqtt_translations = {
        "poll-now": "command that starts spontaneus polling"
    }

    return schema, topics_sub, mqtt_translations

