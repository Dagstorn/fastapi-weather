import httpx
from httpx import Response
from typing import Optional, Tuple

from infra import weather_cache
from models.ValidationError import ValidationError

API_KEY: Optional[str] = None


async def get_report_async(
        city: str,
        state: Optional[str],
        country: str,
        units: str
) -> dict:
    city, state, country, units = validate_units(city, state, country, units)
    forecast = weather_cache.get_weather(city, state, country, units)

    if forecast:
        return forecast

    if state:
        q = f'{city},{state},{country}'
    else:
        q = f'{city},{country}'

    url = f"https://api.openweathermap.org/data/2.5/weather?q={q}&appid={API_KEY}&units={units}"
    print(url)

    async with httpx.AsyncClient() as client:
        resp: Response = await client.get(url)
        if resp.status_code != 200:
            raise ValidationError(resp.text, status_code=resp.status_code)

    data = resp.json()
    forecast = data['main']

    weather_cache.set_weather(city, state, country, units, forecast)

    return forecast


def validate_units(
    city: str, state: Optional[str], country: Optional[str], units: str
) -> Tuple[str, Optional[str], str, str]:
    city = city.lower().strip()
    if not country:
        error = f'Invalid country: {country}. Country is required.'
        raise ValidationError(status_code=400, error_msg=error)
    else:
        country = country.lower().strip()

    if len(country) != 2:
        error = f'Invalid country: {country}. It must be a two letter abbreviation such as US or KZ.'
        raise ValidationError(status_code=400, error_msg=error)

    if state:
        state = state.strip().lower()

    if state and len(state) != 2:
        error = f'Invalid state: {state}. It must be a two letter abbreviation such as CA or KS (for US only).'
        raise ValidationError(status_code=400, error_msg=error)

    if units:
        units = units.strip().lower()

    valid_units = {'standard', 'metric', 'imperial'}
    if units not in valid_units:
        error = f"Invalid units '{units}', it must be one of {valid_units}."
        raise ValidationError(status_code=400, error_msg=error)

    return city, state, country, units