# Website Integratie — IJsboer Tracker

Plak het onderstaande HTML-snippet op de plek waar de kaart moet verschijnen.

## Wat je moet aanpassen

1. **`setView([52.3676, 4.9041], 15)`** → vervang de coördinaten met de wijk van de ijsboer

## HTML Snippet

```html
<!-- IJsboer Tracker - plak dit waar de kaart moet komen -->
<div id="ijsboer-map" style="height: 400px; width: 100%; border-radius: 8px;"></div>
<link rel="stylesheet" href="https://unpkg.com/leaflet@1.9.4/dist/leaflet.css" />
<script src="https://unpkg.com/leaflet@1.9.4/dist/leaflet.js"></script>
<script>
const API_URL = "https://ijsboer-tracker-production.up.railway.app/api/location";
const POLL_INTERVAL = 30000;

const map = L.map("ijsboer-map").setView([52.3676, 4.9041], 15); // ← coördinaten aanpassen

L.tileLayer("https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png", {
  attribution: "© OpenStreetMap contributors"
}).addTo(map);

const ijsbusIcon = L.icon({
  iconUrl: "https://shansoul.github.io/ijsboer-tracker/Ijsbus.png",
  iconSize: [116, 66],
  iconAnchor: [58, 66]
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
      marker = L.marker(pos, { icon: ijsbusIcon }).addTo(map);
    } else {
      marker.setLatLng(pos);
    }
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
```

## Testen zonder echte rit

Verander `API_URL` tijdelijk naar:

```
https://ijsboer-tracker-production.up.railway.app/api/location/test
```

De ijsbus beweegt dan automatisch in een cirkel — zo kan het webteam de kaart testen zonder dat de ijsboer hoeft te rijden.

## CORS

De backend staat ingesteld om verzoeken toe te staan van:
- `https://ijsvantijs.nl`
- `https://www.ijsvantijs.nl`
- `https://shansoul.github.io`

Wil je de kaart op een ander domein embedden, meld dit dan aan de beheerder.
