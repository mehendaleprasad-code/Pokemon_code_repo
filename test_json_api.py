# check the URL is working and we are getting 200 OK
"""
Status Code Assertion

Performance Validation (SLA: Response should be under 1.5 seconds) - timeout factor
Core Data Assertions
Nested JSON/List Validation (Assert 'limber' is one of Ditto's abilities)

Parameterization (Data-Driven Testing for Multiple Pokémon)

add 4 more pokeman and get report properly
add new cases for errors
upload it to git and share the link
"""
import requests
import pytest
import time
from jsonschema import validate
from jsonschema.exceptions import ValidationError

from conftest import validate_response, validate_pokemon_schema


BASE_URL = "https://pokeapi.co/api/v2/pokemon"


@pytest.mark.parametrize("pokemon_name", ["ditto", "bulbasaur", "wartortle", "metapod", "weedle"])
def test_json_api(pokemon_name):
    start_time = time.time()

    try:
        newurl = f"{BASE_URL}/{pokemon_name}"

        # Validating API performance:
        # If a Pokémon API response exceeds the defined timeout, the test will fail;
        # otherwise, it will pass.
        if pokemon_name == "metapod":
            response = requests.get(newurl, timeout=.02)
        else:
            response = requests.get(newurl, timeout=5)

        # Validate the response i.e. url is working
        assert validate_response(response), "Site is not accessible"
        json_data = response.json()

        # Validate abilities present
        assert len(json_data["abilities"]) > 0

        # validating at least 1 ability is present for the selected pokemon
        # ability for ditto is changed, so that it will fail. to address the failure scenario
        abilities = ["limber22", "overgrow", "shed-skin", "torrent", "shield-dust"]
        pokemon_ability = json_data["abilities"][0]["ability"]["name"]
        assert pokemon_ability in abilities, f"Ability not found for {pokemon_name}"

        # Schema validation
        validate_pokemon_schema(json_data)

    except requests.exceptions.Timeout:
        end_time = time.time()
        assert False, f"Request timed out. It took {start_time - end_time} seconds to load"
