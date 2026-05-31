"""
landcover.py

Download Impact Observatory Annual
Land Use/Land Cover (IO-LULC)
data for wildfire susceptibility
and exposure modeling.

Dataset:
Impact Observatory Annual Land Use/Land Cover

Collection:
io-lulc-annual-v02

Class Definitions
-----------------
1  = Water
2  = Trees
4  = Flooded Vegetation
5  = Crops
7  = Built Area
8  = Bare Ground
9  = Snow/Ice
11 = Rangeland

Important:
-----------
Built Area = 7

This class should be used for:
- distance_to_settlements
- developed_land
- exposure analysis
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
# SETTINGS
# =========================================================

RAW_DATA_DIR = Path(
    config["paths"]["raw_data"]
)

BOUNDARY_PATH = (
    RAW_DATA_DIR /
    "boundaries" /
    "boundary.geojson"
)

LANDCOVER_OUTPUT_DIR = (
    RAW_DATA_DIR /
    "landcover"
)

LANDCOVER_OUTPUT_DIR.mkdir(
    parents=True,
    exist_ok=True
)

OUTPUT_FILE = (
    LANDCOVER_OUTPUT_DIR /
    "landcover.tif"
)

PLANETARY_COMPUTER_STAC = (
    "https://planetarycomputer.microsoft.com/api/stac/v1"
)

LULC_COLLECTION = (
    "io-lulc-annual-v02"
)


# =========================================================
# DOWNLOAD FUNCTION
# =========================================================

def download_landcover(
    boundary_path=BOUNDARY_PATH,
    output_file=OUTPUT_FILE,
    diagnostics=True
):
    """
    Download Impact Observatory
    Annual Land Use/Land Cover raster.
    """

    # -----------------------------------------------------
    # LOAD BOUNDARY
    # -----------------------------------------------------

    if diagnostics:

        print("\n===================================")
        print("LOADING STUDY AREA BOUNDARY")
        print("===================================")

    boundary = gpd.read_file(
        boundary_path
    )

    boundary_wgs84 = boundary.to_crs(
        "EPSG:4326"
    )

    bbox = tuple(
        boundary_wgs84.total_bounds
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
    # SEARCH DATA
    # -----------------------------------------------------

    search = catalog.search(
        collections=[LULC_COLLECTION],
        bbox=bbox
    )

    items = list(
        search.items()
    )

    if diagnostics:

        print(
            f"\nTiles found: {len(items)}"
        )

    if len(items) == 0:

        raise ValueError(
            "No landcover tiles found."
        )

    # -----------------------------------------------------
    # LOAD MOSAIC
    # -----------------------------------------------------

    if diagnostics:

        print(
            "\nLoading landcover raster"
        )

    stack = stackstac.stack(
        items,
        assets=["data"],
        bounds_latlon=bbox,
        epsg=4326,
        chunksize=512,
        dtype="float64",
        rescale=False
    )

    landcover = (
        stack
        .max(dim="time")
        .squeeze()
    )

    landcover = landcover.rio.write_crs(
        "EPSG:4326"
    )

    # -----------------------------------------------------
    # SAVE
    # -----------------------------------------------------

    if diagnostics:

        print(
            "\nSaving raster..."
        )

    landcover.rio.to_raster(
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
        print("LANDCOVER DOWNLOAD COMPLETE")
        print("===================================")

        print(
            "Dataset: Impact Observatory LULC"
        )

        print(
            f"Collection: {LULC_COLLECTION}"
        )

        print(
            f"Output: {output_file}"
        )

        print(
            f"CRS: {landcover.rio.crs}"
        )

        print(
            f"Shape: {landcover.shape}"
        )

        print(
            "\nBuilt Area Class: 7"
        )

    return landcover


# =========================================================
# EXECUTE
# =========================================================

if __name__ == "__main__":

    landcover = download_landcover()