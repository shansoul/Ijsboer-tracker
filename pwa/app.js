const API_URL = "http://localhost:8000/api/location"; // ← vervang met jouw backend URL bij deploy
const INTERVAL_MS = 30000;

let actief = false;
let intervalId = null;

const btn = document.getElementById("toggle-btn");
const statusEl = document.getElementById("status");
const coordsEl = document.getElementById("coords");

function toggle() {
  if (!actief) {
    start();
  } else {
    stop();
  }
}

function start() {
  if (!navigator.geolocation) {
    statusEl.textContent = "GPS wordt niet ondersteund door deze browser.";
    return;
  }

  navigator.geolocation.getCurrentPosition(
    (pos) => {
      actief = true;
      btn.textContent = "Stop";
      btn.classList.add("actief");
      statusEl.textContent = "Rit actief — locatie wordt gedeeld.";

      stuurLocatie(pos);
      intervalId = setInterval(() => {
        navigator.geolocation.getCurrentPosition(stuurLocatie, onGpsError, {
          enableHighAccuracy: true,
          timeout: 10000,
        });
      }, INTERVAL_MS);
    },
    onGpsError,
    { enableHighAccuracy: true, timeout: 15000 }
  );

  statusEl.textContent = "GPS ophalen…";
}

function stop() {
  actief = false;
  clearInterval(intervalId);
  intervalId = null;

  btn.textContent = "Start";
  btn.classList.remove("actief");
  coordsEl.textContent = "";
  statusEl.textContent = "Rit beëindigd.";

  fetch(API_URL + "/stop", { method: "POST" }).catch(() => {});
}

function stuurLocatie(pos) {
  const { latitude, longitude } = pos.coords;
  coordsEl.textContent = `${latitude.toFixed(5)}, ${longitude.toFixed(5)}`;

  const url = `${API_URL}?lat=${latitude}&lng=${longitude}`;
  fetch(url, { method: "POST" }).catch(() => {
    statusEl.textContent = "Verbindingsfout — volgende poging over 30s.";
  });
}

function onGpsError(err) {
  statusEl.textContent = "GPS niet beschikbaar: " + err.message;
}
