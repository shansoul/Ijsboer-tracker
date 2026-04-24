# 🍦 IJsboer Tracker

Live GPS tracker voor [IJs van Tijs](https://ijsvantijs.nl/) — klanten zien in real-time waar de ijsbus is.

## Hoe het werkt

De ijsboer opent de PWA op zijn telefoon en drukt op **Start**. Zijn locatie verschijnt direct als bewegende ijsbus op de kaart op de website. Na afloop drukt hij op **Stop** — de pin verdwijnt automatisch.

```
[PWA telefoon ijsboer] → [FastAPI backend] → [Kaart op website]
     GPS elke 30s           Railway hosting       Leaflet.js
```

## Live URLs

| | URL |
|---|---|
| PWA voor ijsboer | [shansoul.github.io/Ijsboer-tracker](https://shansoul.github.io/Ijsboer-tracker/) |
| Kaart demo | [shansoul.github.io/Ijsboer-tracker/kaart-demo.html](https://shansoul.github.io/Ijsboer-tracker/kaart-demo.html) |
| Backend API | [ijsboer-tracker-production.up.railway.app](https://ijsboer-tracker-production.up.railway.app/api/location) |

## Voor het webteam

Het kant-en-klare HTML-snippet voor integratie op de website staat in [`docs/website-integratie.md`](docs/website-integratie.md) — ook beschikbaar als [PDF](docs/website-integratie.pdf).

## Technologie

- **Backend** — FastAPI op Railway
- **PWA** — Vanilla HTML/JS op GitHub Pages
- **Kaart** — Leaflet.js + OpenStreetMap
