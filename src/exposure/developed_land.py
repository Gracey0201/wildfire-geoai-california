"""
developed_land.py

Create a developed land raster
for wildfire exposure analysis.

Input:
- landcover_aligned.tif

Output:
- developed_land.tif

Impact Observatory LULC Classes
-------------------------------
1  = Water
2  = Trees
4  = Flooded Vegetation
5  = Crops
7  = Built Area
8  = Bare Ground
9  = Snow/Ice
11 = Rangeland

Built Area (7) is used as a proxy
for developed land and human exposure.
"""

from pathlib import Path
import warnings

import numpy as np
import rasterio

warnings.filterwarnings("ignore")


# =========================================================
# PATHS
# =========================================================

INPUT_DIR = Path(
    "data/processed/aligned"
)

OUTPUT_DIR = Path(
    "data/features"
)

OUTPUT_DIR.mkdir(
    parents=True,
    exist_ok=True
)

LANDCOVER_PATH = (
    INPUT_DIR /
    "landcover_aligned.tif"
)

OUTPUT_PATH = (
    OUTPUT_DIR /
    "developed_land.tif"
)


# =========================================================
# LOAD LANDCOVER
# =========================================================

print("\nLoading land cover raster")

with rasterio.open(
    LANDCOVER_PATH
) as src:

    landcover = src.read(1)

    profile = src.profile.copy()

    nodata = src.nodata


# =========================================================
# CREATE DEVELOPED LAND MASK
# =========================================================

print("\nCreating developed land raster")

# Impact Observatory LULC
# Built Area = 7

developed = np.isin(

    landcover,

    [7]

).astype(
    np.uint8
)


# =========================================================
# PRESERVE NODATA
# =========================================================

if nodata is not None:

    developed[
        landcover == nodata
    ] = 255


# =========================================================
# UPDATE PROFILE
# =========================================================

profile.update(

    dtype=rasterio.uint8,

    count=1,

    nodata=255

)


# =========================================================
# SAVE OUTPUT
# =========================================================

with rasterio.open(

    OUTPUT_PATH,

    "w",

    **profile

) as dst:

    dst.write(

        developed,

        1

    )

print(
    f"Saved: {OUTPUT_PATH}"
)


# =========================================================
# SUMMARY
# =========================================================

developed_pixels = np.sum(
    developed == 1
)

undeveloped_pixels = np.sum(
    developed == 0
)

print("\n===================================")
print("DEVELOPED LAND COMPLETE")
print("===================================")

print(
    f"Developed pixels: "
    f"{developed_pixels:,}"
)

print(
    f"Undeveloped pixels: "
    f"{undeveloped_pixels:,}"
)

print(
    f"\nOutput:"
)

print(
    OUTPUT_PATH
)