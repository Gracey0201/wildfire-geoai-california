"""
wildfire.py

Download California historical wildfire
perimeter data from CAL FIRE FRAP.

This module:
- downloads California fire perimeter data
- filters wildfire perimeters by year
- exports raw wildfire perimeter dataset

The dataset is intentionally preserved
in raw form for downstream preprocessing.
"""

from pathlib import Path
import warnings
import requests

import geopandas as gpd
import yaml

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

START_YEAR = config["study_area"]["analysis_years"]["start"]

END_YEAR = config["study_area"]["analysis_years"]["end"]

RAW_DATA_DIR = Path(
    config["paths"]["raw_data"]
)

WILDFIRE_OUTPUT_DIR = (
    RAW_DATA_DIR /
    "wildfire"
)

WILDFIRE_OUTPUT_DIR.mkdir(
    parents=True,
    exist_ok=True
)

OUTPUT_FILE = (
    WILDFIRE_OUTPUT_DIR /
    f"{REGION_NAME}_wildfire_history.geojson"
)

# ---------------------------------------------------------
# TEMP DIRECTORY
# ---------------------------------------------------------

TEMP_DIR = Path(
    "data/temp"
)

TEMP_DIR.mkdir(
    parents=True,
    exist_ok=True
)

GEOJSON_PATH = (
    TEMP_DIR /
    "calfire_fire_perimeters.geojson"
)

# ---------------------------------------------------------
# CAL FIRE DATASET
# ---------------------------------------------------------

CALFIRE_URL = (
    "https://gis.data.ca.gov/datasets/"
    "CALFIRE-Forestry::california-fire-perimeters-1950.geojson"
)


# =========================================================
# DOWNLOAD FUNCTION
# =========================================================

def download_wildfire_history(
    wildfire_url=CALFIRE_URL,
    output_file=OUTPUT_FILE,
    diagnostics=True
):
    """
    Download CAL FIRE wildfire perimeter data.

    Parameters
    ----------
    wildfire_url : str
        CAL FIRE GeoJSON download URL.

    output_file : str or pathlib.Path
        Output wildfire dataset path.

    diagnostics : bool
        If True, print workflow diagnostics.

    Returns
    -------
    wildfire_gdf : geopandas.GeoDataFrame
        Raw wildfire perimeter dataset.
    """

    # -----------------------------------------------------
    # DOWNLOAD DATASET
    # -----------------------------------------------------

    if diagnostics:
        print("\n===================================")
        print("DOWNLOADING WILDFIRE DATA")
        print("===================================")

        print("\nDownloading CAL FIRE dataset")

    response = requests.get(
        wildfire_url,
        stream=True
    )

    response.raise_for_status()

    with open(
        GEOJSON_PATH,
        "wb"
    ) as file:

        for chunk in response.iter_content(
            chunk_size=8192
        ):
            file.write(chunk)

    # -----------------------------------------------------
    # READ DATASET
    # -----------------------------------------------------

    wildfire_gdf = gpd.read_file(
        GEOJSON_PATH
    )

    if diagnostics:
        print(
            f"\nWildfire records downloaded: "
            f"{len(wildfire_gdf)}"
        )

    # -----------------------------------------------------
    # FILTER YEARS
    # -----------------------------------------------------

    possible_year_fields = [
        "YEAR_",
        "YEAR",
        "FIRE_YEAR",
        "FIRE_YEAR_",
        "ALARM_DATE"
    ]

    year_field = None

    for field in possible_year_fields:

        if field in wildfire_gdf.columns:

            year_field = field

            break

    if year_field:

        wildfire_gdf["YEAR_FILTER"] = (
            wildfire_gdf[year_field]
            .astype(str)
            .str[:4]
        )

        wildfire_gdf["YEAR_FILTER"] = (
            wildfire_gdf["YEAR_FILTER"]
            .astype("Int64")
        )

        wildfire_gdf = wildfire_gdf[
            (
                wildfire_gdf["YEAR_FILTER"]
                >= START_YEAR
            )
            &
            (
                wildfire_gdf["YEAR_FILTER"]
                <= END_YEAR
            )
        ]

    # -----------------------------------------------------
    # SAVE DATASET
    # -----------------------------------------------------

    if diagnostics:
        print("\nSaving wildfire dataset...")

    wildfire_gdf.to_file(
        output_file,
        driver="GeoJSON"
    )

    # -----------------------------------------------------
    # SUMMARY
    # -----------------------------------------------------

    if diagnostics:
        print("\n===================================")
        print("WILDFIRE DOWNLOAD COMPLETE")
        print("===================================")

        print(
            f"Wildfire records: "
            f"{len(wildfire_gdf)}"
        )

        print(f"CRS: {wildfire_gdf.crs}")

        print(f"Output: {output_file}")

    return wildfire_gdf


# =========================================================
# EXECUTE WORKFLOW
# =========================================================

if __name__ == "__main__":

    wildfire_history = (
        download_wildfire_history()
    )