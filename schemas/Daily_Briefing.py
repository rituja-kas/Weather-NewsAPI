from pydantic import BaseModel
from news import NewsResponse
from weather import WeatherResponse

class DailyBriefing(BaseModel):
    weather: WeatherResponse
    news: NewsResponse

