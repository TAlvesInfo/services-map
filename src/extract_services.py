"""Extract country/service data from bizAPIs metadata files.

Reads:
- service-metadata/*.yaml  (service name, portal, region)
- instructions/services/{country}/{country}/*.json (service instructions)

Produces: data/countries.json
"""

import json
import os
import sys
from pathlib import Path

import yaml

from countries_data import COUNTRY_NAMES, get_country_name


def parse_service_metadata(metadata_path):
    """Parse all YAML service metadata files and return a list of service dicts."""
    services = []
    metadata_dir = Path(metadata_path)

    if not metadata_dir.exists():
        print(f"Warning: metadata path does not exist: {metadata_dir}")
        return services

    for yaml_file in sorted(metadata_dir.glob("*.yaml")):
        with open(yaml_file, "r", encoding="utf-8") as f:
            data = yaml.safe_load(f)

        if not data:
            continue

        service = {
            "name": data.get("serviceName", yaml_file.stem),
            "identifier": data.get("serviceIdentifier", ""),
            "portal": data.get("sourcePortal", ""),
            "portal_url": data.get("sourcePortalURL", ""),
            "country": data.get("region", {}).get("countryPortal", ""),
        }
        services.append(service)

    return services


def scan_instructions_directory(instructions_path):
    """Scan the instructions/services directory to discover all countries and services.

    Directory structure: instructions/services/{country_code}/{country_code}/*.json
    Excludes 'working' subdirectories (contain duplicates).
    """
    country_services = {}
    instructions_dir = Path(instructions_path)

    if not instructions_dir.exists():
        print(f"Warning: instructions path does not exist: {instructions_dir}")
        return country_services

    for country_dir in sorted(instructions_dir.iterdir()):
        if not country_dir.is_dir():
            continue

        country_code = country_dir.name.upper()

        # Skip GLEIF (global, not country-specific)
        if country_code == "GLEIF":
            continue

        # Look inside the nested country dir (e.g., pt/pt/)
        inner_dir = country_dir / country_dir.name
        if not inner_dir.exists():
            continue

        services = []
        for json_file in sorted(inner_dir.glob("*.json")):
            # Skip 'working' subdirectory files
            if "working" in str(json_file.parent):
                continue

            service_name = json_file.stem
            services.append({
                "name": service_name,
                "identifier": service_name.upper().replace("-", "_"),
            })

        if services:
            if country_code not in country_services:
                country_services[country_code] = []
            country_services[country_code].extend(services)

    return country_services


def merge_service_data(metadata_services, instruction_services):
    """Merge metadata (YAML) with instruction-discovered services.

    Metadata provides richer info (portal name, URL).
    Instructions provide full country coverage discovery.
    """
    # Build lookup from metadata by service name
    metadata_lookup = {}
    for svc in metadata_services:
        metadata_lookup[svc["name"]] = svc

    # Start with instruction-discovered services (most complete country coverage)
    merged = {}
    for country_code, services in instruction_services.items():
        merged[country_code] = []
        for svc in services:
            # Try to enrich with metadata
            meta = metadata_lookup.get(svc["name"], {})
            merged[country_code].append({
                "name": svc["name"],
                "identifier": meta.get("identifier", svc["identifier"]),
                "portal": meta.get("portal", ""),
                "portal_url": meta.get("portal_url", ""),
            })

    # Add any metadata-only services not found in instructions
    for svc in metadata_services:
        country = svc["country"]
        if not country:
            continue
        if country not in merged:
            merged[country] = []
        existing_names = {s["name"] for s in merged[country]}
        if svc["name"] not in existing_names:
            merged[country].append({
                "name": svc["name"],
                "identifier": svc["identifier"],
                "portal": svc["portal"],
                "portal_url": svc["portal_url"],
            })

    return merged


def build_countries_json(country_services, config_path=None):
    """Build the final countries.json structure.

    Reads config.yaml for developed/in_development classification.
    """
    # Load config for country status classification
    developed = set()
    in_development = set()

    if config_path and Path(config_path).exists():
        with open(config_path, "r", encoding="utf-8") as f:
            config = yaml.safe_load(f)

        countries_config = config.get("countries", {})
        developed = set(countries_config.get("developed", []))
        in_dev_raw = countries_config.get("in_development", [])
        if isinstance(in_dev_raw, list):
            in_development = set(in_dev_raw)

    # Build output
    countries = {}
    for country_code, services in sorted(country_services.items()):
        if country_code in developed:
            status = "developed"
        elif country_code in in_development:
            status = "in_development"
        else:
            status = "developed"  # If it has services, default to developed

        countries[country_code] = {
            "name": get_country_name(country_code),
            "code": country_code,
            "status": status,
            "service_count": len(services),
            "services": sorted(services, key=lambda s: s["name"]),
        }

    # Add in_development countries that have no services yet
    for country_code in in_development:
        if country_code not in countries:
            countries[country_code] = {
                "name": get_country_name(country_code),
                "code": country_code,
                "status": "in_development",
                "service_count": 0,
                "services": [],
            }

    return countries


def main():
    # Resolve paths
    project_root = Path(__file__).parent.parent
    config_path = project_root / "config.yaml"

    # Load config for source paths
    with open(config_path, "r", encoding="utf-8") as f:
        config = yaml.safe_load(f)

    metadata_path = config.get("metadata_path", "")
    instructions_path = config.get("instructions_path", "")

    # Allow command-line overrides
    if len(sys.argv) > 1:
        for arg in sys.argv[1:]:
            if arg.startswith("--metadata-path="):
                metadata_path = arg.split("=", 1)[1]
            elif arg.startswith("--instructions-path="):
                instructions_path = arg.split("=", 1)[1]

    print(f"Metadata path: {metadata_path}")
    print(f"Instructions path: {instructions_path}")

    # Extract data from both sources
    metadata_services = parse_service_metadata(metadata_path)
    print(f"Found {len(metadata_services)} services in YAML metadata")

    instruction_services = scan_instructions_directory(instructions_path)
    total_instruction = sum(len(v) for v in instruction_services.values())
    print(f"Found {total_instruction} services across {len(instruction_services)} countries in instructions")

    # Merge
    merged = merge_service_data(metadata_services, instruction_services)
    total_merged = sum(len(v) for v in merged.values())
    print(f"Merged: {total_merged} services across {len(merged)} countries")

    # Build final JSON
    countries = build_countries_json(merged, config_path)

    # Write output
    output_path = project_root / config.get("output", {}).get("data_file", "data/countries.json")
    output_path.parent.mkdir(parents=True, exist_ok=True)

    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(countries, f, indent=2, ensure_ascii=False)

    print(f"\nWritten to {output_path}")
    print(f"\nCountry summary:")
    for code, data in sorted(countries.items()):
        print(f"  {code} ({data['name']}): {data['service_count']} services [{data['status']}]")


if __name__ == "__main__":
    main()
