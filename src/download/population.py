"""
population.py

Download and process Census population data
for wildfire exposure analysis.

Source:
U.S. Census ACS 5-Year Estimates

This module:
- downloads census tract boundaries
- requests ACS population data
- joins population to tracts
- calculates population density
- exports GeoJSON

Output:
Population exposure layer
"""

from pathlib import Path
import warnings

import geopandas as gpd
import pandas as pd
import requests
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

RAW_DATA_DIR = Path(
    config["paths"]["raw_data"]
)

# ---------------------------------------------------------
# OUTPUT DIRECTORY
# ---------------------------------------------------------

OUTPUT_DIR = (
    RAW_DATA_DIR /
    "population"
)

OUTPUT_DIR.mkdir(
    parents=True,
    exist_ok=True
)

# ---------------------------------------------------------
# OUTPUT FILE
# ---------------------------------------------------------

OUTPUT_FILE = (
    OUTPUT_DIR /
    f"{REGION_NAME}_population.geojson"
)

# ---------------------------------------------------------
# ACS SETTINGS
# ---------------------------------------------------------

ACS_YEAR = "2022"

STATE_FIPS = "06"     # California
COUNTY_FIPS = "007"   # Butte County

# ---------------------------------------------------------
# CENSUS API KEY
# ---------------------------------------------------------

CENSUS_API_KEY = (
    "b08f9a8b1bdafc071dc38c30ce6afe2d08350acf"
)

# ---------------------------------------------------------
# TRACT SHAPEFILE URL
# ---------------------------------------------------------

TRACT_URL = (
    "https://www2.census.gov/geo/tiger/"
    "TIGER2022/TRACT/"
    "tl_2022_06_tract.zip"
)


# =========================================================
# DOWNLOAD POPULATION DATA
# =========================================================

def download_population(
    diagnostics=True
):
    """
    Download census population data.

    Parameters
    ----------
    diagnostics : bool
        Print workflow diagnostics.

    Returns
    -------
    population_gdf : GeoDataFrame
        Population exposure layer.
    """

    # -----------------------------------------------------
    # START WORKFLOW
    # -----------------------------------------------------

    if diagnostics:

        print("\n===================================")
        print("DOWNLOADING POPULATION DATA")
        print("===================================")

    # -----------------------------------------------------
    # DOWNLOAD TRACTS
    # -----------------------------------------------------

    if diagnostics:
        print("\nDownloading census tracts")

    tracts = gpd.read_file(
        TRACT_URL
    )

    # -----------------------------------------------------
    # FILTER TO BUTTE COUNTY
    # -----------------------------------------------------

    tracts = tracts[
        tracts["COUNTYFP"] == COUNTY_FIPS
    ]

    # -----------------------------------------------------
    # ACS VARIABLE
    # -----------------------------------------------------

    variable = "B01003_001E"

    # -----------------------------------------------------
    # BUILD URL
    # -----------------------------------------------------

    url = (
        f"https://api.census.gov/data/"
        f"{ACS_YEAR}/acs/acs5"
        f"?get={variable}"
        f"&for=tract:*"
        f"&in=state:{STATE_FIPS}"
        f"&in=county:{COUNTY_FIPS}"
        f"&key={CENSUS_API_KEY}"
    )

    if diagnostics:

        print("\nRequesting population data")
        print("\nACS URL:")
        print(url)

    # -----------------------------------------------------
    # REQUEST HEADERS
    # -----------------------------------------------------

    headers = {

        "User-Agent":
        "wildfire-geoai-project"

    }

    # -----------------------------------------------------
    # REQUEST DATA
    # -----------------------------------------------------

    response = requests.get(
        url,
        headers=headers,
        timeout=60
    )

    # -----------------------------------------------------
    # DEBUG RESPONSE
    # -----------------------------------------------------

    print("\nSTATUS CODE:")
    print(response.status_code)

    print("\nFULL RESPONSE:")
    print(response.text[:1000])

    # -----------------------------------------------------
    # CHECK STATUS
    # -----------------------------------------------------

    response.raise_for_status()

    # -----------------------------------------------------
    # CONVERT TO JSON
    # -----------------------------------------------------

    data_json = response.json()

    # -----------------------------------------------------
    # CREATE DATAFRAME
    # -----------------------------------------------------

    population_df = pd.DataFrame(
        data_json[1:],
        columns=data_json[0]
    )

    # -----------------------------------------------------
    # CREATE GEOID
    # -----------------------------------------------------

    population_df["GEOID"] = (

        population_df["state"] +
        population_df["county"] +
        population_df["tract"]

    )

    # -----------------------------------------------------
    # RENAME COLUMN
    # -----------------------------------------------------

    population_df = population_df.rename(
        columns={
            "B01003_001E":
            "population"
        }
    )

    # -----------------------------------------------------
    # CONVERT TO NUMERIC
    # -----------------------------------------------------

    population_df["population"] = pd.to_numeric(
        population_df["population"],
        errors="coerce"
    )

    # -----------------------------------------------------
    # JOIN TO TRACTS
    # -----------------------------------------------------

    if diagnostics:
        print("\nJoining population to tracts")

    population_gdf = tracts.merge(
        population_df,
        on="GEOID",
        how="left"
    )

    # -----------------------------------------------------
    # PROJECT TO EPSG:3310
    # -----------------------------------------------------

    population_gdf = (
        population_gdf
        .to_crs("EPSG:3310")
    )

    # -----------------------------------------------------
    # AREA
    # -----------------------------------------------------

    population_gdf["area_km2"] = (

        population_gdf.geometry.area /

        1_000_000

    )

    # -----------------------------------------------------
    # POPULATION DENSITY
    # -----------------------------------------------------

    population_gdf["population_density"] = (

        population_gdf["population"] /

        population_gdf["area_km2"]

    )

    # -----------------------------------------------------
    # KEEP IMPORTANT COLUMNS
    # -----------------------------------------------------

    keep_columns = [

        "GEOID",
        "NAME",

        "population",

        "population_density",

        "geometry"

    ]

    population_gdf = (
        population_gdf[
            keep_columns
        ]
    )

    # -----------------------------------------------------
    # SAVE OUTPUT
    # -----------------------------------------------------

    if diagnostics:
        print("\nSaving population layer")

    population_gdf.to_file(
        OUTPUT_FILE,
        driver="GeoJSON"
    )

    # -----------------------------------------------------
    # SUMMARY
    # -----------------------------------------------------

    if diagnostics:

        print("\n===================================")
        print("POPULATION DOWNLOAD COMPLETE")
        print("===================================")

        print(
            f"\nCensus tracts: "
            f"{len(population_gdf)}"
        )

        print(
            f"\nCRS: "
            f"{population_gdf.crs}"
        )

        print(
            f"\nOutput: "
            f"{OUTPUT_FILE}"
        )

    return population_gdf


# =========================================================
# EXECUTE WORKFLOW
# =========================================================

if __name__ == "__main__":

    population = (
        download_population()
    )