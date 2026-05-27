"""
standardize.py

Verify standardized rasters.
"""

from pathlib import Path
import warnings

import rioxarray as rxr

warnings.filterwarnings("ignore")


# =========================================================
# PATHS
# =========================================================

DATA_DIR = Path(
    "data/processed/aligned"
)


# =========================================================
# VERIFY FUNCTION
# =========================================================

def verify_raster(
    raster_path
):

    raster = rxr.open_rasterio(
        raster_path
    )

    print("\n===================================")
    print(raster_path.name)
    print("===================================")

    print(f"\nCRS: {raster.rio.crs}")

    print(
        f"Resolution: "
        f"{raster.rio.resolution()}"
    )

    print(
        f"Shape: "
        f"{raster.shape}"
    )

    print(
        f"Bounds: "
        f"{raster.rio.bounds()}"
    )


# =========================================================
# VERIFY ALL
# =========================================================

verify_raster(

    DATA_DIR /
    "dem_aligned.tif"

)

verify_raster(

    DATA_DIR /
    "landcover_aligned.tif"

)

verify_raster(

    DATA_DIR /
    "precipitation_aligned.tif"

)


# =========================================================
# COMPLETE
# =========================================================

print("\n===================================")
print("STANDARDIZATION VERIFIED")
print("===================================")