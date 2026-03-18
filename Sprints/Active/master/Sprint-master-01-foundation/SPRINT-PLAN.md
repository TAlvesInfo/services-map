# Sprint-master-01 - Foundation

**Branch:** master
**Created:** 2026-03-18
**Status:** Active

## Sprint Goals
### Primary Objectives
1. [ ] Set up Python project with virtual environment and dependencies
2. [ ] Parse bizAPIs service-metadata YAML and instructions JSON to extract country/service data
3. [ ] Generate countries.json mapping countries to their services
4. [ ] Download and prepare world GeoJSON boundaries
5. [ ] Create config-driven country status classification

## Task Breakdown (Max 5-7 Tasks)
| ID | Task | Priority | Status |
|----|------|----------|--------|
| T001 | Install Python deps (folium, pyyaml, requests) via pip | HIGH | PENDING |
| T002 | Create extract_services.py - parse YAML metadata + instructions JSON | HIGH | PENDING |
| T003 | Create countries_data.py - data models and country name mappings | HIGH | PENDING |
| T004 | Create generate_map.py - download GeoJSON + build interactive map | HIGH | PENDING |
| T005 | Generate countries.json from actual bizAPIs data | MEDIUM | PENDING |

## Dependencies
- Python 3.12 installed (DONE)
- Access to bizAPIs service-metadata at C:\Users\talves\gitlab\environment-setup\

## Technical Notes
- Service metadata YAML files contain: serviceName, serviceIdentifier, sourcePortal, region.countryPortal
- Instructions JSON files are organized by country: instructions/services/{country_code}/{country_code}/*.json
- Country codes are ISO 3166-1 alpha-2 (PT, FR, IT, PL, etc.)
- GLEIF is a global service (not country-specific) - will be handled separately
- The "working" subdirectory under pt/pt/ contains duplicates - should be excluded

## AI Development Notes
- All tasks are VIBE-appropriate (fully AI-driven)
- Estimated context usage: moderate (mostly file creation)
