"""
roads.py

Download road network data for
wildfire susceptibility modeling.

This module:
- downloads OpenStreetMap road data
- clips roads to study area boundary
- exports raw road network dataset

The dataset is intentionally preserved
in raw form for downstream preprocessing.
"""

from pathlib import Path
import warnings

import geopandas as gpd
import osmnx as ox
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

# INPUT BOUNDARY
BOUNDARY_PATH = (
    RAW_DATA_DIR /
    "boundaries" /
    f"{REGION_NAME}_boundary.geojson"
)

# OUTPUT DIRECTORY

OUTPUT_DIR = (
    RAW_DATA_DIR /
    "roads"
)

OUTPUT_DIR.mkdir(
    parents=True,
    exist_ok=True
)

OUTPUT_FILE = (
    OUTPUT_DIR /
    f"{REGION_NAME}_roads.geojson"
)


# DOWNLOAD ROAD DATA

def download_roads(
    boundary_path=BOUNDARY_PATH,
    output_file=OUTPUT_FILE,
    diagnostics=True
):
    """
    Download OpenStreetMap roads.

    Parameters
    ----------
    boundary_path : str or pathlib.Path
        Study area boundary path.

    output_file : str or pathlib.Path
        Output road dataset path.

    diagnostics : bool
        If True, print workflow diagnostics.

    Returns
    -------
    roads_gdf : geopandas.GeoDataFrame
        Road network dataset.
    """

    # LOAD STUDY AREA

    if diagnostics:

        print("\n===================================")
        print("LOADING STUDY AREA BOUNDARY")
        print("===================================")

    boundary = gpd.read_file(
        boundary_path
    )

    print(f"\nBoundary CRS: {boundary.crs}")

    # CONVERT TO WGS84

    boundary_wgs84 = boundary.to_crs(
        "EPSG:4326"
    )

    # EXTRACT GEOMETRY

    polygon = (
        boundary_wgs84.geometry.iloc[0]
    )

    # DOWNLOAD ROAD NETWORK

    if diagnostics:

        print("\n===================================")
        print("DOWNLOADING ROAD NETWORK")
        print("===================================")

    graph = ox.graph_from_polygon(
        polygon,
        network_type="drive"
    )

    # CONVERT TO GEODATAFRAME

    roads_gdf = ox.graph_to_gdfs(
        graph,
        nodes=False,
        edges=True
    )

    # KEEP IMPORTANT COLUMNS

    keep_columns = [
        "highway",
        "name",
        "geometry"
    ]

    existing_columns = [

        col

        for col in keep_columns

        if col in roads_gdf.columns

    ]

    roads_gdf = roads_gdf[
        existing_columns
    ]

    # RESET INDEX

    roads_gdf = roads_gdf.reset_index(
        drop=True
    )

    # SAVE OUTPUT

    if diagnostics:
        print("\nSaving road dataset")

    roads_gdf.to_file(
        output_file,
        driver="GeoJSON"
    )

    # SUMMARY

    if diagnostics:

        print("\n===================================")
        print("ROAD DOWNLOAD COMPLETE")
        print("===================================")

        print(
            f"\nRoad segments: "
            f"{len(roads_gdf)}"
        )

        print(
            f"\nCRS: "
            f"{roads_gdf.crs}"
        )

        print(
            f"\nOutput: "
            f"{output_file}"
        )

    return roads_gdf


# EXECUTE WORKFLOW

if __name__ == "__main__":

    roads = (
        download_roads()
    )