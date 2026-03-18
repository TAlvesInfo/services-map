# Sprint Planning - Master Task List

> **Master planning document for all project sprints**

---

## Project Roadmap

### Phase 1: Foundation
| Sprint | Focus | Status | Dependencies |
|--------|-------|--------|--------------|
| Sprint-01 | Project setup, data extraction | PENDING | Python environment |
| Sprint-02 | Interactive map with Leaflet/Folium | PENDING | Sprint-01 |

### Phase 2: Core Features
| Sprint | Focus | Status | Dependencies |
|--------|-------|--------|--------------|
| Sprint-03 | Country hover/click with service list | PENDING | Sprint-02 |
| Sprint-04 | ReadMe integration (iframe embed) | PENDING | Sprint-03 |

### Phase 3: Polish & Release
| Sprint | Focus | Status | Dependencies |
|--------|-------|--------|--------------|
| Sprint-05 | Styling, responsiveness, deployment | PENDING | Sprint-04 |

---

## Current Sprint Backlog

### Sprint-01: Foundation (PENDING)

**Goals:**
- [ ] Extract country/service data from bizAPIs YAML metadata
- [ ] Create Python project structure with dependencies
- [ ] Generate countries.json with developed/in-development/blank status
- [ ] Create GeoJSON data pipeline

**Tasks:**
| ID | Task | Priority | Estimate | Status |
|----|------|----------|----------|--------|
| 01.1 | Set up Python project (venv, requirements.txt) | HIGH | - | PENDING |
| 01.2 | Parse bizAPIs service-metadata YAML files | HIGH | - | PENDING |
| 01.3 | Build country → services mapping JSON | HIGH | - | PENDING |
| 01.4 | Source world GeoJSON boundaries data | MEDIUM | - | PENDING |
| 01.5 | Create configuration for country status (developed/in-dev/blank) | MEDIUM | - | PENDING |

---

## Upcoming Sprints

### Sprint-02: Interactive Map (Planned)
- Build world map using Folium (Python Leaflet wrapper)
- Color countries by status (developed/in-development/blank)
- Generate static HTML output

### Sprint-03: Interactivity (Planned)
- Add hover tooltips with country name + status
- Add click handlers showing service list panel
- Service details: name, description, status

### Sprint-04: ReadMe Integration (Planned)
- Host generated HTML (GitHub Pages or static hosting)
- Create ReadMe custom page with iframe embed
- Test rendering in ReadMe dashboard

### Sprint-05: Polish (Planned)
- Mobile responsiveness
- Europe zoom option (heavy EU coverage)
- Legend and color key
- Auto-update script from YAML metadata

---

## Sprint Planning Guidelines

### Task Limits
- **Maximum 5-7 tasks per sprint** (AI context aware)
- Each task should be completable in one session
- Complex tasks must be broken into sub-tasks

### Task Status Values
- `PENDING` - Not started
- `IN_PROGRESS` - Currently being worked on
- `COMPLETED` - Done
- `BLOCKED` - Cannot proceed (see EXCEPTIONS-LOG)

### Priority Levels
- `HIGH` - Must complete this sprint
- `MEDIUM` - Should complete if time permits
- `LOW` - Can carry over to next sprint

---

## Notes

- Update this document when planning new sprints
- Keep task descriptions concise but clear
- Link to detailed sprint plans in respective folders

---

*Last Updated: 2026-03-18*
