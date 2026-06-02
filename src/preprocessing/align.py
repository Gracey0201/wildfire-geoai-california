"""
align.py

Align rasters to a common grid.
"""

from pathlib import Path
import warnings

import rioxarray as rxr

warnings.filterwarnings("ignore")


# PATHS

INPUT_DIR = Path(
    "data/processed/clipped"
)

OUTPUT_DIR = Path(
    "data/processed/aligned"
)

OUTPUT_DIR.mkdir(
    parents=True,
    exist_ok=True
)

# REFERENCE RASTER

REFERENCE_RASTER = (
    INPUT_DIR /
    "dem_clipped.tif"
)

# ALIGN FUNCTION

def align_raster(
    input_path,
    output_path
):

    print(f"\nAligning: {input_path.name}")

    reference = rxr.open_rasterio(
        REFERENCE_RASTER
    )

    raster = rxr.open_rasterio(
        input_path
    )

    aligned = raster.rio.reproject_match(
        reference
    )

    aligned.rio.to_raster(
        output_path
    )

    print(f"Saved: {output_path}")


# ALIGN RASTERS

align_raster(

    INPUT_DIR /
    "landcover_clipped.tif",

    OUTPUT_DIR /
    "landcover_aligned.tif"

)

align_raster(

    INPUT_DIR /
    "precipitation_clipped.tif",

    OUTPUT_DIR /
    "precipitation_aligned.tif"

)

# COPY DEM

dem = rxr.open_rasterio(
    REFERENCE_RASTER
)

dem.rio.to_raster(

    OUTPUT_DIR /
    "dem_aligned.tif"

)

# COMPLETE

print("\n===================================")
print("ALIGNMENT COMPLETE")
print("===================================")