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

with rasterio.open(
    DEM_PATH
) as src:

    dem = src.read(1).astype(
        np.float32
    )

    profile = src.profile.copy()

    nodata = src.nodata


# =========================================================
# CREATE COUNTY MASK
# =========================================================

mask = (
    dem == nodata
)

dem[mask] = np.nan


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

# restore county mask

slope[mask] = -9999


# =========================================================
# SAVE SLOPE
# =========================================================

profile.update(

    dtype=rasterio.float32,

    count=1,

    nodata=-9999

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

print(
    f"Saved: {SLOPE_OUTPUT}"
)


# =========================================================
# GENERATE TWI
# =========================================================

print("\nGenerating TWI")

# PySheds does not handle NaN well

dem_pysheds = dem.copy()

dem_pysheds[
    np.isnan(dem_pysheds)
] = 0


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
# HYDROLOGIC CORRECTIONS
# ---------------------------------------------------------

flooded_dem = grid.fill_depressions(
    dem_raster
)

inflated_dem = grid.resolve_flats(
    flooded_dem
)

flowdir = grid.flowdir(
    inflated_dem
)

acc = grid.accumulation(
    flowdir
)

# ---------------------------------------------------------
# TWI
# ---------------------------------------------------------

slope_radians = np.radians(
    slope
)

slope_radians[
    slope_radians <= 0
] = 0.001

twi = np.log(

    (
        acc + 1
    )

    /

    np.tan(
        slope_radians
    )

)

# restore county mask

twi[mask] = -9999


# =========================================================
# SAVE TWI
# =========================================================

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

print(
    f"Saved: {TWI_OUTPUT}"
)


# =========================================================
# COMPLETE
# =========================================================

print("\n===================================")
print("TERRAIN FEATURES COMPLETE")
print("===================================")