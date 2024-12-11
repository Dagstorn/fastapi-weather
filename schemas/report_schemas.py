from typing import Optional

from pydantic import BaseModel


class ReportUpdateRequest(BaseModel):
    city: str
    country: str
    state: Optional[str] = None
    units: Optional[str] = 'metric'
