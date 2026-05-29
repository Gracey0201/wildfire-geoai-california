"""
distance.py

Generate:
- distance to roads
- distance to settlements

Input:
- roads vector
- aligned landcover raster

Output:
- distance_to_roads.tif
- distance_to_settlements.tif
"""

from pathlib import Path
import warnings

import geopandas as gpd
import numpy as np
import rasterio
from rasterio.features import rasterize
from scipy.ndimage import distance_transform_edt

warnings.filterwarnings("ignore")


# =========================================================
# PATHS
# =========================================================

ALIGNED_DIR = Path(
    "data/processed/aligned"
)

VECTOR_DIR = Path(
    "data/processed/reprojected"
)

OUTPUT_DIR = Path(
    "data/features"
)

OUTPUT_DIR.mkdir(
    parents=True,
    exist_ok=True
)


# =========================================================
# REFERENCE RASTER
# =========================================================

REFERENCE_RASTER = (
    ALIGNED_DIR /
    "dem_aligned.tif"
)

with rasterio.open(
    REFERENCE_RASTER
) as src:

    profile = src.profile

    shape = src.shape

    transform = src.transform


# =========================================================
# DISTANCE TO ROADS
# =========================================================

print("\nGenerating distance to roads")

roads = gpd.read_file(

    VECTOR_DIR /
    "roads_3310.geojson"

)

road_raster = rasterize(

    [
        (geom, 1)

        for geom in roads.geometry
    ],

    out_shape=shape,

    transform=transform,

    fill=0,

    dtype="uint8"

)

distance_roads = distance_transform_edt(
    1 - road_raster
) * 30

DISTANCE_ROADS_OUTPUT = (
    OUTPUT_DIR /
    "distance_to_roads.tif"
)

profile.update(
    dtype=rasterio.float32,
    count=1
)

with rasterio.open(

    DISTANCE_ROADS_OUTPUT,

    "w",

    **profile

) as dst:

    dst.write(

        distance_roads.astype(
            rasterio.float32
        ),

        1

    )

print(f"Saved: {DISTANCE_ROADS_OUTPUT}")


# =========================================================
# DISTANCE TO SETTLEMENTS
# =========================================================

print("\nGenerating distance to settlements")

LULC_PATH = (
    ALIGNED_DIR /
    "landcover_aligned.tif"
)

with rasterio.open(
    LULC_PATH
) as src:

    lulc = src.read(1)


settlements = np.isin(

    lulc,

    [21, 22, 23, 24]

).astype("uint8")


distance_settlements = distance_transform_edt(

    1 - settlements

) * 30


DISTANCE_SETTLEMENTS_OUTPUT = (
    OUTPUT_DIR /
    "distance_to_settlements.tif"
)

with rasterio.open(

    DISTANCE_SETTLEMENTS_OUTPUT,

    "w",

    **profile

) as dst:

    dst.write(

        distance_settlements.astype(
            rasterio.float32
        ),

        1

    )

print(f"Saved: {DISTANCE_SETTLEMENTS_OUTPUT}")


# =========================================================
# COMPLETE
# =========================================================

print("\n===================================")
print("DISTANCE FEATURES COMPLETE")
print("===================================")