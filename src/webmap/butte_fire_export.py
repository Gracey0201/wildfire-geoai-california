"""
butte_fire_export.py

Clip California wildfire history
to the Butte County study area
for web mapping.

Inputs:
- data/raw/wildfire/wildfire_history.geojson
- data/raw/boundaries/butte_county_boundary.geojson

Output:
- outputs/web/butte_wildfire.geojson
"""

from pathlib import Path
import warnings

import geopandas as gpd

warnings.filterwarnings("ignore")

# PATHS

FIRES_PATH = Path(
    "data/raw/wildfire/wildfire_history.geojson"
)

COUNTY_PATH = Path(
    "data/raw/boundaries/butte_county_boundary.geojson"
)

OUTPUT_DIR = Path(
    "outputs/web"
)

OUTPUT_DIR.mkdir(
    parents=True,
    exist_ok=True
)

OUTPUT_PATH = (
    OUTPUT_DIR /
    "butte_wildfire.geojson"
)

# LOAD DATA

print(
    "\nLoading wildfire history"
)

fires = gpd.read_file(
    FIRES_PATH
)

print(
    "\nLoading Butte County boundary"
)

county = gpd.read_file(
    COUNTY_PATH
)

# MATCH CRS

fires = fires.to_crs(
    county.crs
)

# REPAIR GEOMETRIES

fires["geometry"] = (
    fires.geometry.make_valid()
)

county["geometry"] = (
    county.geometry.make_valid()
)

# CLIP

print(
    "\nClipping wildfire history"
)

fires_butte = gpd.clip(
    fires,
    county
)

# EXPORT TO WGS84 FOR WEB MAPS

fires_butte = fires_butte.to_crs(
    "EPSG:4326"
)

# SAVE

fires_butte.to_file(
    OUTPUT_PATH,
    driver="GeoJSON"
)

print(
    f"\nSaved: {OUTPUT_PATH}"
)

print(
    f"\nTotal California Fires: {len(fires):,}"
)

print(
    f"Butte County Fires: {len(fires_butte):,}"
)

print(
    "\nButte Wildfire Export complete"
)