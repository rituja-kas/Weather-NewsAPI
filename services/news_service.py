from fastapi import HTTPException
import httpx
from utils.http_client import async_client
from dotenv import load_dotenv
import os

load_dotenv()

News_URL = "https://gnews.io/api/v4/top-headlines"
API_KEY = os.getenv("NEWS_API_KEY")


COUNTRY_MAP = {
    "india": "in",
    "united states": "us",
    "uk": "gb",
    "britain": "gb",
}

async def get_news(country:str = "india",limit:int=5):
    print(API_KEY)
    try:
        new_country = COUNTRY_MAP.get(country.lower(),country.lower())
        response = await async_client.get(News_URL,params={"country":new_country,"max":limit,"token":API_KEY}, timeout=10.0)
        print("responseeeeeeeeeee",response)
        print("params:",{
            "country":new_country,
            "max":limit,
            "token":API_KEY
        })
        response.raise_for_status()
        news_response = response.json()
        print("response",news_response)
        articles = news_response.get("articles")
        if not articles:
            raise HTTPException(status_code=502,detail="No news found")
        headlines = [article["title"] for article in articles]
        return headlines
    except httpx.TimeoutException:
        raise HTTPException(status_code=504, detail="Timeout Error")
    except httpx.HTTPStatusError:
        raise HTTPException(status_code=502, detail="API failure")




