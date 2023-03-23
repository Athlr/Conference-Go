from .keys import PEXELS_API_KEY, OPEN_WEATHER_API_KEY
import json
import requests

# Use Pexels API


def get_photo(city, state):
    pexels_url = "https://api.pexels.com/v1/search"
    pexels_params = {"per_page": 1, "query": f"{city} {state}"}
    pexels_header = {
        "Authorization": PEXELS_API_KEY,
    }
    pexels_r = requests.get(
        pexels_url,
        headers=pexels_header,
        params=pexels_params,
    )
    pexels_content = json.loads(pexels_r.content)
    try:
        return {"picture_url": pexels_content["photos"][0]["src"]["original"]}
    except (KeyError, IndexError):
        return {"picture_url": None}


# Use Open Weather API


def get_weather_data(city, state):

    geocoding_url = "http://api.openweathermap.org/geo/1.0/direct"
    geocoding_params = {
        "q": f"{city},{state},US",
        "appid": OPEN_WEATHER_API_KEY,
        "limit": 1,
    }
    geocoding_r = requests.get(
        geocoding_url,
        params=geocoding_params,
    )
    geocoding_content = json.loads(geocoding_r.content)
    longitude = geocoding_content[0]["lon"]
    latitude = geocoding_content[0]["lat"]

    open_weather_url = "https://api.openweathermap.org/data/2.5/weather"
    open_weather_params = {
        "lat": latitude,
        "lon": longitude,
        "appid": OPEN_WEATHER_API_KEY,
        "lang": "en",
    }
    open_weather_r = requests.get(open_weather_url, params=open_weather_params)
    open_weather_content = json.loads(open_weather_r.content)
    try:
        return {
            "weather": {
                "temp": open_weather_content["main"]["temp"],
                "description": open_weather_content["weather"][0][
                    "description"
                ],
            }
        }
    except Exception:
        return {"weather": None}
