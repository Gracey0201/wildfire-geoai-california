"""
susceptibility.py

Generate wildfire susceptibility maps
using the trained Random Forest model.
"""

from pathlib import Path
import warnings
import joblib

import numpy as np
import pandas as pd
import rasterio
import mapclassify
import rioxarray as rxr
import matplotlib.pyplot as plt

warnings.filterwarnings("ignore")

# PATHS

PROJECT_ROOT = Path.cwd()

ALIGNED_DIR = (
    PROJECT_ROOT /
    "data" /
    "processed" /
    "aligned"
)

FEATURE_DIR = (
    PROJECT_ROOT /
    "data" /
    "features"
)

MODEL_DIR = (
    PROJECT_ROOT /
    "outputs" /
    "models"
)

OUTPUT_DIR = (
    PROJECT_ROOT /
    "outputs" /
    "maps"
)

OUTPUT_DIR.mkdir(
    parents=True,
    exist_ok=True
)

# FILES

MODEL_PATH = (
    MODEL_DIR /
    "random_forest.pkl"
)

REFERENCE_RASTER = (
    ALIGNED_DIR /
    "dem_aligned.tif"
)

# LOAD MODEL

print("\nLoading model")

model = joblib.load(
    MODEL_PATH
)

print("Model loaded")


# LOAD RASTERS

print("\nLoading predictor rasters")

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

precipitation = rxr.open_rasterio(
    ALIGNED_DIR /
    "precipitation_aligned.tif"
).squeeze()

landcover = rxr.open_rasterio(
    ALIGNED_DIR /
    "landcover_aligned.tif"
).squeeze()

distance_to_roads = rxr.open_rasterio(
    FEATURE_DIR /
    "distance_to_roads.tif"
).squeeze()

distance_to_settlements = rxr.open_rasterio(
    FEATURE_DIR /
    "distance_to_settlements.tif"
).squeeze()


# COUNTY MASK

county_mask = (
    dem.values == -9999
)

# BUILD FEATURE STACK

print("\nBuilding predictor stack")

feature_df = pd.DataFrame({

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
        distance_to_settlements.values.flatten()

})

# CLEAN DATA

feature_df = feature_df.replace(
    -9999,
    np.nan
)

feature_df = feature_df.replace(
    [np.inf, -np.inf],
    np.nan
)

feature_df = feature_df.fillna(
    feature_df.median()
)


# GENERATE SUSCEPTIBILITY

print("\nGenerating susceptibility")

probability = model.predict_proba(
    feature_df
)[:, 1]

susceptibility = probability.reshape(
    dem.shape
)

susceptibility[
    county_mask
] = -9999


# SAVE CONTINUOUS RASTER

with rasterio.open(
    REFERENCE_RASTER
) as src:

    profile = src.profile.copy()

profile.update(

    dtype=rasterio.float32,

    count=1,

    nodata=-9999

)

SUSCEPTIBILITY_PATH = (
    OUTPUT_DIR /
    "wildfire_susceptibility.tif"
)

with rasterio.open(

    SUSCEPTIBILITY_PATH,

    "w",

    **profile

) as dst:

    dst.write(

        susceptibility.astype(
            rasterio.float32
        ),

        1

    )

print(
    f"Saved: {SUSCEPTIBILITY_PATH}"
)


# NATURAL BREAKS CLASSIFICATION

print("\nCalculating Natural Breaks classes")

valid = susceptibility[
    susceptibility != -9999
]

classifier = mapclassify.NaturalBreaks(
    valid,
    k=5
)

classes = np.full(
    susceptibility.shape,
    0,
    dtype=np.uint8
)

classes[
    susceptibility != -9999
] = classifier.yb + 1

print("\nNatural Breaks")

for i, value in enumerate(
    classifier.bins,
    start=1
):
    print(
        f"Class {i}: <= {value:.4f}"
    )

# SAVE CLASSIFIED RASTER

CLASS_PATH = (
    OUTPUT_DIR /
    "wildfire_susceptibility_classes.tif"
)

class_profile = profile.copy()

class_profile.update(
    dtype=rasterio.uint8,
    nodata=0
)

with rasterio.open(
    CLASS_PATH,
    "w",
    **class_profile
) as dst:

    dst.write(
        classes.astype(
            rasterio.uint8
        ),
        1
    )

print(
    f"Saved: {CLASS_PATH}"
)

print(
    "\nSusceptibility Classes:"
)

print(
    "1 = Very Low"
)

print(
    "2 = Low"
)

print(
    "3 = Moderate"
)

print(
    "4 = High"
)

print(
    "5 = Very High"
)


# PNG MAP

print("\nCreating map")

display_raster = np.where(

    susceptibility == -9999,

    np.nan,

    susceptibility

)

fig, ax = plt.subplots(
    figsize=(10, 8)
)

im = ax.imshow(
    display_raster
)

plt.colorbar(

    im,

    ax=ax,

    label="Wildfire Susceptibility"

)

ax.set_title(
    "Wildfire Susceptibility"
)

plt.tight_layout()

PNG_PATH = (
    OUTPUT_DIR /
    "wildfire_susceptibility.png"
)

plt.savefig(

    PNG_PATH,

    dpi=300,

    bbox_inches="tight"

)

plt.close()

print(
    f"Saved: {PNG_PATH}"
)


# COMPLETE

print("\n===================================")
print("SUSCEPTIBILITY MAPPING COMPLETE")
print("===================================")

print(
    f"\nOutputs:\n{OUTPUT_DIR}"
)