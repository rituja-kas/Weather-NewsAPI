from fastapi import FastAPI, HTTPException, status, Request
import aiohttp
import asyncio

from schemas import news, weather
from services.weather_service import get_weather
from services.news_service import get_news
from services.briefing_service import get_dailybriefing

# app connected with the server
app = FastAPI()


# test api
@app.get("/")
async def root():
    return {"message": "Hello World"}

# weather api
@app.get("/weather/{city}")
async def weather(city: str):
    return await get_weather(city)


# news api
@app.get("/news")
async def news(country: str="india",limit: int=5):
    return await get_news(country=country,limit=limit)


# Daily Briefing Endpoint
@app.get("/briefing/city")
async def briefing(city: str):
    return await get_dailybriefing(city)

