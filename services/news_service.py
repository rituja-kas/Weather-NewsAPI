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
LANGUAGE_MAP = {
    "arabic": "ar",
    "chinese": "zh",
    "dutch": "nl",
    "english": "en",
    "french": "fr",
    "german": "de",
    "greek": "el",
    "hebrew": "he",
    "hindi": "hi",
    "italian": "it",
    "japanese": "ja",
    "malayalam": "ml",
    "marathi": "mr",
    "norwegian": "no",
    "portuguese": "pt",
    "romanian": "ro",
    "russian": "ru",
    "spanish": "es",
    "swedish": "sv",
    "tamil": "ta",
    "telugu": "te",
    "ukrainian": "uk"
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


async def hindi_news(country:str="india",language:str="language",limit:int=5):
    try:
        country_code = COUNTRY_MAP.get(country.lower(),country.lower())
        print("country_code",country_code)
        language_code = LANGUAGE_MAP.get(language.lower(),language.lower())
        print("language_code:",language_code)
        if not language_code:
            raise HTTPException(status_code=400,detail="Language not found in Language Map")
        params = {"country":country_code,"lang":language_code,"max":limit,"token":API_KEY}
        print("parmas:",params)
        response = await async_client.get(News_URL,params=params)
        response.raise_for_status()
        news_response = response.json()
        print("Data fetched",news_response)
        print("keys:",news_response.keys())
        # print("articles_detail",news_response["articles"][0]["lang"])
        articles = news_response.get("articles",[])
        if not articles:
            print(f"No articles found for language '{language_code}' Message from API"),
            news_response.get("information",[])
            return "success but no article found"
        print("articles:",articles)
        print(f"Fetched {len(articles)} articles in language '{language_code}'")
        for article in articles:
            article["language"] = language_code
        return articles
    except httpx.TimeoutException:
        raise HTTPException(status_code=504,detail="Timeout Error")
    except httpx.HTTPStatusError:
        raise HTTPException(status_code=502, detail="API failure")


async def news_pagination(country:str="country",language:str="language"):
    try:
        language_code = LANGUAGE_MAP.get(language.lower(),language.lower())
        country_code = COUNTRY_MAP.get(language.lower(),language.lower())
        params = {"country":country_code,"lang":language_code,"token":API_KEY}
        if not language_code:
            raise HTTPException(status_code=400,detail="Language not found in Language Map")

        response = await async_client.get(News_URL,params=params)
        response.raise_for_status()
        news_response = response.json()
        articles = news_response.get("articles",[])

        LANGUAGE_MAP[language] = language
        # start_index = (page-1)*page_size
        # end_index = start_index + page_size
        # paginated_articles = articles[start_index:end_index]
        return {
            # "page":page,
            # "page_size":page_size,
            "total_articles":len(articles),
            "articles":articles,
        }
    except httpx.TimeoutException:
        raise HTTPException(status_code=504,detail="Timeout Error")
    except httpx.HTTPStatusError:
        raise HTTPException(status_code=502, detail="API failure")





