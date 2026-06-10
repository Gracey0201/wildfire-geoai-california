"""
risk.py

Create a wildfire risk map
for Butte County, California.

Risk is calculated as:

Risk =
Hazard
×
Exposure
×
Vulnerability

Input:
- wildfire_susceptibility.tif
- wildfire_exposure.tif
- vulnerability_index.tif

Output:
- wildfire_risk.tif
- wildfire_risk_classes.tif
"""

from pathlib import Path
import warnings

import numpy as np
import rasterio
import mapclassify

warnings.filterwarnings("ignore")


# PATHS

HAZARD_PATH = Path(
    "outputs/maps/wildfire_susceptibility.tif"
)

EXPOSURE_PATH = Path(
    "outputs/maps/wildfire_exposure.tif"
)

VULNERABILITY_PATH = Path(
    "data/features/vulnerability_index.tif"
)

OUTPUT_DIR = Path(
    "outputs/maps"
)

OUTPUT_DIR.mkdir(
    parents=True,
    exist_ok=True
)

RISK_PATH = (
    OUTPUT_DIR /
    "wildfire_risk.tif"
)


# LOAD HAZARD

print(
    "\nLoading hazard raster"
)

with rasterio.open(
    HAZARD_PATH
) as src:

    hazard = src.read(1)

    profile = src.profile.copy()

    hazard_nodata = src.nodata


# LOAD EXPOSURE

print(
    "\nLoading exposure raster"
)

with rasterio.open(
    EXPOSURE_PATH
) as src:

    exposure = src.read(1)

    exposure_nodata = src.nodata


# LOAD VULNERABILITY

print(
    "\nLoading vulnerability raster"
)

with rasterio.open(
    VULNERABILITY_PATH
) as src:

    vulnerability = src.read(1)

    vulnerability_nodata = src.nodata


# VALID MASK

valid_hazard = (

    np.ones_like(
        hazard,
        dtype=bool
    )

    if hazard_nodata is None

    else

    hazard != hazard_nodata

)

valid_exposure = (

    np.ones_like(
        exposure,
        dtype=bool
    )

    if exposure_nodata is None

    else

    exposure != exposure_nodata

)

valid_vulnerability = (

    np.ones_like(
        vulnerability,
        dtype=bool
    )

    if vulnerability_nodata is None

    else

    vulnerability != vulnerability_nodata

)

valid_mask = (

    valid_hazard

    &

    valid_exposure

    &

    valid_vulnerability

)

# CALCULATE RISK

print(
    "\nCalculating wildfire risk"
)

risk = np.full(

    hazard.shape,

    -9999,

    dtype=np.float32

)

risk[
    valid_mask
] = (

    hazard[
        valid_mask
    ]

    *

    exposure[
        valid_mask
    ]

    *

    vulnerability[
        valid_mask
    ]

)


# SAVE OUTPUT

profile.update(

    dtype=rasterio.float32,

    count=1,

    nodata=-9999

)

with rasterio.open(

    RISK_PATH,

    "w",

    **profile

) as dst:

    dst.write(

        risk.astype(
            np.float32
        ),

        1

    )

print(
    f"Saved: {RISK_PATH}"
)

# RISK CLASSES

RISK_CLASSES_PATH = (
    OUTPUT_DIR /
    "wildfire_risk_classes.tif"
)

print(
    "\nClassifying wildfire risk"
)

valid_values = risk[
    risk != -9999
]

classifier = mapclassify.Quantiles(
    valid_values,
    k=5
)

classes = np.full(
    risk.shape,
    -9999,
    dtype=np.int16
)

classes[
    risk != -9999
] = classifier.yb + 1

class_profile = profile.copy()

class_profile.update(
    dtype=rasterio.int16,
    nodata=-9999
)

with rasterio.open(
    RISK_CLASSES_PATH,
    "w",
    **class_profile
) as dst:

    dst.write(
        classes.astype(
            np.int16
        ),
        1
    )

print(
    f"Saved: {RISK_CLASSES_PATH}"
)

print(
    "\nRisk Classes:"
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

# SUMMARY

valid = risk[
    risk != -9999
]

print("\n===================================")
print("WILDFIRE RISK COMPLETE")
print("===================================")

print(
    f"Minimum Risk: "
    f"{valid.min():.4f}"
)

print(
    f"Maximum Risk: "
    f"{valid.max():.4f}"
)

print(
    f"Mean Risk: "
    f"{valid.mean():.4f}"
)

print(
    f"Valid Pixels: "
    f"{len(valid):,}"
)

print("\nOutput:")

print(
    RISK_PATH
)

print(
    RISK_CLASSES_PATH
)