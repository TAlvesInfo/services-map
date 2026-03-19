"""Country data models and ISO code to name mappings."""

# ISO 3166-1 alpha-2 to country name mapping (for display on the map)
COUNTRY_NAMES = {
    "AR": "Argentina",
    "AU": "Australia",
    "BR": "Brazil",
    "CH": "Switzerland",
    "CL": "Chile",
    "CZ": "Czech Republic",
    "ES": "Spain",
    "FI": "Finland",
    "FR": "France",
    "HU": "Hungary",
    "IE": "Ireland",
    "IT": "Italy",
    "NO": "Norway",
    "NZ": "New Zealand",
    "PL": "Poland",
    "PT": "Portugal",
    "RO": "Romania",
    "US": "United States",
}

# ISO alpha-2 to alpha-3 mapping (GeoJSON uses alpha-3)
ALPHA2_TO_ALPHA3 = {
    "AR": "ARG", "AU": "AUS", "BR": "BRA", "CH": "CHE",
    "CL": "CHL", "CZ": "CZE", "FI": "FIN", "FR": "FRA",
    "HU": "HUN", "IE": "IRL", "IT": "ITA", "NO": "NOR",
    "NZ": "NZL", "PL": "POL", "PT": "PRT", "RO": "ROU",
    "DE": "DEU", "ES": "ESP", "GB": "GBR", "US": "USA",
    "NL": "NLD", "BE": "BEL", "AT": "AUT", "SE": "SWE",
    "DK": "DNK", "SK": "SVK", "BG": "BGR", "HR": "HRV",
    "SI": "SVN", "LT": "LTU", "LV": "LVA", "EE": "EST",
    "CY": "CYP", "LU": "LUX", "MT": "MLT", "GR": "GRC",
}


def get_country_name(alpha2_code):
    """Get display name for a country code."""
    return COUNTRY_NAMES.get(alpha2_code, alpha2_code)


def get_alpha3(alpha2_code):
    """Convert ISO alpha-2 to alpha-3 code."""
    return ALPHA2_TO_ALPHA3.get(alpha2_code, alpha2_code)
