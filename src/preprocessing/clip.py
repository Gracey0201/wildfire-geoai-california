"""
clip.py

Clip raster datasets
to the study boundary.
"""

from pathlib import Path
import warnings

import geopandas as gpd
import rasterio
from rasterio.mask import mask

warnings.filterwarnings("ignore")


# =========================================================
# PATHS
# =========================================================

INPUT_DIR = Path(
    "data/processed/reprojected"
)

OUTPUT_DIR = Path(
    "data/processed/clipped"
)

OUTPUT_DIR.mkdir(
    parents=True,
    exist_ok=True
)

BOUNDARY_PATH = (
    "data/raw/boundaries/boundary.geojson"
)


# =========================================================
# LOAD BOUNDARY
# =========================================================

boundary = gpd.read_file(
    BOUNDARY_PATH
)

boundary = boundary.to_crs(
    "EPSG:3310"
)


# =========================================================
# CLIP FUNCTION
# =========================================================

def clip_raster(
    input_path,
    output_path
):

    print(f"\nClipping: {input_path.name}")

    with rasterio.open(input_path) as src:

        clipped, transform = mask(

            src,

            boundary.geometry,

            crop=True

        )

        metadata = src.meta.copy()

        metadata.update({

            "height": clipped.shape[1],
            "width": clipped.shape[2],
            "transform": transform

        })

        with rasterio.open(
            output_path,
            "w",
            **metadata
        ) as dst:

            dst.write(clipped)

    print(f"Saved: {output_path}")


# =========================================================
# CLIP RASTERS
# =========================================================

clip_raster(

    INPUT_DIR /
    "dem_3310.tif",

    OUTPUT_DIR /
    "dem_clipped.tif"

)

clip_raster(

    INPUT_DIR /
    "landcover_3310.tif",

    OUTPUT_DIR /
    "landcover_clipped.tif"

)

clip_raster(

    INPUT_DIR /
    "precipitation_3310.tif",

    OUTPUT_DIR /
    "precipitation_clipped.tif"

)


# =========================================================
# COMPLETE
# =========================================================

print("\n===================================")
print("CLIPPING COMPLETE")
print("===================================")