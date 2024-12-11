import fastapi
from typing import Optional
from fastapi.params import Depends
from sqlalchemy.orm import Session

from infra.database import get_db
from models.ValidationError import ValidationError
from models.location import Location
from schemas.report_schemas import ReportUpdateRequest
from schemas.weather_schemas import WeatherSchema
from services import openweather_service, report_service
from services.auth_service import get_current_user
from services.report_service import get_all_weather

router = fastapi.APIRouter(
    prefix="/api/v1/weather",
    tags=["weather"]
)


@router.get("/", name="Test external API")
async def weather(location: Location = Depends(), units: Optional[str] = 'metric'):
    try:
        return await openweather_service.get_report_async(
            location.city, location.state, location.country, units
        )
    except ValidationError as ve:
        return fastapi.Response(content=ve.error_msg, status_code=ve.status_code)


@router.get("/reports", name="Get all weather reports")
def get_reports(db: Session = Depends(get_db)):
    return get_all_weather(db)


@router.post("/reports", status_code=201, dependencies=[Depends(get_current_user)])
async def add_report(
        location: Location = Depends(),
        units: Optional[str] = 'metric',
        db: Session = Depends(get_db)
):
    try:
        weather_data = await openweather_service.get_report_async(
            location.city, location.state, location.country, units
        )

        new_weather_report = WeatherSchema(
            city=location.city,
            temperature=str(weather_data['temp'])
        )

        return await report_service.add_report(
            new_weather_report,
            db,
        )

    except ValidationError as ve:
        return fastapi.Response(content=ve.error_msg, status_code=ve.status_code)


@router.put("/reports/{report_id}", dependencies=[Depends(get_current_user)])
async def update_report(
    report_id: int,
    updated_report: ReportUpdateRequest,
    db: Session = Depends(get_db),
):
    existing_report = await report_service.get_report(report_id, db)
    if not existing_report:
        raise ValidationError(status_code=404, error_msg="Report not found")

    try:
        weather_data = await openweather_service.get_report_async(
            updated_report.city, updated_report.state, updated_report.country, updated_report.units
        )
        updated_weather_report = WeatherSchema(
            city=updated_report.city,
            temperature=str(weather_data['temp'])
        )
        return await report_service.update_report(report_id, updated_weather_report, db)
    except ValidationError as ve:
        return fastapi.Response(content=ve.error_msg, status_code=ve.status_code)


@router.delete("/reports/{report_id}", status_code=204, dependencies=[Depends(get_current_user)])
async def delete_report(
    report_id: int,
    db: Session = Depends(get_db),
):
    report = await report_service.get_report(report_id, db)
    if not report:
        raise ValidationError(status_code=404, error_msg="Report not found")

    await report_service.delete_report(report_id, db)
    return {"detail": "Report deleted successfully"}