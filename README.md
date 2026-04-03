# South View — Historic Cemetery Navigation & History

Interactive map and list for South View Cemetery (Atlanta, GA). The app loads **`data/graves.json`**, generated from **`buried-data.csv`** (20 real records with distinct coordinates from the cemetery export). Regenerate both JSON files with **`python python/buried_subset.py`** from the project root (stdlib only). For a larger merge workflow with pandas, set **`INPUT_FILE`** in **`python/convert.py`** to `buried-data.csv` (default) or to the full daily CSV under the repo root.

## Setup

1. **Mapbox token**  
   - Get a token at [account.mapbox.com](https://account.mapbox.com/).  
   - Copy `config.example.js` to `config.js` and set your token in `config.js`.

2. **Data**  
   - **Curated subset (default):** run `python3 python/buried_subset.py` — writes `data/graves.json` and `data/coordinates.json` from `buried-data.csv` (20 records; no pandas). If a full export CSV named `southview-daily-interment-all-time (1).csv` exists in the repo root, it also rebuilds `buried-data.csv` first.  
   - **Full CSV + pandas:** install deps (`pip install -r python/requirements.txt`), set `INPUT_FILE` in `python/convert.py` if needed, then `python3 python/convert.py`.

3. **Run locally**  
   - Serve over HTTP (Mapbox needs it; `file://` will not load tiles):
     cd /path/to/southview
     ```bash
     python3 -m http.server 3000
     ```
   - Open **http://localhost:3000**.

   - **If you see a failed-to-load dataset error:**  
     - Run **`python python/buried_subset.py`** to create `buried-data.csv`, `data/graves.json`, and `data/coordinates.json`.  
     - Open **http://localhost:3000** (not `file://`) and serve from the project root.

## Features

- **Map**: Clustered markers for burials with coordinates; click cluster to zoom, click point to open detail.
- **Filters**: Name search, Gender, Section, Funeral home, Grave type.
- **List view**: Toggle “List view” to see burials; click a row to fly to map and open popup.
- **Detail popup**: Name, birth/death/service dates, age, section, funeral home, grave type; “Related burials” (same section or funeral home).
- **Guided tour**: Path through up to 20 filtered burials; Prev/Next and Exit.
- **Randomize**: Picks a random burial (with coordinates) from the current filter and opens its popup.

## Data workflow

See **WORKFLOW.md** for the recommended path: Google Forms → Google Sheets → CSV export → `python/convert.py` → `data/graves.json`. No auth in this phase.

## Usability testing

See **USABILITY_TESTING.md** for tasks and notes to use with 2 testers.

## Tech

- `index.html`, `css/app.css`, `assets/`, and ES modules in `js/`; Mapbox GL JS from CDN; no build step.
- Backend / data pipeline: `python/` (`buried_subset.py`, `convert.py`, `reorder_buried_path.py`, `requirements.txt`).
- Data: `data/graves.json` from `buried-data.csv` via `python/buried_subset.py`, or from `python/convert.py` for larger exports.
