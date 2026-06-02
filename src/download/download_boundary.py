"""
download_boundary.py

Automated download and preprocessing of
Butte County administrative boundary data
for wildfire susceptibility modeling.

This module:
- downloads U.S. county boundaries
- extracts Butte County, California
- reprojects to project CRS
- saves boundary to project directory
"""

from pathlib import Path
import warnings

import geopandas as gpd
import yaml

warnings.filterwarnings("ignore")

# LOAD CONFIGURATION
CONFIG_PATH = "config/config.yaml"

with open(CONFIG_PATH, "r") as file:
    config = yaml.safe_load(file)


# SETTINGS CONFIGURATION
REGION_NAME = config["study_area"]["region_name"]

COUNTY_NAME = config["study_area"]["county_name"]

TARGET_CRS = config["study_area"]["crs"]

RAW_DATA_DIR = Path(
    config["paths"]["raw_data"]
)

BOUNDARY_OUTPUT_DIR = (
    RAW_DATA_DIR /
    "boundaries"
)

BOUNDARY_OUTPUT_DIR.mkdir(
    parents=True,
    exist_ok=True
)

OUTPUT_FILE = (
    BOUNDARY_OUTPUT_DIR /
    f"{REGION_NAME}_boundary.geojson"
)

COUNTY_BOUNDARY_URL = (
    "https://www2.census.gov/geo/tiger/GENZ2023/shp/"
    "cb_2023_us_county_500k.zip"
)


# DOWNLOAD FUNCTION
def download_boundary(
    county_name=COUNTY_NAME,
    target_crs=TARGET_CRS,
    output_file=OUTPUT_FILE,
    diagnostics=True
):
    """
    Download and preprocess Butte County boundary.

    Returns
    -------
    boundary_gdf : geopandas.GeoDataFrame
    """
    
    # DOWNLOAD COUNTY DATA
    

    if diagnostics:
        print("\n===================================")
        print("DOWNLOADING COUNTY BOUNDARIES")
        print("===================================")

    counties = gpd.read_file(
        COUNTY_BOUNDARY_URL
    )

    # FILTER CALIFORNIA

    california = counties[
        counties["STATEFP"] == "06"
    ]

    # EXTRACT BUTTE COUNTY

    if diagnostics:
        print(f"\nExtracting: {county_name} County")

    boundary_gdf = california[
        california["NAME"] == county_name
    ]

    if boundary_gdf.empty:
        raise ValueError(
            f"County not found: {county_name}"
        )


    # REPROJECT
   
    if diagnostics:
        print(f"\nReprojecting to: {target_crs}")

    boundary_gdf = boundary_gdf.to_crs(
        target_crs
    )

    # SAVE

    if diagnostics:
        print("\nSaving boundary dataset...")

    boundary_gdf.to_file(
        output_file,
        driver="GeoJSON"
    )

    # SUMMARY

    if diagnostics:
        print("\n===================================")
        print("BOUNDARY DOWNLOAD COMPLETE")
        print("===================================")

        print(f"County: {county_name}")
        print(f"CRS: {boundary_gdf.crs}")
        print(f"Features: {len(boundary_gdf)}")
        print(f"Output: {output_file}")

    return boundary_gdf


# EXECUTE WORKFLOW

if __name__ == "__main__":

    butte_boundary = download_boundary()