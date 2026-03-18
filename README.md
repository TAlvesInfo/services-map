# ReadMe Coverage Map

Interactive world map showing bizAPIs country coverage and services, designed to be embedded in ReadMe documentation.

## Overview

This project generates an interactive HTML map that visualizes:
- **Green**: Countries where bizAPIs services are fully developed
- **Yellow/Orange**: Countries currently in development
- **Gray/Blank**: Countries with no coverage

Hovering or clicking a country displays a panel listing all available services for that country.

## Technology Stack

- **Python 3.8+** - Core language
- **Folium** - Python wrapper for Leaflet.js (interactive maps)
- **PyYAML** - Parse bizAPIs service metadata
- **GeoJSON** - World country boundaries data

## Project Structure

```
readme-map/
├── README.md                  # This file
├── requirements.txt           # Python dependencies
├── config.yaml                # Country status configuration
├── src/
│   ├── extract_services.py    # Parse bizAPIs YAML metadata
│   ├── generate_map.py        # Build the interactive map
│   └── countries_data.py      # Country/service data models
├── data/
│   ├── countries.json         # Generated country→services mapping
│   └── world.geojson          # World boundaries (auto-downloaded)
├── output/
│   └── index.html             # Generated map (deploy this)
├── Sprints/                   # Sprint Management (v2.2.0)
│   ├── MASTER-SPRINT.md       # Start here after /clear
│   ├── SPRINT-INDEX.md        # Sprint lookup
│   ├── SPRINT-PLANNING.md     # Roadmap
│   └── ...
└── .claude/commands/          # Sprint slash commands
```

## Quick Start

```bash
# 1. Install dependencies
pip install -r requirements.txt

# 2. Extract service data from bizAPIs metadata
python src/extract_services.py --metadata-path /path/to/environment-setup/service-metadata/

# 3. Generate the map
python src/generate_map.py

# 4. Open output/index.html in browser
```

## Sprint Management

This project uses the [Sprint Management Framework v2.2.0](https://github.com/github-joyngroup/SprintManagement).

- Check status: `/sprint-status`
- Start work: `/sprint-start`
- Create sprint: `/sprint-new`
- Complete sprint: `/sprint-complete`

See [Sprints/MASTER-SPRINT.md](./Sprints/MASTER-SPRINT.md) for current project state.

## Data Sources

- **Country/service data**: Extracted from `C:\Users\talves\gitlab\environment-setup\service-metadata\*.yaml`
- **Country boundaries**: Natural Earth GeoJSON (auto-downloaded)

## Deployment

The generated `output/index.html` is a self-contained file that can be:
1. Hosted on GitHub Pages, Netlify, or S3
2. Embedded in ReadMe docs via `<iframe>`
