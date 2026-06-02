"""
precipitation.py

Download and process observed precipitation
data for wildfire susceptibility modeling.

Source:
Livneh VIC Output Dataset
University of Colorado Boulder

Dataset:
https://albers.cnr.berkeley.edu/data/scripps/livneh_vic-output/

This module:
- downloads precipitation NetCDF files
- filters years 2000–2013
- computes annual precipitation means
- computes long-term precipitation climatology
- exports standardized precipitation raster
"""

from pathlib import Path
import warnings
import requests

import xarray as xr
import rioxarray
import yaml

warnings.filterwarnings("ignore")


# LOAD CONFIGURATION

CONFIG_PATH = "config/config.yaml"

with open(CONFIG_PATH, "r") as file:
    config = yaml.safe_load(file)


# CONFIGURATION SETTINGS
REGION_NAME = config["study_area"]["region_name"]

RAW_DATA_DIR = Path(
    config["paths"]["raw_data"]
)

CLIMATE_DIR = (
    RAW_DATA_DIR /
    "climate"
)

CLIMATE_DIR.mkdir(
    parents=True,
    exist_ok=True
)

OUTPUT_FILE = (
    CLIMATE_DIR /
    f"{REGION_NAME}_precipitation.tif"
)

# LIVNEH DATASET BASE URL
BASE_URL = (
    "https://albers.cnr.berkeley.edu/"
    "data/scripps/livneh_vic-output/"
)

# YEARS TO DOWNLOAD
YEARS = list(
    range(2000, 2014)
)


# DOWNLOAD FILES

def download_precip_files(
    output_dir=CLIMATE_DIR,
    diagnostics=True
):
    """
    Download precipitation NetCDF files.
    """

    downloaded_files = []

    for year in YEARS:

        filename = (
            f"precip.{year}.v0.nc"
        )

        url = BASE_URL + filename

        output_path = (
            output_dir / filename
        )

        # SKIP EXISTING FILES

        if output_path.exists():

            if diagnostics:
                print(
                    f"\nAlready exists: "
                    f"{filename}"
                )

            downloaded_files.append(
                output_path
            )

            continue

        # DOWNLOAD FILE

        if diagnostics:
            print(
                f"\nDownloading: "
                f"{filename}"
            )

        response = requests.get(
            url,
            stream=True
        )

        response.raise_for_status()

        with open(
            output_path,
            "wb"
        ) as file:

            for chunk in response.iter_content(
                chunk_size=8192
            ):
                file.write(chunk)

        downloaded_files.append(
            output_path
        )

    return downloaded_files

# PROCESS PRECIPITATION
def download_precipitation(
    diagnostics=True
):
    """
    Download and process precipitation data.
    """

    # START WORKFLOW

    if diagnostics:

        print("\n===================================")
        print("DOWNLOADING PRECIPITATION DATA")
        print("===================================")

    # DOWNLOAD FILES

    precip_files = download_precip_files()

    # PROCESS FILES

    annual_means = []

    for file in precip_files:

        year = int(
            file.name.split(".")[1]
        )

        if diagnostics:
            print(f"\nProcessing year: {year}")

        # OPEN DATASET

        ds = xr.open_dataset(file)

        # EXTRACT PRECIP VARIABLE

        precipitation = ds["precip"]

        # COMPUTE ANNUAL MEAN

        annual_mean = precipitation.mean(
            dim="Time"
        )

        annual_means.append(
            annual_mean
        )

    # STACK YEARS
    precipitation_stack = xr.concat(
        annual_means,
        dim="year"
    )

    # COMPUTE LONG-TERM MEAN

    precipitation_mean = (
        precipitation_stack
        .mean(dim="year")
    )

    # ASSIGN CRS

    precipitation_mean = (
        precipitation_mean
        .rio.write_crs("EPSG:4326")
    )

    # SAVE OUTPUT

    if diagnostics:
        print("\nSaving precipitation raster")

    precipitation_mean.rio.to_raster(
        OUTPUT_FILE,
        compress="LZW",
        tiled=True
    )

    # SUMMARY

    if diagnostics:

        print("\n===================================")
        print("PRECIPITATION COMPLETE")
        print("===================================")

        print(f"\nOutput: {OUTPUT_FILE}")

        print(
            f"\nCRS: "
            f"{precipitation_mean.rio.crs}"
        )

        print(
            f"\nShape: "
            f"{precipitation_mean.shape}"
        )

    return precipitation_mean


# EXECUTE WORKFLOW

if __name__ == "__main__":

    precipitation = (
        download_precipitation()
    )