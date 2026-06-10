"""
Download community location points for major population centers in
Butte County, California.

This script uses OpenStreetMap's Nominatim geocoding service to obtain
coordinates for selected communities and exports them as a GeoJSON
point layer for use in wildfire risk mapping and web applications.
"""

from pathlib import Path

import geopandas as gpd
from geopy.geocoders import Nominatim


PROJECT_ROOT = Path(__file__).resolve().parents[2]

PROCESSED_DIR = (
    PROJECT_ROOT /
    "data" /
    "processed"
)

COMMUNITIES_PATH = (
    PROCESSED_DIR /
    "community_points.geojson"
)

COMMUNITIES = [
    "Chico, California, USA",
    "Paradise, California, USA",
    "Magalia, California, USA",
    "Oroville, California, USA",
    "Gridley, California, USA",
    "Biggs, California, USA"
]


geolocator = Nominatim(
    user_agent="wildfire_geoai"
)

records = []

for community in COMMUNITIES:

    location = geolocator.geocode(
        community
    )

    if location:

        records.append(
            {
                "community": community.split(",")[0],
                "longitude": location.longitude,
                "latitude": location.latitude
            }
        )

communities = gpd.GeoDataFrame(
    records,
    geometry=gpd.points_from_xy(
        [r["longitude"] for r in records],
        [r["latitude"] for r in records]
    ),
    crs="EPSG:4326"
)

communities.to_file(
    COMMUNITIES_PATH,
    driver="GeoJSON"
)

print(
    f"Saved: {COMMUNITIES_PATH}"
)