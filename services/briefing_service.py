import asyncio
from fastapi import HTTPException
from services.weather_service import get_weather
from services.news_service import get_news


async def get_dailybriefing(city:str):

    weather_data = None
    news_data = None
    warnings = []

    weather_task = asyncio.create_task(get_weather(city))
    news_task = asyncio.create_task(get_news())

    results = await asyncio.gather(weather_task,news_task,return_exceptions=True)

    # for handling weather result
    if isinstance(results[0],Exception):
        warnings.append(results[0])
    else:
        weather_data = results[0]

    # for handling news result
    if isinstance(results[1],Exception):
        warnings.append(results[1])
    else:
        news_data = results[1]

    # if we both fail
    if not weather_data and not news_data:
        raise HTTPException(status_code=502, detail="Both Services Failed")
    return {
        "weather":weather_data,
        "news":news_data
    }