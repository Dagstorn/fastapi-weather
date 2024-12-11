from datetime import datetime
from pydantic import BaseModel

class WeatherSchema(BaseModel):
    city: str
    temperature: str

class Weather(WeatherSchema):
    id: int
    created_at: datetime

    class Config:
        from_attributes = True