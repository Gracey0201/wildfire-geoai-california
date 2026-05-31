"""
exposure.py

Create a wildfire exposure index
for Butte County, California.

Exposure is calculated as:

Exposure =
(
WUI
+
Normalized Population Density
) / 2

Input:
- wui.tif
- population_density.tif

Output:
- wildfire_exposure.tif
"""

from pathlib import Path
import warnings

import numpy as np
import rasterio

warnings.filterwarnings("ignore")


# =========================================================
# PATHS
# =========================================================

WUI_PATH = Path(
    "data/features/wui.tif"
)

POPULATION_PATH = Path(
    "data/features/population_density.tif"
)

OUTPUT_DIR = Path(
    "outputs/maps"
)

OUTPUT_DIR.mkdir(
    parents=True,
    exist_ok=True
)

EXPOSURE_PATH = (
    OUTPUT_DIR /
    "wildfire_exposure.tif"
)


# =========================================================
# LOAD WUI
# =========================================================

print(
    "\nLoading WUI raster"
)

with rasterio.open(
    WUI_PATH
) as src:

    wui = src.read(1)

    profile = src.profile.copy()

    wui_nodata = src.nodata


# =========================================================
# LOAD POPULATION DENSITY
# =========================================================

print(
    "\nLoading population density raster"
)

with rasterio.open(
    POPULATION_PATH
) as src:

    population = src.read(1)

    population_nodata = src.nodata


# =========================================================
# VALID MASK
# =========================================================

if wui_nodata is None:

    valid_wui = np.ones_like(
        wui,
        dtype=bool
    )

else:

    valid_wui = (
        wui != wui_nodata
    )

if population_nodata is None:

    valid_population = np.ones_like(
        population,
        dtype=bool
    )

else:

    valid_population = (
        population != population_nodata
    )

valid_mask = (

    valid_wui

    &

    valid_population

)


# =========================================================
# WUI
# =========================================================

print(
    "\nPreparing WUI layer"
)

# WUI is already binary:
# 0 = Non-WUI
# 1 = WUI

wui_norm = wui.astype(
    np.float32
)


# =========================================================
# NORMALIZE POPULATION DENSITY
# =========================================================

print(
    "\nNormalizing population density"
)

population_norm = np.zeros_like(

    population,

    dtype=np.float32

)

# Log-transform population density
# to reduce extreme skewness

population_log = np.log1p(
    population.astype(
        np.float32
    )
)

valid_population_values = population_log[
    valid_mask
]

population_min = valid_population_values.min()

population_max = valid_population_values.max()

if population_max > population_min:

    population_norm[
        valid_mask
    ] = (

        (
            population_log[
                valid_mask
            ]
            -
            population_min
        )

        /

        (
            population_max
            -
            population_min
        )

    )

# =========================================================
# EXPOSURE INDEX
# =========================================================

print(
    "\nCalculating exposure index"
)

exposure = np.full(

    wui.shape,

    -9999,

    dtype=np.float32

)

exposure[
    valid_mask
] = (

    wui_norm[
        valid_mask
    ]

    +

    population_norm[
        valid_mask
    ]

) / 2


# =========================================================
# SAVE OUTPUT
# =========================================================

profile.update(

    dtype=rasterio.float32,

    count=1,

    nodata=-9999

)

with rasterio.open(

    EXPOSURE_PATH,

    "w",

    **profile

) as dst:

    dst.write(

        exposure.astype(
            np.float32
        ),

        1

    )

print(
    f"Saved: {EXPOSURE_PATH}"
)


# =========================================================
# SUMMARY
# =========================================================

valid = exposure[
    exposure != -9999
]

print("\n===================================")
print("EXPOSURE ANALYSIS COMPLETE")
print("===================================")

print(
    f"Minimum Exposure: "
    f"{valid.min():.4f}"
)

print(
    f"Maximum Exposure: "
    f"{valid.max():.4f}"
)

print(
    f"Mean Exposure: "
    f"{valid.mean():.4f}"
)

print(
    f"Valid Pixels: "
    f"{len(valid):,}"
)

print("\nOutput:")

print(
    EXPOSURE_PATH
)