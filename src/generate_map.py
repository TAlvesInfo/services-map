"""Generate an interactive world map showing bizAPIs country coverage.

Uses Folium (Python Leaflet wrapper) to create a self-contained HTML file
with colored countries and hover/click interactivity.
"""

import json
import sys
from pathlib import Path

import folium
import requests
import yaml

from countries_data import ALPHA2_TO_ALPHA3, get_country_name

# Base URL for the bizAPIs developer docs
DOCS_BASE = "https://developers.bizapis.com/v3.0/reference"

# Mapping: service name -> (page_slug, anchor_fragment)
# Built from the ReadMe docs navigation structure
SERVICE_DOC_LINKS = {
    # Portugal - AT Services
    "at-aggregator": ("at-services", "at-aggregator-autoridade-tributária-agregador"),
    "at-divida": ("at-services", "at-divida-autoridade-tributária-dívidanão-dívida"),
    "at-irc": ("at-services", "at-irc-autoridade-tributária-imposto-sobre-o-rendimento"),
    "at-iva-sa": ("at-services", "at-iva--sa-autoridade-tributária-iva-situação-atual"),
    "at-iva-enquadramento": ("at-services", "at-iva-enquadramento-autoridade-tributária-enquadramento-do-iva"),
    "at-iva-dp": ("at-services", "at-iva-dp-autoridade-tributária-iva-declarações-periódicas"),
    "at-debtors-list": ("at-services", "serviços-at-autoridade-tributária"),
    "at-information": ("at-services", "serviços-at-autoridade-tributária"),
    "at-information-service": ("at-services", "serviços-at-autoridade-tributária"),
    # Portugal - Property Registration
    "cpp": ("property-registration", "cpp-certidão-permanente-predial"),
    "cprc-by-nif": ("property-registration", "cprc-certidão-permanente-de-registo-comercial"),
    # Portugal - Business & Financial
    "northdata-company-search": ("business-financial", "negócios-e-finanças"),
    # Portugal - Tax Returns (IRS)
    "irs-by-code": ("tax-returns-irs", "irsbycode-imposto-sobre-o-rendimento-das-pessoas-singulares"),
    "irs-by-user-password": ("tax-returns-irs", "irsbyuserpassword-imposto-sobre-o-rendimento-das-pessoas-singulares"),
    # Portugal - Social Security
    "ss-no-debt": ("social-security", "ss-no-debt-segurança-social"),
    "ss-sa": ("social-security", "ss-sa-segurança-social"),
    "ss-debtors-list": ("social-security", "segurança-social"),
    # Portugal - Other Services
    "seguro-by-matricula": ("other-services", "seguro-by-matricula"),
    "inpi-trademark-extraction": ("other-services", "inpi-trademark-extraction"),
    "vehicle-by-nif": ("other-services", "outros-serviços"),
    # France
    "rne": ("french-services", "rne"),
    # Poland - KRS
    "court-registry-current-extract": ("polish-krs-services", "court-registry-current-extract"),
    "court-registry-current-extract-service": ("polish-krs-services", "court-registry-current-extract"),
    "court-registry-full-extract": ("polish-krs-services", "court-registry-full-extract"),
    "court-registry-full-extract-service": ("polish-krs-services", "court-registry-full-extract"),
    "court-registry-financials": ("polish-krs-services", "serviços-krs-registo-comercial"),
    "court-registry-financials-service": ("polish-krs-services", "serviços-krs-registo-comercial"),
    # Poland - CRBR
    "beneficial-owner-registry": ("polish-crbr-services", "beneficial-owner-registry"),
    "beneficial-owner-registry-service": ("polish-crbr-services", "beneficial-owner-registry"),
    # Spain
    "company-registry-search": ("spanish-services", "company-registry-search"),
    # Hungary
    "company-registry-data": ("hungarian-services-1", "company-registry-data"),
    "company-registry-snapshot": ("hungarian-services-1", "company-registry-snapshot"),
    # Romania
    "company-data": ("romanian-services", "company-tax-data"),
    "court-records": ("romanian-services", "serviços-roménia"),
    "tax-debt": ("romanian-services", "serviços-roménia"),
}


def get_service_doc_url(service_name):
    """Get the full documentation URL for a service, or None if not mapped."""
    entry = SERVICE_DOC_LINKS.get(service_name)
    if entry:
        page_slug, anchor = entry
        return f"{DOCS_BASE}/{page_slug}#{anchor}"
    return None


# GeoJSON data source (Natural Earth via GitHub)
GEOJSON_URL = "https://raw.githubusercontent.com/datasets/geo-countries/master/data/countries.geojson"

# Property keys used by this GeoJSON source
PROP_ISO_A3 = "ISO3166-1-Alpha-3"
PROP_ISO_A2 = "ISO3166-1-Alpha-2"
PROP_NAME = "name"

# Fallback: map country names to alpha-2 codes for GeoJSON entries with -99 codes
NAME_TO_ALPHA2 = {
    "France": "FR",
    "Norway": "NO",
    "Kosovo": "XK",
    "Somaliland": "SO",
    "Northern Cyprus": "CY",
}


def download_geojson(data_dir):
    """Download world GeoJSON if not already cached."""
    geojson_path = data_dir / "world.geojson"

    if geojson_path.exists():
        print(f"Using cached GeoJSON: {geojson_path}")
        with open(geojson_path, "r", encoding="utf-8") as f:
            return json.load(f)

    print(f"Downloading world GeoJSON from {GEOJSON_URL}...")
    response = requests.get(GEOJSON_URL, timeout=60)
    response.raise_for_status()

    geojson = response.json()

    with open(geojson_path, "w", encoding="utf-8") as f:
        json.dump(geojson, f)

    print(f"Saved to {geojson_path} ({len(geojson['features'])} countries)")
    return geojson


def load_countries_data(data_dir):
    """Load the countries.json produced by extract_services.py."""
    countries_path = data_dir / "countries.json"

    if not countries_path.exists():
        print(f"Error: {countries_path} not found. Run extract_services.py first.")
        sys.exit(1)

    with open(countries_path, "r", encoding="utf-8") as f:
        return json.load(f)


def build_map(geojson, countries_data, config):
    """Build the interactive Folium map."""
    colors = config.get("colors", {})
    map_config = config.get("map", {})

    color_map = {
        "developed": colors.get("developed", "#2ecc71"),
        "in_development": colors.get("in_development", "#f39c12"),
        "not_covered": colors.get("not_covered", "#ecf0f1"),
    }

    # Build alpha-2 lookup from GeoJSON (this source has both alpha-2 and alpha-3)
    # countries_data is keyed by alpha-2 (PT, FR, etc.)

    # Create base map
    center = map_config.get("initial_center", [30, 10])
    zoom = map_config.get("initial_zoom", 2)

    m = folium.Map(
        location=center,
        zoom_start=zoom,
        tiles="cartodbpositron",
        min_zoom=3,
        max_zoom=7,
        world_copy_jump=False,
        no_wrap=True,
        max_bounds=True,
    )

    def get_alpha2(feature):
        """Get alpha-2 code from feature, with name-based fallback for -99 entries."""
        props = feature.get("properties", {})
        alpha2 = props.get(PROP_ISO_A2, "")
        if alpha2 and alpha2 != "-99":
            return alpha2
        # Fallback: match by country name
        name = props.get(PROP_NAME, "")
        return NAME_TO_ALPHA2.get(name, "")

    def get_status(feature):
        """Get country status from feature properties using alpha-2 code."""
        alpha2 = get_alpha2(feature)
        if alpha2 in countries_data:
            return countries_data[alpha2]["status"]
        return "not_covered"

    def style_function(feature):
        status = get_status(feature)
        return {
            "fillColor": color_map.get(status, color_map["not_covered"]),
            "color": colors.get("border", "#bdc3c7"),
            "weight": 0.5,
            "fillOpacity": 0.7,
        }

    def highlight_function(feature):
        return {
            "weight": 2,
            "color": colors.get("hover", "#3498db"),
            "fillOpacity": 0.85,
        }

    def build_popup_html(feature):
        props = feature.get("properties", {})
        alpha2 = get_alpha2(feature)
        country_name = props.get(PROP_NAME, "Unknown")
        country_data = countries_data.get(alpha2)

        if not country_data:
            return f"<div style='font-family:sans-serif;min-width:150px;'><b>{country_name}</b><br><i>No bizAPIs coverage</i></div>"

        status = country_data["status"]
        status_label = "Developed" if status == "developed" else "In Development"
        status_color = color_map.get(status, "#999")
        services = country_data.get("services", [])

        html = f"""
        <div style="font-family:sans-serif;min-width:220px;max-width:320px;">
            <h4 style="margin:0 0 6px 0;border-bottom:2px solid {status_color};padding-bottom:4px;">
                {country_name}
            </h4>
            <div style="margin-bottom:6px;">
                <span style="background:{status_color};color:#fff;padding:2px 8px;border-radius:3px;font-size:12px;">
                    {status_label}
                </span>
                <span style="font-size:12px;color:#666;margin-left:8px;">
                    {len(services)} service{'s' if len(services) != 1 else ''}
                </span>
            </div>
            <div style="max-height:200px;overflow-y:auto;">
        """

        for svc in services:
            portal = svc.get("portal", "")
            portal_html = f"<span style='color:#888;font-size:11px;'> — {portal}</span>" if portal else ""
            doc_url = get_service_doc_url(svc["name"])
            if doc_url:
                name_html = f"<a href='{doc_url}' target='_blank' style='color:#2980b9;text-decoration:none;font-weight:500;' onmouseover=\"this.style.textDecoration='underline'\" onmouseout=\"this.style.textDecoration='none'\">{svc['name']}</a>"
            else:
                name_html = svc["name"]
            html += f"<div style='padding:3px 0;border-bottom:1px solid #eee;font-size:13px;'>{name_html}{portal_html}</div>"

        html += "</div></div>"
        return html

    # Add each country as its own GeoJson layer with popup
    for feature in geojson["features"]:
        popup_html = build_popup_html(feature)
        popup = folium.Popup(popup_html, max_width=350)

        country_name = feature.get("properties", {}).get(PROP_NAME, "")
        tooltip = folium.Tooltip(
            country_name,
            style="font-family:sans-serif;font-size:13px;font-weight:bold;",
            sticky=True,
        )

        geojson_layer = folium.GeoJson(
            feature,
            style_function=style_function,
            highlight_function=highlight_function,
        )
        geojson_layer.add_child(popup)
        geojson_layer.add_child(tooltip)
        geojson_layer.add_to(m)

    # Add legend
    legend_html = f"""
    <div style="
        position: fixed;
        bottom: 30px;
        right: 30px;
        z-index: 1000;
        background: white;
        padding: 12px 16px;
        border-radius: 8px;
        box-shadow: 0 2px 8px rgba(0,0,0,0.2);
        font-family: sans-serif;
        font-size: 13px;
    ">
        <b style="font-size:14px;">{map_config.get('title', 'bizAPIs Coverage')}</b>
        <br><br>
        <span style="background:{color_map['developed']};width:14px;height:14px;display:inline-block;border-radius:3px;vertical-align:middle;"></span>
        &nbsp;Developed ({sum(1 for c in countries_data.values() if c['status'] == 'developed')})
        <br>
        <span style="background:{color_map['in_development']};width:14px;height:14px;display:inline-block;border-radius:3px;vertical-align:middle;"></span>
        &nbsp;In Development ({sum(1 for c in countries_data.values() if c['status'] == 'in_development')})
        <br>
        <span style="background:{color_map['not_covered']};width:14px;height:14px;display:inline-block;border-radius:3px;vertical-align:middle;border:1px solid #ddd;"></span>
        &nbsp;Not Covered
    </div>
    """
    m.get_root().html.add_child(folium.Element(legend_html))

    return m


def main():
    project_root = Path(__file__).parent.parent
    config_path = project_root / "config.yaml"
    data_dir = project_root / "data"

    # Load config
    with open(config_path, "r", encoding="utf-8") as f:
        config = yaml.safe_load(f)

    # Download/load GeoJSON
    geojson = download_geojson(data_dir)

    # Load countries data
    countries_data = load_countries_data(data_dir)
    print(f"Loaded {len(countries_data)} countries with services")

    # Verify matching: check how many countries_data entries match GeoJSON features
    matched = set()
    for feat in geojson["features"]:
        a2 = feat.get("properties", {}).get(PROP_ISO_A2, "")
        if a2 == "-99":
            a2 = NAME_TO_ALPHA2.get(feat.get("properties", {}).get(PROP_NAME, ""), "")
        if a2 in countries_data:
            matched.add(a2)
    print(f"Matched {len(matched)}/{len(countries_data)} countries to GeoJSON features")
    unmatched = set(countries_data.keys()) - matched
    if unmatched:
        print(f"Unmatched: {unmatched}")

    # Build map
    m = build_map(geojson, countries_data, config)

    # Save output
    output_file = project_root / config.get("output", {}).get("html_file", "output/index.html")
    output_file.parent.mkdir(parents=True, exist_ok=True)

    m.save(str(output_file))
    print(f"\nMap saved to: {output_file}")
    print(f"Open in browser to view the interactive map.")


if __name__ == "__main__":
    main()
