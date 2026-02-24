# South View — Historic Cemetery Navigation & History

Interactive map and list for South View Cemetery (Atlanta, GA). Data-driven from `data/graves.json`: map markers (with clustering), list view, filters, detail popups with dates and related burials, and guided tour.

## Setup

1. **Mapbox token**  
   - Get a token at [account.mapbox.com](https://account.mapbox.com/).  
   - Copy `config.example.js` to `config.js` and set your token in `config.js`.

2. **Data**  
   - Place the South View interment CSV in the project root (or set `INPUT_FILE` in `convert.py`).  
   - Run:
     ```bash
     pip install -r requirements.txt
     python3 convert.py
     ```
   - This writes `data/graves.json` (and `data/coordinates.json`).

3. **Run locally**  
   - Serve over HTTP (Mapbox needs it; `file://` will not load tiles):
     cd /path/to/southview
     ```bash
     python3 -m http.server 3000
     ```
   - Open **http://localhost:3000**.

   - **If you see "Failed to load data/graves.json":**  
     - Regenerate: `python3 convert.py` (from project root).  
     - Ensure you opened **http://localhost:3000** in the browser, not the HTML file via `file://`.  
     - Ensure the server was started from the project root (the folder that contains `data/` and `index.html`).

## Features

- **Map**: Clustered markers for burials with coordinates; click cluster to zoom, click point to open detail.
- **Filters**: Name search, Gender, Section, Funeral home, Grave type.
- **List view**: Toggle “List view” to see burials; click a row to fly to map and open popup.
- **Detail popup**: Name, birth/death/service dates, age, section, funeral home, grave type; “Related burials” (same section or funeral home).
- **Guided tour**: Path through up to 20 filtered burials; Prev/Next and Exit.
- **Randomize**: Picks a random burial (with coordinates) from the current filter and opens its popup.

## Data workflow

See **WORKFLOW.md** for the recommended path: Google Forms → Google Sheets → CSV export → `convert.py` → `data/graves.json`. No auth in this phase.

## Usability testing

See **USABILITY_TESTING.md** for tasks and notes to use with 2 testers.

## Tech

- Single HTML file + Mapbox GL JS; no build step.
- Data: `data/graves.json` produced by `convert.py` from the South View CSV.
