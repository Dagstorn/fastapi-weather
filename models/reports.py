from sqlalchemy import Column, String, Integer, DateTime
from sqlalchemy.sql import func
from infra.database import Base

class WeatherData(Base):
    __tablename__ = "weather_reports"
    id = Column(
        Integer, primary_key=True, index=True)
    city = Column(String, index=True)
    temperature = Column(String)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
