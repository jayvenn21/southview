# Data workflow — South View Cemetery

Controlled submission pipeline: no public editing, no auth in scope. Proof that staff can add/update graves via a simple, professional flow.

The public app does not link to a submission form; staff use a Google Form and Sheet outside the UI as needed.

---

## A. Link the Form to a Google Sheet

1. Open your burial-updates **Google Form** (create one if needed).
2. Go to **Responses** → click the green **Link to Sheets** icon.
3. Choose **Create a new spreadsheet** and name it: **southview-burial-updates**.
4. Every new submission will appear as a new row in that sheet.

**Google Form fields (what Wini needs):**

| Field | Description |
|-------|-------------|
| Deceased ID | Optional — for updating an existing record |
| First Name | Text, required |
| Middle Name | Optional |
| Last Name | Text, required |
| Birth Date | Date |
| Death Date | Date |
| Service Date | Date |
| Age | Number |
| Gender | M/F or dropdown |
| Section | Dropdown or text |
| Lot | Number |
| Space | Number |
| Vault Type | Text |
| Grave Type | Text |
| Funeral Home | Text |
| Coordinates (lat/lng) | Optional, for manual correction |
| Notes | Long text / description |

In Form settings: **Collect email addresses** and restrict to South-View domain. No login system, no backend auth — the form is the gate.

---

## B. Export the sheet for the app

1. In the Google Sheet: **File → Download → Comma-separated values (.csv)**.
2. Save the file as **southview-burial-updates.csv**.
3. Put it in your project here: **`data/updates/southview-burial-updates.csv`**.

**Optional — Apps Script to export CSV from the sheet:**

```js
function exportCSV() {
  var sheet = SpreadsheetApp.getActive().getSheetByName("Form Responses 1");
  var csv = sheet.getDataRange().getValues()
    .map(function(r) { return r.join(","); })
    .join("\n");
  DriveApp.createFile("southview-burial-updates.csv", csv);
}
```

Run when you want a fresh export; then download the file and place it in `data/updates/`.

---

## C. Merge updates into graves: `python/convert.py`

1. **Main data:** By default **`python/convert.py`** uses **`buried-data.csv`** in the project root (20-row curated subset). To use a new full cemetery export, place it in the project root and set **`INPUT_FILE`** in `python/convert.py` to that filename.
2. **Updates:** Place the Form export at **`data/updates/southview-burial-updates.csv`**.
3. **Run:**
   ```bash
   python3 python/convert.py
   ```
4. **Merge behavior:**
   - Row with **Deceased ID** matching an existing grave → **update** that record.
   - Row with no ID or new ID → **new grave** (appended).
5. Output: **`data/graves.json`** (and `data/coordinates.json`). The app loads `data/graves.json`; refresh the page to see new/updated records.

---

## D. Pipeline summary

```
Google Form (staff only)
   ↓
Google Sheet (southview-burial-updates)
   ↓  File → Download → CSV
data/updates/southview-burial-updates.csv
   ↓
python3 python/convert.py
   ↓
data/graves.json
   ↓
App loads updated records (refresh page)
```

- **No login or Firebase** — form + domain restriction is the gate.
- **When to run convert:** Whenever new submissions are in the sheet. Download CSV → replace `data/updates/southview-burial-updates.csv` → run `python3 python/convert.py` → refresh the app.

---

## E. Historical categories (your interpretive layer)

**The Google Form does not collect categories.** Categories are your curation for storytelling and guided tours, not part of cemetery data entry.

- **File:** `data/categories.json` — keys like `civil_rights`, `veterans`, `musicians`, `community`, `family`, `educators`, `women`, etc., each with an array of **grave IDs** (numbers matching `id` in `graves.json`).
- **Example:** `"veterans": [123, 456, 789]` — those IDs are included in the “Veterans & Heroes” story tour.
- **Guided Tour Mode** in the app uses this file: if a category has IDs, the tour follows those graves in order; if empty, the tour falls back to the first N graves with coordinates.
- You (or Lehman/South-View) research and maintain this file to build Civil Rights, Musicians of Atlanta, Women of South-View, etc. This is the cultural, historical layer that makes the project more than a burial search.

---

## F. Future (presentation only)

“In the full version, South-View staff could log in through a secure admin dashboard and update records directly.” Not built in this phase — keep scope to workflow + map + filters + tours.
