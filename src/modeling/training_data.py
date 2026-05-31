"""
training_data.py

Create a balanced training dataset
for wildfire susceptibility modeling.
"""

from pathlib import Path

import numpy as np
import pandas as pd
import rioxarray as rxr


# =========================================================
# SETTINGS
# =========================================================

RANDOM_STATE = 42

SAMPLES_PER_CLASS = 100000


# =========================================================
# PATHS
# =========================================================

PROJECT_ROOT = Path.cwd()

FEATURE_DIR = (
    PROJECT_ROOT /
    "data" /
    "features"
)

ALIGNED_DIR = (
    PROJECT_ROOT /
    "data" /
    "processed" /
    "aligned"
)

TRAINING_DIR = (
    PROJECT_ROOT /
    "data" /
    "training"
)

OUTPUT_PATH = (
    TRAINING_DIR /
    "training_data.csv"
)


# =========================================================
# LOAD RASTERS
# =========================================================

print("\nLoading rasters")

dem = rxr.open_rasterio(
    ALIGNED_DIR /
    "dem_aligned.tif"
).squeeze()

slope = rxr.open_rasterio(
    FEATURE_DIR /
    "slope.tif"
).squeeze()

twi = rxr.open_rasterio(
    FEATURE_DIR /
    "twi.tif"
).squeeze()

distance_to_roads = rxr.open_rasterio(
    FEATURE_DIR /
    "distance_to_roads.tif"
).squeeze()

distance_to_settlements = rxr.open_rasterio(
    FEATURE_DIR /
    "distance_to_settlements.tif"
).squeeze()

landcover = rxr.open_rasterio(
    ALIGNED_DIR /
    "landcover_aligned.tif"
).squeeze()

precipitation = rxr.open_rasterio(
    ALIGNED_DIR /
    "precipitation_aligned.tif"
).squeeze()

labels = rxr.open_rasterio(
    TRAINING_DIR /
    "labels.tif"
).squeeze()


# =========================================================
# APPLY COUNTY MASK TO LABELS
# =========================================================

labels = labels.where(
    dem != -9999
)


# =========================================================
# VERIFY SHAPES
# =========================================================

shape = labels.shape

for raster in [

    dem,
    slope,
    twi,
    distance_to_roads,
    distance_to_settlements,
    landcover,
    precipitation

]:

    if raster.shape != shape:

        raise ValueError(
            f"Shape mismatch: {raster.shape}"
        )

print(
    f"Raster shape: {shape}"
)


# =========================================================
# BUILD DATAFRAME
# =========================================================

print("\nBuilding dataframe")

df = pd.DataFrame({

    "dem":
        dem.values.flatten(),

    "slope":
        slope.values.flatten(),

    "twi":
        twi.values.flatten(),

    "precipitation":
        precipitation.values.flatten(),

    "landcover":
        landcover.values.flatten(),

    "distance_to_roads":
        distance_to_roads.values.flatten(),

    "distance_to_settlements":
        distance_to_settlements.values.flatten(),

    "label":
        labels.values.flatten()

})


# =========================================================
# CLEAN DATA
# =========================================================

print("\nCleaning data")

total_pixels = len(df)

# Replace raster nodata values

df = df.replace(
    -9999,
    np.nan
)

# Replace infinities

df = df.replace(
    [np.inf, -np.inf],
    np.nan
)

# Remove nodata pixels

df = df.dropna()

removed_pixels = (
    total_pixels -
    len(df)
)

print(
    f"Valid pixels: {len(df):,}"
)

print(
    f"Removed nodata pixels: "
    f"{removed_pixels:,}"
)


# =========================================================
# SPLIT CLASSES
# =========================================================

burned = df[
    df["label"] == 1
]

unburned = df[
    df["label"] == 0
]

print(
    f"Burned pixels: {len(burned):,}"
)

print(
    f"Unburned pixels: {len(unburned):,}"
)


# =========================================================
# BALANCED RANDOM SAMPLING
# =========================================================

burned_sample = burned.sample(

    n=SAMPLES_PER_CLASS,

    random_state=RANDOM_STATE

)

unburned_sample = unburned.sample(

    n=SAMPLES_PER_CLASS,

    random_state=RANDOM_STATE

)

training_data = pd.concat(

    [
        burned_sample,
        unburned_sample
    ]

)

training_data = training_data.sample(

    frac=1,

    random_state=RANDOM_STATE

).reset_index(
    drop=True
)


# =========================================================
# SAVE CSV
# =========================================================

training_data.to_csv(

    OUTPUT_PATH,

    index=False

)


# =========================================================
# SUMMARY
# =========================================================

print("\n===================================")
print("TRAINING DATA CREATED")
print("===================================")

print(
    f"Burned samples: "
    f"{len(burned_sample):,}"
)

print(
    f"Unburned samples: "
    f"{len(unburned_sample):,}"
)

print(
    f"Total samples: "
    f"{len(training_data):,}"
)

print(
    "\nPredictors:"
)

print(
    "dem, slope, twi, precipitation, "
    "landcover, distance_to_roads, "
    "distance_to_settlements"
)

print(
    f"\nSaved: {OUTPUT_PATH}"
)