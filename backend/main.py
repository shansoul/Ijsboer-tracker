import math
from datetime import datetime

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from models import LocationResponse
from storage import get_location, save_location, save_location_inactive

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://shansoul.github.io", "https://ijsvantijs.nl", "https://www.ijsvantijs.nl"],
    allow_methods=["GET", "POST"],
)


@app.post("/api/location")
def update_location(lat: float, lng: float):
    save_location(lat, lng)
    return {"status": "ok"}


@app.post("/api/location/stop")
def stop_tracking():
    save_location_inactive()
    return {"status": "stopped"}


@app.get("/api/location", response_model=LocationResponse)
def get_current_location():
    return get_location()


@app.get("/api/location/test", response_model=LocationResponse)
def test_location():
    # Beweegt in cirkel — voor webteam om kaart te testen zonder echte rit
    t = datetime.utcnow().second / 60 * 2 * math.pi
    return LocationResponse(
        lat=52.3676 + math.sin(t) * 0.002,
        lng=4.9041 + math.cos(t) * 0.002,
        updated_at=datetime.utcnow().isoformat(),
        is_active=True,
    )
