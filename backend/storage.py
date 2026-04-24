from datetime import datetime
from models import LocationResponse

_current_location: LocationResponse = LocationResponse(
    lat=0.0,
    lng=0.0,
    updated_at=datetime.utcnow().isoformat(),
    is_active=False,
)


def save_location(lat: float, lng: float):
    global _current_location
    _current_location = LocationResponse(
        lat=lat,
        lng=lng,
        updated_at=datetime.utcnow().isoformat(),
        is_active=True,
    )


def save_location_inactive():
    global _current_location
    _current_location = LocationResponse(
        lat=_current_location.lat,
        lng=_current_location.lng,
        updated_at=datetime.utcnow().isoformat(),
        is_active=False,
    )


def get_location() -> LocationResponse:
    return _current_location
