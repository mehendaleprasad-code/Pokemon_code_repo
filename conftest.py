from jsonschema import validate

def validate_response(response):
    return response.status_code == 200

def validate_pokemon_schema(response_data):
    """
    Reusable schema validation function
    """
    pokemon_schema = {
        "type": "object",
        "properties": {
            "name": {"type": "string"},
            "abilities": {"type": "array"}
        },
        "required": ["name", "abilities"]
    }

    validate(
        instance=response_data,
        schema=pokemon_schema
    )

