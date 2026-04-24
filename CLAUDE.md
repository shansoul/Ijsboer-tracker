IJsboer Tracker — CLAUDE.md
Waarom dit project
Een lokale ijsboer rijdt elke zaterdag een vaste route door de wijk. Zijn klanten weten niet
precies wanneer hij bij hen in de straat is. Hij wil een live tracker op zijn website zodat
mensen kunnen zien waar hij nu is.
Een Belgisch IT-bedrijf heeft dit eerder geprobeerd en het opgegeven. De oplossing is
echter eenvoudig als je de operationele realiteit centraal stelt: de ijsboer is niet tech-savvy,
dus de tool moet zero-maintenance zijn voor hem.
Dit project is gebouwd als een eerste AI consultancy case — klein, afgebakend, en volledig
productie-ready na Fase 1.
Architectuur overzicht
[PWA op telefoon ijsboer] → [FastAPI backend] → [Website bezoekers]
Stuurt GPS elke 30s Slaat positie op Leaflet.js kaart embed
Start/Stop knop REST API Polt elke 30s
File structuur
ijsboer-tracker/
│
├── backend/
│ ├── main.py # FastAPI app, alle endpoints
│ ├── models.py # Pydantic LocationResponse schema
│ ├── storage.py # In-memory locatie opslag (MVP)
│ └── requirements.txt # fastapi, uvicorn, pydantic
│
├── pwa/
│ ├── index.html # Start/Stop UI voor ijsboer
│ └── app.js # GPS uitlezen + sturen naar backend
│
└── docs/
└── website-integratie.md # Instructies + snippet voor webteam ijsboer
Fase 1 — MVP (nu bouwen)
Doel
Volledig werkende tracker die productie-ready is:
IJsboer opent PWA in browser → drukt Start → pin verschijnt op kaart
Pin update elke 30 seconden live
IJsboer drukt Stop aan einde rit → pin verdwijnt van kaart
Webteam van ijsboer integreert kaart via copy-paste HTML snippet
Backend — FastAPI
models.py
from pydantic import BaseModel
class LocationResponse(BaseModel):
lat: float
lng: float
updated_at: str
is_active: bool # False = niet onderweg, True = rijdt nu
storage.py
from datetime import datetime
from models import LocationResponse
# In-memory opslag — verdwijnt bij herstart, voldoende voor MVP
_current_location: LocationResponse = LocationResponse(
lat=0.0,
lng=0.0,
updated_at=datetime.utcnow().isoformat(),
is_active=False
)
def save_location(lat: float, lng: float):
global _current_location
_current_location = LocationResponse(
lat=lat,
lng=lng,
updated_at=datetime.utcnow().isoformat(),
is_active=True
)
def save_location_inactive():
global _current_location
_current_location = LocationResponse(
lat=_current_location.lat,
lng=_current_location.lng,
updated_at=datetime.utcnow().isoformat(),
is_active=False # Pin verdwijnt op de kaart
)
def get_location() -> LocationResponse:
return _current_location
main.py
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from models import LocationResponse
from storage import save_location, save_location_inactive, get_location
import math
from datetime import datetime
app = FastAPI()
# CORS: sta toe dat de website van de ijsboer de API aanroept
# Vervang "*" met het echte domein zodra bekend
app.add_middleware(
CORSMiddleware,
allow_origins=["*"],
allow_methods=["GET", "POST"],
)
@app.post("/api/location")
def update_location(lat: float, lng: float):
# PWA stuurt elke 30s de huidige GPS positie hierheen
save_location(lat, lng)
return {"status": "ok"}
@app.post("/api/location/stop")
def stop_tracking():
# IJsboer drukt Stop — pin verdwijnt van de kaart
save_location_inactive()
return {"status": "stopped"}
@app.get("/api/location", response_model=LocationResponse)
def get_current_location():
# Kaart embed polt dit endpoint elke 30s
return get_location()
@app.get("/api/location/test", response_model=LocationResponse)
def test_location():
# Beweegt in cirkel — voor webteam om kaart te testen zonder echte rit
t = datetime.utcnow().second / 60 * 2 * math.pi
return LocationResponse(
lat=52.3676 + math.sin(t) * 0.002,
lng=4.9041 + math.cos(t) * 0.002,
updated_at=datetime.utcnow().isoformat(),
is_active=True
)
requirements.txt
fastapi
uvicorn
pydantic
Server starten:
uvicorn main:app --reload
PWA — Voor de ijsboer (pwa/)
index.html + app.js — nog te bouwen. Gedrag:
Simpele pagina, grote Start knop
Na drukken: Start wordt Stop, GPS polling begint (elke 30s POST naar /api/location )
Na Stop drukken: POST naar /api/location/stop , knop wordt weer Start
Werkt in Safari (iPhone) en Chrome (Android) — geen app store nodig
Browser vraagt eenmalig toestemming voor locatie
Kaart embed — Voor het webteam (docs/)
Geef hen dit HTML snippet + instructies:
<!-- IJsboer Tracker - paste this where you want the map to appear -->
<div id="ijsboer-map" style="height: 400px; width: 100%; border-radius: 8px;"></div>
<link rel="stylesheet" href="https://unpkg.com/leaflet@1.9.4/dist/leaflet.css" />
<script src="https://unpkg.com/leaflet@1.9.4/dist/leaflet.js"></script>
<script>
const API_URL = "https://JOUW_DOMEIN/api/location"; // ← aanpassen
const POLL_INTERVAL = 30000;
const map = L.map("ijsboer-map").setView([52.3676, 4.9041], 15); // ← coördinaten aanpassen
L.tileLayer("https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png", {
attribution: "© OpenStreetMap contributors"
}).addTo(map);
const ijsjesIcon = L.divIcon({
html: " ",
className: "",
iconSize: [30, 30],
iconAnchor: [15, 15]
});
let marker = null;
let statusBanner = null;
async function updateLocation() {
try {
const response = await fetch(API_URL);
const data = await response.json();
if (!data.is_active) {
showStatus("De ijsboer is vandaag nog niet onderweg.");
if (marker) { marker.remove(); marker = null; }
return;
}
const pos = [data.lat, data.lng];
if (!marker) {
marker = L.marker(pos, { icon: ijsjesIcon }).addTo(map);
} else {
marker.setLatLng(pos);
}
Wat het webteam moet aanpassen:
1. API_URL → jouw echte backend URL
2. setView([52.3676, 4.9041], 15) → coördinaten van de wijk van de ijsboer
Voor testen zonder echte rit: verander API_URL tijdelijk naar /api/location/test — de
pin beweegt dan automatisch in een cirkel.
Belangrijk: geef hen jouw domeinnaam zodat je CORS correct instelt ( allow_origins ).
Hosting (gratis)
Component Platform Kosten
FastAPI backend Railway of Render Gratis tier
PWA voor ijsboer GitHub Pages Gratis
map.panTo(pos);
hideStatus();
} catch (error) {
showStatus("Locatie tijdelijk niet beschikbaar.");
}
}
function showStatus(msg) {
if (!statusBanner) {
statusBanner = document.createElement("p");
statusBanner.style.textAlign = "center";
statusBanner.style.marginTop = "8px";
document.getElementById("ijsboer-map").after(statusBanner);
}
statusBanner.textContent = msg;
}
function hideStatus() {
if (statusBanner) statusBanner.textContent = "";
}
updateLocation();
setInterval(updateLocation, POLL_INTERVAL);
</script>
Domeinnaam — Niet nodig voor MVP
Fase 2 — Voorspelde aankomsttijd (later)
Aanpak
1. Eerste weken: GPS-traces loggen naar database (PostgreSQL of SQLite)
2. Na ~4 zaterdagen: historische patronen zichtbaar (om 10:15 altijd bij straat X)
3. Huidige positie matchen aan historische route → verwachte tijd per stopplaats
berekenen
4. Tonen op kaart: “Verwacht in uw straat om ±10:45”
Wat er dan bij komt
Database voor het opslaan van ritten (SQLite voor MVP Fase 2)
Route-matching algoritme (geen ML nodig, gewoon interpolatie op tijdreeksdata)
UI update: popup per wijk/straat met verwachte tijd
Nog niet bouwen — eerst Fase 1 volledig werkend en getest