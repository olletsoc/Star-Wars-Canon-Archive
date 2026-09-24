# Star Wars Canon Media Chronology

An interactive, single-page timeline of *Star Wars* canon media — films, series
episodes, novels, comics, audio dramas, and games — organized by in-universe era
(from the Dawn of the Jedi through the New Republic and beyond). Built from
[Wookieepedia's "Timeline of canon media"](https://starwars.fandom.com/wiki/Timeline_of_canon_media).

Filter by format, search titles, and toggle between **story order** (in-universe
chronology) and **release order** (real-world publication date).

## Project structure

```
.
├── index.html    The page. Presentation + logic only; fetches data.json at load.
├── data.json     Generated output. Do NOT hand-edit — it's overwritten by build.py.
├── data.csv      Source of truth. Edit this to add, change, or remove entries.
├── editor.html   Visual editor — add/edit entries with a form, export both files.
└── build.py      Regenerates data.json from data.csv.
```

`data.csv` is the file you edit; `data.json` is generated from it.

## Editing without hand-coding: editor.html

Prefer a form over a spreadsheet? Open `editor.html` (served over http — see
"Running locally"). It auto-loads `data.json`, lists every entry, and gives you
proper fields for each column. `era` is derived live from the year as you type.

- **Add / edit / duplicate / delete / reorder** entries.
- **Search and sort** (file order, story order, or release date).
- **Italicize** helper wraps selected title text in `<em>`, with a live preview.
- **Export** buttons download a fresh `data.json` (era derived) and `data.csv`,
  both in the exact formats used here. Drop the downloads into this folder,
  replacing the old files, then commit.

If you're not running a local server, click **Import file…** in the editor to load
your existing `data.json` or `data.csv` from disk.

## Editing the timeline

Open `data.csv` in any spreadsheet app (Numbers, Excel, Google Sheets) or a text
editor. Each row is one entry.

| Column | Meaning |
|--------|---------|
| `y`    | Integer sort key — years relative to the Battle of Yavin. Negative = **BBY** (before), positive or zero = **ABY** (after). e.g. `-382`, `9`, `34` |
| `disp` | The date label shown on the card. e.g. `382 BBY`, `9 ABY` |
| `f`    | Format code (see below) |
| `t`    | Title. May contain `<em>…</em>` for italics |
| `rel`  | Real-world release date, `YYYY-MM-DD`, or blank if unknown/unreleased |
| `note` | Optional note shown on the card, or blank |
| `url`  | Optional link to the media. When set, the card becomes clickable. Blank if none yet |

**Format codes:** `F` film · `N` novel · `JR` junior novel · `YR` young-reader ·
`VG` video game · `TV` TV episode · `C` comic · `SS` short story · `A` audio drama ·
`RPG` roleplaying · `P` promotional

There is **no `era` column** — the era is derived from `y` by the build script, so
changing a row's year automatically moves it to the correct era.

## Building

After editing `data.csv`, regenerate `data.json`:

```bash
python3 build.py
```

Requires only the Python 3 standard library (no installs). It prints a summary:

```
Wrote 602 records to .../data.json
  dawn          8
  highrepublic  156
  fall          204
  ...
```

## Running locally

The page loads its data with `fetch()`, so it must be served over **http** —
opening `index.html` directly from a `file://` path won't work. Start a quick
local server in this folder:

```bash
python3 -m http.server
# then open http://localhost:8000
```

## Deploying

Any static host works. For **GitHub Pages**: push this folder to a repo, then in
**Settings → Pages** set the source to your default branch at the root. The site
will serve at `https://<username>.github.io/<repo>/`.

---

*Media data © Lucasfilm / Disney, sourced from Wookieepedia (CC BY-SA). This is a
non-commercial fan project.*
