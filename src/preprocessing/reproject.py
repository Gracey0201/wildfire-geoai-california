"""
reproject.py

Reproject raster and vector datasets
to a common CRS.

Target CRS:
EPSG:3310
"""

from pathlib import Path
import warnings

import geopandas as gpd
import rasterio
from rasterio.enums import Resampling
from rasterio.warp import (
    calculate_default_transform,
    reproject
)

warnings.filterwarnings("ignore")

# SETTINGS

TARGET_CRS = "EPSG:3310"

RAW_DATA_DIR = Path("data/raw")

OUTPUT_DIR = Path(
    "data/processed/reprojected"
)

OUTPUT_DIR.mkdir(
    parents=True,
    exist_ok=True
)

# VECTOR REPROJECTION

def reproject_vector(
    input_path,
    output_path
):

    print(f"\nReprojecting: {input_path.name}")

    gdf = gpd.read_file(
        input_path
    )

    gdf = gdf.to_crs(
        TARGET_CRS
    )

    gdf.to_file(
        output_path,
        driver="GeoJSON"
    )

    print(f"Saved: {output_path}")


# RASTER REPROJECTION

def reproject_raster(
    input_path,
    output_path
):

    print(f"\nReprojecting: {input_path.name}")

    with rasterio.open(input_path) as src:

        transform, width, height = (
            calculate_default_transform(
                src.crs,
                TARGET_CRS,
                src.width,
                src.height,
                *src.bounds,
                resolution=30
            )
        )

        kwargs = src.meta.copy()

        kwargs.update({

            "crs": TARGET_CRS,
            "transform": transform,
            "width": width,
            "height": height

        })

        with rasterio.open(
            output_path,
            "w",
            **kwargs
        ) as dst:

            for i in range(
                1,
                src.count + 1
            ):

                reproject(

                    source=rasterio.band(src, i),

                    destination=rasterio.band(dst, i),

                    src_transform=src.transform,
                    src_crs=src.crs,

                    dst_transform=transform,
                    dst_crs=TARGET_CRS,

                    resampling=Resampling.nearest

                )

    print(f"Saved: {output_path}")


# PROCESS VECTORS

reproject_vector(

    RAW_DATA_DIR /
    "roads" /
    "roads.geojson",

    OUTPUT_DIR /
    "roads_3310.geojson"

)

reproject_vector(

    RAW_DATA_DIR /
    "wildfire" /
    "wildfire_history.geojson",

    OUTPUT_DIR /
    "wildfire_3310.geojson"

)

# PROCESS RASTERS

reproject_raster(

    RAW_DATA_DIR /
    "dem" /
    "dem.tif",

    OUTPUT_DIR /
    "dem_3310.tif"

)

reproject_raster(

    RAW_DATA_DIR /
    "landcover" /
    "landcover.tif",

    OUTPUT_DIR /
    "landcover_3310.tif"

)

reproject_raster(

    RAW_DATA_DIR /
    "climate" /
    "precipitation.tif",

    OUTPUT_DIR /
    "precipitation_3310.tif"

)

# COMPLETE

print("\n===================================")
print("REPROJECTION COMPLETE")
print("===================================")