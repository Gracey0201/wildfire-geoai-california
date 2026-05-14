# GeoAI-Driven Wildfire Climate Risk Intelligence and Community Vulnerability Modeling for California

## Overview

This project develops a reproducible GeoAI framework for statewide wildfire susceptibility modeling and climate risk intelligence across California using machine learning, automated geospatial preprocessing, socioeconomic vulnerability analysis, and interactive web mapping.

The workflow integrates:
- terrain variables
- climate predictors
- vegetation indicators
- anthropogenic ignition factors
- socioeconomic vulnerability indicators
- population exposure layers
- wildfire occurrence data

to model wildfire susceptibility and integrated climate risk using Random Forest and geospatial artificial intelligence (GeoAI) methods.

The project is designed to support:
- climate resilience planning
- environmental risk assessment
- geospatial decision intelligence
- scalable geospatial automation
- reproducible environmental analytics

The repository emphasizes:
- reproducibility
- automation
- cloud-native geospatial workflows
- scalable machine learning
- open science practices

---

## Objectives

The main objectives of this project are to:

- Develop a reproducible GeoAI wildfire susceptibility modeling pipeline
- Automate large-scale geospatial data acquisition and preprocessing
- Build a machine learning-based wildfire susceptibility model for California
- Generate statewide wildfire hazard and climate risk surfaces
- Integrate socioeconomic vulnerability and exposure indicators into wildfire climate risk analysis
- Explore relationships between environmental and anthropogenic wildfire drivers
- Produce static and interactive geospatial intelligence products
- Develop an interactive wildfire risk web mapping dashboard using MapLibre GL JS
- Demonstrate scalable cloud-compatible geospatial AI workflows
- Publish a reproducible open-source geospatial analytics framework

---

## Conceptual Framework

This project follows an integrated climate risk framework:

```math
Risk = Hazard × Vulnerability × Exposure
```

### Hazard
Represents the physical likelihood of wildfire occurrence based on environmental and anthropogenic conditions.

### Vulnerability
Represents the socioeconomic sensitivity and adaptive capacity of communities exposed to wildfire hazards.

### Exposure
Represents populations and built environments located within wildfire-prone areas.

The integration of these components produces a statewide wildfire climate risk intelligence surface for California.

---

## Study Area

The study area is the state of California, USA.

California was selected due to:
- increasing wildfire frequency and severity
- climate-driven environmental stressors
- diverse terrain and vegetation conditions
- significant wildland–urban interface exposure
- strong availability of open geospatial datasets

---

## Predictor Variables

### Hazard Variables

#### Terrain
- Elevation
- Slope
- Topographic Wetness Index (TWI)

#### Climate
- Temperature
- Wind
- Drought proxy

#### Vegetation
- NDVI
- Land Use / Land Cover (LULC)

#### Human Ignition Factors
- Distance to roads
- Distance to settlements

---

### Vulnerability Variables

#### Socioeconomic Vulnerability
- Poverty rate
- Median household income
- Elderly population percentage
- Disability prevalence percentage
- Housing vulnerability indicators

---

### Exposure Variables

#### Population & Built Environment Exposure
- Population density
- Settlements / Wildland–Urban Interface (WUI)

---

## Methodology

The project workflow is divided into three major analytical components:
1. Wildfire Hazard Modeling
2. Socioeconomic Vulnerability Modeling
3. Exposure Assessment

These components are integrated to generate a final wildfire climate risk intelligence surface.

---

## 1. Automated Geospatial Data Acquisition

Geospatial datasets are automatically acquired using:
- STAC APIs
- Microsoft Planetary Computer
- Open geospatial repositories
- Census and socioeconomic APIs
- OpenStreetMap services

The workflow automates:
- dataset querying
- downloading
- clipping
- reprojection
- storage organization

Datasets include:
- DEMs
- climate rasters
- vegetation products
- wildfire occurrence data
- transportation networks
- socioeconomic indicators
- population datasets

---

## 2. Raster Preprocessing and Spatial Harmonization

All raster datasets are standardized through automated preprocessing workflows.

Processing steps include:
- reprojection to common CRS
- spatial clipping to California boundary
- raster resampling
- alignment to common grid
- nodata handling
- raster masking
- spatial normalization

The project uses:
- Rasterio
- Rioxarray
- Xarray
- Dask
- WhiteboxTools

to support scalable raster processing.

---

## 3. Terrain and Feature Derivation

Terrain variables are derived from digital elevation models (DEMs).

Derived layers include:
- slope
- topographic wetness index (TWI)

Distance-based anthropogenic predictors are also generated:
- distance to roads
- distance to settlements

Vegetation and climate indicators are processed from remotely sensed and gridded datasets.

---

## 4. Wildfire Hazard Modeling

Wildfire susceptibility modeling is performed using Random Forest machine learning.

The hazard model integrates:
- terrain conditions
- climate variables
- vegetation indicators
- anthropogenic ignition drivers

The workflow includes:
- feature extraction
- training dataset preparation
- predictor stacking
- model fitting
- prediction generation
- feature importance analysis

The final output is a statewide wildfire susceptibility surface representing relative wildfire hazard probability.

---

## 5. Socioeconomic Vulnerability Modeling

Socioeconomic indicators are processed to generate a wildfire vulnerability index.

Indicators are normalized and integrated to characterize:
- social sensitivity
- adaptive capacity
- socioeconomic disadvantage

The vulnerability model identifies communities that may experience greater difficulty responding to or recovering from wildfire impacts.

---

## 6. Exposure Assessment

Exposure analysis identifies populations and built environments located within wildfire-prone areas.

Exposure layers include:
- population density
- settlements / WUI

These layers characterize the spatial distribution of populations and infrastructure exposed to wildfire hazards.

---

## 7. Integrated Climate Risk Modeling

Hazard, vulnerability, and exposure components are integrated to generate a composite wildfire climate risk surface.

```math
Risk = Hazard × Vulnerability × Exposure
```

The integrated framework supports:
- climate resilience analysis
- wildfire risk prioritization
- community vulnerability assessment
- geospatial decision support

---

## 8. Visualization and Geospatial Intelligence Products

The project produces:
- wildfire susceptibility maps
- climate risk surfaces
- feature importance plots
- exploratory spatial analyses
- interactive dashboards
- web GIS visualizations

Visualization outputs include:
- static publication-quality maps
- interactive MapLibre GL JS web maps
- geospatial intelligence dashboards

---

## Technology Stack

### Programming & Workflow
- Python
- Linux (WSL Ubuntu)
- Git & GitHub
- Conda environments

### Geospatial Libraries
- GeoPandas
- Rasterio
- Rioxarray
- Xarray
- WhiteboxTools
- OSMnx

### Machine Learning
- Scikit-learn
- Random Forest

### Parallel & Cloud Processing
- Dask
- STAC APIs
- Microsoft Planetary Computer

### Visualization & Web Mapping
- Matplotlib
- Plotly
- Leafmap
- MapLibre GL JS

---

## Reproducibility

This repository is structured as a reproducible geospatial machine learning pipeline.

Key reproducibility features include:
- environment management with Conda
- version control with Git/GitHub
- automated preprocessing workflows
- configuration-driven analysis
- modular Python scripts
- cloud-native geospatial data access
- scalable geospatial computation

---

## Planned Outputs

### Analytical Outputs
- Wildfire susceptibility rasters
- Climate risk surfaces
- Vulnerability indices
- Exposure layers
- Predictor variable layers
- Model evaluation metrics
- Feature importance analysis

### Visualization Outputs
- Static wildfire susceptibility maps
- Interactive web maps
- Dashboard visualizations
- Publication-quality figures

---

## Repository Structure

```text
data/           -> raw, interim, processed, and training datasets
src/            -> pipeline scripts
notebooks/      -> exploratory notebooks
outputs/        -> figures, models, tables, and web layers
config/         -> project configuration files
webapp/         -> MapLibre frontend application
```

---

## Future Work

Planned future improvements include:
- temporal wildfire forecasting
- explainable AI integration (SHAP analysis)
- cloud-optimized raster workflows
- Docker containerization
- Snakemake workflow orchestration
- deployment-ready geospatial intelligence dashboards
- scalable cloud geospatial infrastructure

---

## License

This project is released under the repository license.