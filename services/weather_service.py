from fastapi import HTTPException
import httpx
from utils.http_client import async_client


GEOCODE_URL = "https://geocoding-api.open-meteo.com/v1/search"
WEATHER_URL = "https://api.open-meteo.com/v1/forecast"


WEATHER_CODE_MAP ={
    0:"clear-sky",
    1:"Main clear",
    2:"Partly cloudy",
    3:"Cloudy",
    45:"Fog",
    48:"Freezing fog",
    51:"Drizzle",
    53:"Moderate drizzle",
    55:"High Drizzle",
    56:"Freezing Drizzle",
    57:"High Freezing Drizzle",
    61:"light Rain",
    63:"Moderate Rain",
    65:"High Rain",
    66:"Freezing Rain",
    67:"Freezing Rain with High Intensity",
    71:"light Snowfall",
    73:"Moderate Snowfall",
    75:"High Snowfall",
    77:"Snow grains",
    80:"Light Rain Showers",
    81:"Moderate Rain Showers",
    82:"High Rain Showers",
    85:"Snow showers light",
    86:"Moderate snow showers",
    95:"Thunderstorm",
    96:"Thunderstorm with light hail",
    99:"Thunderstorm with high hail",
}

async def get_weather(city:str):
    try:
        geo_response = await async_client.get(GEOCODE_URL,params={"name":city})
        geo_response.raise_for_status()
        geo_data = geo_response.json()
        print("geo dataaaaaaaaaaaaaaaaaaaaa",geo_data.keys())
        if "results" not in  geo_data or not geo_data["results"]:
            raise HTTPException(status_code=404, detail="City not found")

        location = geo_data["results"][0]
        print(f"location detail: {location}, latitude: {location['latitude']}, longitude: {location['longitude']}")
        # get weather using co-ordinates
        weather_response = await async_client.get(WEATHER_URL,params={"latitude":location["latitude"],"longitude":location["longitude"],"current_weather":True,},)
        weather_response.raise_for_status()
        weather_data = weather_response.json()

        print(f"weather data:{weather_data}")

        current = weather_data.get("current_weather")
        if not current:
            raise HTTPException(status_code=502, detail="Weather Service failure")

        temperature = current["temperature"]
        weather_code = current["weathercode"]
        condition = WEATHER_CODE_MAP[weather_code]

        result = {
            "city":location["name"],
            "temperature":temperature,
            "condition":condition,
        }
        print("resulttttttttttt",result)
        return result
    except httpx.TimeoutException:
        raise HTTPException(status_code=504, detail="Timeout exception")
    except httpx.HTTPStatusError:
        raise HTTPException(status_code=502, detail="Weather Service failure")
    except httpx.RequestError:
        raise HTTPException(status_code=502, detail="Weather Service failure")

