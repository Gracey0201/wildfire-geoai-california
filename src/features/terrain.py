"""
terrain.py

Generate terrain-based features:
- slope
- Topographic Wetness Index (TWI)

Input:
DEM aligned raster

Output:
- slope.tif
- twi.tif
"""

from pathlib import Path
import warnings

import numpy as np
import rasterio
from pysheds.grid import Grid

warnings.filterwarnings("ignore")


# =========================================================
# NUMPY COMPATIBILITY PATCH
# =========================================================

if not hasattr(np, "in1d"):

    np.in1d = np.isin


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

DEM_PATH = (
    INPUT_DIR /
    "dem_aligned.tif"
)


# =========================================================
# LOAD DEM
# =========================================================

with rasterio.open(DEM_PATH) as src:

    dem = src.read(1)

    profile = src.profile


# =========================================================
# GENERATE SLOPE
# =========================================================

print("\nGenerating slope")

x_gradient, y_gradient = np.gradient(
    dem,
    30,
    30
)

slope = np.degrees(

    np.arctan(

        np.sqrt(

            x_gradient**2 +
            y_gradient**2

        )

    )

)

profile.update(

    dtype=rasterio.float32,
    count=1

)

SLOPE_OUTPUT = (
    OUTPUT_DIR /
    "slope.tif"
)

with rasterio.open(

    SLOPE_OUTPUT,

    "w",

    **profile

) as dst:

    dst.write(

        slope.astype(
            rasterio.float32
        ),

        1

    )

print(f"Saved: {SLOPE_OUTPUT}")


# =========================================================
# GENERATE TWI
# =========================================================

print("\nGenerating TWI")

# ---------------------------------------------------------
# LOAD GRID
# ---------------------------------------------------------

grid = Grid.from_raster(
    str(DEM_PATH)
)

dem_raster = grid.read_raster(
    str(DEM_PATH)
)

# ---------------------------------------------------------
# FILL DEPRESSIONS
# ---------------------------------------------------------

flooded_dem = grid.fill_depressions(
    dem_raster
)

# ---------------------------------------------------------
# RESOLVE FLATS
# ---------------------------------------------------------

inflated_dem = grid.resolve_flats(
    flooded_dem
)

# ---------------------------------------------------------
# FLOW DIRECTION
# ---------------------------------------------------------

flowdir = grid.flowdir(
    inflated_dem
)

# ---------------------------------------------------------
# FLOW ACCUMULATION
# ---------------------------------------------------------

acc = grid.accumulation(
    flowdir
)

# ---------------------------------------------------------
# TWI CALCULATION
# ---------------------------------------------------------

slope_radians = np.radians(
    slope
)

slope_radians[
    slope_radians == 0
] = 0.001

twi = np.log(

    (
        acc + 1
    ) /

    np.tan(
        slope_radians
    )

)

# ---------------------------------------------------------
# SAVE TWI
# ---------------------------------------------------------

TWI_OUTPUT = (
    OUTPUT_DIR /
    "twi.tif"
)

with rasterio.open(

    TWI_OUTPUT,

    "w",

    **profile

) as dst:

    dst.write(

        twi.astype(
            rasterio.float32
        ),

        1

    )

print(f"Saved: {TWI_OUTPUT}")


# =========================================================
# COMPLETE
# =========================================================

print("\n===================================")
print("TERRAIN FEATURES COMPLETE")
print("===================================")