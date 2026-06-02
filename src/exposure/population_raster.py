"""
population_raster.py

Convert census tract population density
to a raster aligned with the wildfire
susceptibility model grid.

Input:
- population.geojson
- dem_aligned.tif

Output:
- population_density.tif
"""

from pathlib import Path
import warnings

import geopandas as gpd
import numpy as np
import rasterio
from rasterio.features import rasterize

warnings.filterwarnings("ignore")


# PATHS

POPULATION_PATH = Path(
    "data/raw/population/population.geojson"
)

REFERENCE_RASTER = Path(
    "data/processed/aligned/dem_aligned.tif"
)

OUTPUT_DIR = Path(
    "data/features"
)

OUTPUT_DIR.mkdir(
    parents=True,
    exist_ok=True
)

OUTPUT_PATH = (
    OUTPUT_DIR /
    "population_density.tif"
)

# LOAD REFERENCE GRID
print("\nLoading reference raster")

with rasterio.open(
    REFERENCE_RASTER
) as src:

    profile = src.profile.copy()

    shape = src.shape

    transform = src.transform

    dem = src.read(1)

    nodata = src.nodata

# COUNTY MASK

county_mask = (
    dem == nodata
)

# LOAD POPULATION DATA

print("\nLoading population polygons")

population = gpd.read_file(
    POPULATION_PATH
)

print(
    f"Features: {len(population)}"
)

required_field = (
    "population_density"
)

if required_field not in population.columns:

    raise ValueError(
        f"Missing field: {required_field}"
    )


# RASTERIZE POPULATION DENSITY
print(
    "\nRasterizing population density"
)

population_raster = rasterize(

    [
        (
            geom,
            value
        )

        for geom, value in zip(

            population.geometry,

            population[
                "population_density"
            ]

        )
    ],

    out_shape=shape,

    transform=transform,

    fill=-9999,

    dtype="float32"

)


# APPLY COUNTY MASK

population_raster[
    county_mask
] = -9999


# UPDATE PROFILE

profile.update(

    dtype=rasterio.float32,

    count=1,

    nodata=-9999

)


# SAVE OUTPUT

with rasterio.open(

    OUTPUT_PATH,

    "w",

    **profile

) as dst:

    dst.write(

        population_raster.astype(
            rasterio.float32
        ),

        1

    )

print(
    f"Saved: {OUTPUT_PATH}"
)

# SUMMARY
valid = population_raster[
    population_raster != -9999
]

print("\n===================================")
print("POPULATION RASTER COMPLETE")
print("===================================")

print(
    f"Minimum density: "
    f"{valid.min():.2f}"
)

print(
    f"Maximum density: "
    f"{valid.max():.2f}"
)

print(
    f"Mean density: "
    f"{valid.mean():.2f}"
)

print(
    f"\nOutput:"
)

print(
    OUTPUT_PATH
)