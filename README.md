# South View — Interactive Map Demo

Minimal Mapbox proof-of-concept. Static map centered on South View Cemetery (Atlanta, GA) with 5 clickable markers and a Randomize button.

## Setup (≈15 min)

1. **Get a Mapbox token**
   - Go to [account.mapbox.com](https://account.mapbox.com/)
   - Sign up (free tier is enough)
   - Copy your default public token (or create one)

2. **Add your token**
   - Copy `config.example.js` to `config.js`
   - Replace `YOUR_MAPBOX_ACCESS_TOKEN` with your token in `config.js`

3. **Open the map**
   - Open `index.html` in a browser (double-click or `open index.html` in Terminal)

## What it does

- Map centered on South View Cemetery
- 5 hardcoded markers (notable figures buried there)
- Click a marker → popup with name + summary
- **Randomize** button → cycles to next marker, flies to it, opens its popup

## No build step

Single HTML file. No npm, no database, no backend.
