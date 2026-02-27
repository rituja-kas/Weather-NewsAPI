from pydantic import BaseModel


class WeatherResponse(BaseModel):
    city_name: str
    temperature: float
    condition: str