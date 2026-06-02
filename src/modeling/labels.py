"""
labels.py

Create wildfire labels for Random Forest modeling.

Input:
    data/processed/reprojected/wildfire_3310.geojson
    data/processed/aligned/dem_aligned.tif

Output:
    data/training/labels.tif

Classes:
    0 = Unburned
    1 = Burned
"""

from pathlib import Path

import geopandas as gpd
import numpy as np
import rasterio
from rasterio.features import rasterize

# PATHS

PROJECT_ROOT = Path.cwd()

WILDFIRE_PATH = (
    PROJECT_ROOT /
    "data" /
    "processed" /
    "reprojected" /
    "wildfire_3310.geojson"
)

REFERENCE_RASTER = (
    PROJECT_ROOT /
    "data" /
    "processed" /
    "aligned" /
    "dem_aligned.tif"
)

OUTPUT_DIR = (
    PROJECT_ROOT /
    "data" /
    "training"
)

OUTPUT_DIR.mkdir(
    parents=True,
    exist_ok=True
)

OUTPUT_PATH = (
    OUTPUT_DIR /
    "labels.tif"
)

# LOAD WILDFIRE POLYGONS

print("\nLoading wildfire polygons")

wildfire = gpd.read_file(
    WILDFIRE_PATH
)

print(
    f"Wildfire polygons: {len(wildfire)}"
)

# LOAD REFERENCE RASTER

print("\nLoading reference raster")

with rasterio.open(
    REFERENCE_RASTER
) as src:

    profile = src.profile.copy()

    transform = src.transform

    height = src.height

    width = src.width

    crs = src.crs

print(f"CRS: {crs}")
print(f"Shape: ({height}, {width})")


# MATCH CRS

if wildfire.crs != crs:

    wildfire = wildfire.to_crs(
        crs
    )

# RASTERIZE

print("\nRasterizing wildfire history")

shapes = [

    (
        geometry,
        1
    )

    for geometry in wildfire.geometry

]

labels = rasterize(

    shapes=shapes,

    out_shape=(
        height,
        width
    ),

    transform=transform,

    fill=0,

    dtype="uint8"

)

# SAVE LABELS

profile.update(

    dtype=rasterio.uint8,

    count=1,

    nodata=None

)

with rasterio.open(

    OUTPUT_PATH,

    "w",

    **profile

) as dst:

    dst.write(
        labels,
        1
    )

print(
    f"\nSaved: {OUTPUT_PATH}"
)

# SUMMARY

unique, counts = np.unique(
    labels,
    return_counts=True
)

print("\n===================================")
print("LABEL CREATION COMPLETE")
print("===================================")

for value, count in zip(
    unique,
    counts
):

    if value == 0:

        print(
            f"Unburned pixels: {count:,}"
        )

    elif value == 1:

        print(
            f"Burned pixels: {count:,}"
        )