from sqlalchemy import literal
from sqlalchemy.orm import Session
from models.reports import  WeatherData
from schemas.weather_schemas import WeatherSchema

async def get_report(report_id: int, db: Session):
    return db.query(WeatherData).filter(WeatherData.id.__eq__(literal(report_id))).first()


async def add_report(weather: WeatherSchema, db: Session):
    db_weather = WeatherData(
        city=weather.city,
        temperature=weather.temperature,
    )
    db.add(db_weather)
    db.commit()
    db.refresh(db_weather)
    return db_weather


def get_all_weather(db: Session):
    return db.query(WeatherData).all()


async def update_report(report_id: int, updated_report: WeatherSchema, db: Session):
    db_report = db.query(WeatherData).filter(WeatherData.id.__eq__(literal(report_id))).first()
    if not db_report:
        return None

    db_report.city = updated_report.city
    db_report.temperature = updated_report.temperature
    db.commit()
    db.refresh(db_report)
    return db_report


async def delete_report(report_id: int, db: Session):
    db_report = db.query(WeatherData).filter(WeatherData.id.__eq__(literal(report_id))).first()
    if db_report:
        db.delete(db_report)
        db.commit()