"""
download_dem.py

Automated DEM download for Butte County,
California using Microsoft Planetary Computer.

This module:
- loads county boundary
- searches Copernicus DEM tiles
- mosaics DEM data
- exports DEM raster for preprocessing

Project:
GeoAI-Driven Wildfire Climate Risk Intelligence
and Community Vulnerability Modeling
for Butte County, California
"""

from pathlib import Path
import warnings

import geopandas as gpd
import planetary_computer
import rioxarray
import stackstac
import yaml
from pystac_client import Client as StacClient

warnings.filterwarnings("ignore")


# =========================================================
# LOAD CONFIGURATION
# =========================================================

CONFIG_PATH = "config/config.yaml"

with open(CONFIG_PATH, "r") as file:
    config = yaml.safe_load(file)


# =========================================================
# CONFIGURATION SETTINGS
# =========================================================

REGION_NAME = config["study_area"]["region_name"]

COUNTY_NAME = config["study_area"]["county_name"]

RAW_DATA_DIR = Path(
    config["paths"]["raw_data"]
)

BOUNDARY_PATH = (
    RAW_DATA_DIR /
    "boundaries" /
    f"{REGION_NAME}_boundary.geojson"
)

DEM_OUTPUT_DIR = (
    RAW_DATA_DIR /
    "dem"
)

DEM_OUTPUT_DIR.mkdir(
    parents=True,
    exist_ok=True
)

OUTPUT_FILE = (
    DEM_OUTPUT_DIR /
    f"{REGION_NAME}_dem.tif"
)

PLANETARY_COMPUTER_STAC = (
    "https://planetarycomputer.microsoft.com/api/stac/v1"
)


# =========================================================
# DEM DOWNLOAD FUNCTION
# =========================================================

def download_dem(
    boundary_path=BOUNDARY_PATH,
    output_file=OUTPUT_FILE,
    collection="cop-dem-glo-30",
    diagnostics=True
):

    # -----------------------------------------------------
    # LOAD COUNTY BOUNDARY
    # -----------------------------------------------------

    if diagnostics:
        print("\n===================================")
        print("LOADING COUNTY BOUNDARY")
        print("===================================")

    boundary = gpd.read_file(
        boundary_path
    )

    print(f"County: {COUNTY_NAME}")
    print(f"Boundary CRS: {boundary.crs}")

    # -----------------------------------------------------
    # CONVERT TO WGS84
    # -----------------------------------------------------

    boundary_wgs84 = boundary.to_crs(
        "EPSG:4326"
    )

    # -----------------------------------------------------
    # CONNECT TO STAC
    # -----------------------------------------------------

    if diagnostics:
        print("\n===================================")
        print("CONNECTING TO PLANETARY COMPUTER")
        print("===================================")

    catalog = StacClient.open(
        PLANETARY_COMPUTER_STAC,
        modifier=planetary_computer.sign_inplace
    )

    # -----------------------------------------------------
    # SEARCH DEM
    # -----------------------------------------------------

    search = catalog.search(
        collections=[collection],
        bbox=tuple(
            boundary_wgs84.total_bounds.tolist()
        )
    )

    items = list(search.items())

    if diagnostics:
        print(f"\nDEM tiles found: {len(items)}")

    # -----------------------------------------------------
    # LOAD DEM
    # -----------------------------------------------------

    stack = stackstac.stack(
        items,
        assets=["data"],
        bounds_latlon=tuple(
            boundary_wgs84.total_bounds.tolist()
        ),
        epsg=4326,
        chunksize=512,
        dtype="float64",
        rescale=False
    )

    # -----------------------------------------------------
    # MOSAIC DEM
    # -----------------------------------------------------

    if diagnostics:
        print("\nCreating DEM mosaic")

    dem = stack.max(dim="time").squeeze()

    # -----------------------------------------------------
    # ASSIGN CRS
    # -----------------------------------------------------

    dem = dem.rio.write_crs(
        "EPSG:4326"
    )

    # -----------------------------------------------------
    # SAVE DEM
    # -----------------------------------------------------

    if diagnostics:
        print("\nSaving DEM raster...")

    dem.rio.to_raster(
        output_file,
        tiled=True,
        compress="LZW",
        BIGTIFF="YES"
    )

    # -----------------------------------------------------
    # SUMMARY
    # -----------------------------------------------------

    if diagnostics:
        print("\n===================================")
        print("DEM DOWNLOAD COMPLETE")
        print("===================================")

        print(f"Output: {output_file}")
        print(f"CRS: {dem.rio.crs}")
        print(f"Shape: {dem.shape}")

    return dem


# =========================================================
# EXECUTE
# =========================================================

if __name__ == "__main__":

    butte_dem = download_dem()