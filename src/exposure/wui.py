"""
wui.py

Create a Wildland-Urban Interface (WUI) raster.

Definition:

Built Area located within
500 meters of Trees or Shrubland.

Input:
- developed_land.tif
- landcover_aligned.tif

Output:
- wui.tif
"""

from pathlib import Path
import warnings

import numpy as np
import rasterio
from scipy.ndimage import distance_transform_edt

warnings.filterwarnings("ignore")


# PATHS

FEATURE_DIR = Path(
    "data/features"
)

ALIGNED_DIR = Path(
    "data/processed/aligned"
)

DEVELOPED_PATH = (
    FEATURE_DIR /
    "developed_land.tif"
)

LANDCOVER_PATH = (
    ALIGNED_DIR /
    "landcover_aligned.tif"
)

OUTPUT_PATH = (
    FEATURE_DIR /
    "wui.tif"
)


# LOAD DEVELOPED LAND

print(
    "\nLoading developed land"
)

with rasterio.open(
    DEVELOPED_PATH
) as src:

    developed = src.read(1)

    profile = src.profile.copy()

    developed_nodata = src.nodata


# LOAD LANDCOVER
print(
    "\nLoading landcover"
)

with rasterio.open(
    LANDCOVER_PATH
) as src:

    landcover = src.read(1)

    lc_nodata = src.nodata


# VEGETATION MASK

print(
    "\nCreating vegetation mask"
)

# Impact Observatory Classes
#
# 1 = Trees
# 2 = Shrubland
# 5 = Grassland
# 7 = Built Area
#
# For wildfire WUI, use only
# Trees and Shrubland.

vegetation = np.isin(

    landcover,

    [
        1,  # Trees
        2   # Shrubland
    ]

).astype(
    np.uint8
)

# Remove landcover nodata

if lc_nodata is not None:

    vegetation[
        landcover == lc_nodata
    ] = 0

# DISTANCE TO VEGETATION

print(
    "\nCalculating distance to vegetation"
)

distance = distance_transform_edt(

    1 - vegetation

) * 30

# WUI DEFINITION

print(
    "\nCreating WUI raster"
)

# WUI =
# Built Area within 500 m
# of Trees or Shrubland

wui = np.where(

    (
        developed == 1
    )

    &

    (
        distance <= 500
    ),

    1,

    0

).astype(
    np.uint8
)


# PRESERVE NODATA

if developed_nodata is not None:

    wui[
        developed == developed_nodata
    ] = 255


# SAVE OUTPUT

profile.update(

    dtype=rasterio.uint8,

    count=1,

    nodata=255

)

with rasterio.open(

    OUTPUT_PATH,

    "w",

    **profile

) as dst:

    dst.write(
        wui,
        1
    )

print(
    f"Saved: {OUTPUT_PATH}"
)


# SUMMARY

wui_pixels = np.sum(
    wui == 1
)

non_wui_pixels = np.sum(
    wui == 0
)

print("\n===================================")
print("WUI COMPLETE")
print("===================================")

print(
    f"WUI pixels: "
    f"{wui_pixels:,}"
)

print(
    f"Non-WUI pixels: "
    f"{non_wui_pixels:,}"
)

print(
    f"\nOutput:"
)

print(
    OUTPUT_PATH
)