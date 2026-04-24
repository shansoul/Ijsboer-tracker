from pydantic import BaseModel


class LocationResponse(BaseModel):
    lat: float
    lng: float
    updated_at: str
    is_active: bool
