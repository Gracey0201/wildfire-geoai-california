"""
landcover.py

Download NLCD land cover data for
wildfire susceptibility modeling.

This module:
- downloads NLCD land cover data
- loads raster data using stackstac
- exports raw land cover raster

The dataset is intentionally preserved
in raw form for downstream preprocessing.
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

RAW_DATA_DIR = Path(
    config["paths"]["raw_data"]
)

BOUNDARY_PATH = (
    RAW_DATA_DIR /
    "boundaries" /
    f"{REGION_NAME}_boundary.geojson"
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
    f"{REGION_NAME}_nlcd_landcover.tif"
)

PLANETARY_COMPUTER_STAC = (
    "https://planetarycomputer.microsoft.com/api/stac/v1"
)

NLCD_COLLECTION = (
    "io-lulc-annual-v02"
)


# =========================================================
# DOWNLOAD FUNCTION
# =========================================================

def download_landcover(
    boundary_path=BOUNDARY_PATH,
    output_file=OUTPUT_FILE,
    collection=NLCD_COLLECTION,
    diagnostics=True
):
    """
    Download NLCD land cover raster.

    Parameters
    ----------
    boundary_path : str or pathlib.Path
        Study area boundary path.

    output_file : str or pathlib.Path
        Output raster path.

    collection : str
        Planetary Computer collection name.

    diagnostics : bool
        If True, print workflow diagnostics.

    Returns
    -------
    landcover : xarray.DataArray
        Raw land cover raster.
    """

    # -----------------------------------------------------
    # LOAD STUDY AREA BOUNDARY
    # -----------------------------------------------------

    if diagnostics:
        print("\n===================================")
        print("LOADING COUNTY BOUNDARY")
        print("===================================")

    boundary = gpd.read_file(
        boundary_path
    )

    print(f"Boundary CRS: {boundary.crs}")

    # -----------------------------------------------------
    # CONVERT TO WGS84
    # -----------------------------------------------------

    boundary_wgs84 = boundary.to_crs(
        "EPSG:4326"
    )

    bbox = tuple(
        boundary_wgs84.total_bounds.tolist()
    )

    # -----------------------------------------------------
    # CONNECT TO PLANETARY COMPUTER
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
    # SEARCH NLCD
    # -----------------------------------------------------

    search = catalog.search(
        collections=[collection],
        bbox=bbox
    )

    items = list(search.items())

    if diagnostics:
        print(
            f"\nLand cover tiles found: "
            f"{len(items)}"
        )

    # -----------------------------------------------------
    # LOAD LAND COVER DATA
    # -----------------------------------------------------

    if diagnostics:
        print("\nLoading land cover raster")

    stack = stackstac.stack(
        items,
        assets=["data"],
        bounds_latlon=bbox,
        epsg=4326,
        chunksize=512,
        dtype="float64",
        rescale=False
    )

    # -----------------------------------------------------
    # CREATE MOSAIC
    # -----------------------------------------------------

    landcover = (
        stack
        .max(dim="time")
        .squeeze()
    )

    # -----------------------------------------------------
    # ASSIGN CRS
    # -----------------------------------------------------

    landcover = landcover.rio.write_crs(
        "EPSG:4326"
    )

    # -----------------------------------------------------
    # SAVE RASTER
    # -----------------------------------------------------

    if diagnostics:
        print("\nSaving land cover raster...")

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
        print("LAND COVER DOWNLOAD COMPLETE")
        print("===================================")

        print(f"Output: {output_file}")

        print(f"CRS: {landcover.rio.crs}")

        print(f"Shape: {landcover.shape}")

    return landcover


# =========================================================
# EXECUTE WORKFLOW
# =========================================================

if __name__ == "__main__":

    landcover = download_landcover()