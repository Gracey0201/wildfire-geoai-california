# Spatial Modeling of Wildfire Risk and Socioeconmomic Vulnerability in Butte County, California
This project develops a reproducible GeoAI framework for wildfire susceptibility, exposure, vulnerability, and risk assessment in Butte County, California.

## Overview

Wildfires represent one of the most significant climate-related hazards affecting communities across California and the western United States. Increasing wildfire frequency, prolonged drought conditions, expanding Wildland–Urban Interface (WUI) development, and growing population exposure have intensified the need for data-driven approaches to wildfire risk assessment and climate adaptation planning.

This project develops a reproducible GeoAI framework for wildfire susceptibility, exposure, vulnerability, and risk assessment in Butte County, California. The workflow integrates machine learning, remote sensing, geospatial analysis, demographic indicators, and automated spatial data processing to identify locations where wildfire impacts may pose the greatest threat to communities.

The project combines environmental hazard indicators, population exposure metrics, and community vulnerability characteristics to support climate resilience planning, environmental justice assessments, public health preparedness, and geospatial decision-making.

---

## Project Significance

Wildfires increasingly threaten communities, infrastructure, ecosystems, and public health across California. Smoke exposure, displacement, infrastructure disruption, and economic losses disproportionately affect vulnerable populations.

By integrating machine learning, geospatial analytics, exposure assessment, and community vulnerability indicators, this project provides a reproducible framework for identifying communities at elevated wildfire risk.

The resulting workflow supports:

* Climate adaptation planning
* Community resilience initiatives
* Environmental justice assessments
* Hazard mitigation planning
* Public health preparedness
* Resource prioritization and decision support

---

## Project Objectives

The objectives of this project are to:

* Develop a reproducible GeoAI workflow for wildfire susceptibility modeling.
* Identify environmental and anthropogenic drivers associated with wildfire occurrence.
* Quantify community exposure using population density and Wildland–Urban Interface (WUI) indicators.
* Assess community vulnerability using socioeconomic indicators.
* Integrate susceptibility, exposure, and vulnerability layers into a comprehensive wildfire risk framework.
* Produce decision-support maps for climate adaptation and resilience planning.
* Demonstrate scalable and reproducible geospatial machine learning workflows using open-source tools.

---

## Installation and Setup

### System Requirements

The project was developed and tested using:

* Python 3.11+
* Conda (recommended)
* Jupyter Notebook / JupyterLab
* ArcGIS Pro (optional, for cartographic map production)

### Clone the Repository

```bash
git clone https://github.com/Gracey0201/wildfire-geoai-california.git

cd wildfire-geoai-california
```

### Create the Conda Environment

```bash
conda env create -f environment.yaml

conda activate wildfire-geoai
```

### Verify Installation

Confirm that required packages are available:

```bash
python -c "import geopandas, rasterio, sklearn; print('Installation successful')"
```

### Configure Census API Access

This project uses the U.S. Census Bureau API to obtain demographic and socioeconomic variables used in both the exposure and vulnerability assessments.

Obtain a free Census API key:

https://api.census.gov/data/key_signup.html

Then update:

```text
src/download/population.py

src/download/vulnerability.py
```

with:

```python
CENSUS_API_KEY = "YOUR_CENSUS_API_KEY"
```

### Reproduce the Analysis

The complete workflow can be executed using the Python scripts described in the Workflow Execution section below.

Jupyter notebooks are provided for model evaluation, visualization, interpretation, and quality assurance of results.


## Study Area

The study area is Butte County, California.

Butte County was selected because of its history of destructive wildfire events, extensive Wildland–Urban Interface development, diverse environmental conditions, and importance for climate resilience planning.

---

## Conceptual Framework

This project follows an integrated wildfire risk framework:

```text
Risk = Susceptibility × Exposure × Vulnerability
```

### Susceptibility

Represents the relative likelihood of wildfire occurrence based on environmental and anthropogenic conditions.

### Exposure

Represents populations, infrastructure, and built environments that may be affected by wildfire events.

### Vulnerability

Represents the socioeconomic characteristics that influence a community's ability to prepare for, respond to, and recover from wildfire impacts.

The integration of these components produces a spatially explicit wildfire risk surface for Butte County.

---

## Methodology

### 1. Automated Geospatial Data Acquisition

Geospatial datasets are obtained from publicly available sources including:

* U.S. Census Bureau
* Microsoft Planetary Computer
* OpenStreetMap
* National Land Cover Database (NLCD)
* Digital Elevation Models (DEM)
* Historical wildfire perimeter datasets

The workflow automates:

* Dataset querying
* Downloading
* Clipping
* Reprojection
* Data organization

---

### 2. Spatial Data Processing

All raster and vector datasets are standardized through:

* Reprojection
* Spatial clipping
* Raster alignment
* Resampling
* NoData handling
* Raster masking
* Normalization

---

### 3. Wildfire Susceptibility Modeling

A Random Forest machine learning model was developed using environmental and anthropogenic predictors.

#### Environmental Variables

* Elevation
* Slope
* Topographic Wetness Index (TWI)
* Precipitation
* Land Cover

#### Human Influence Variables

* Distance to Roads
* Distance to Settlements

The model generates a continuous wildfire susceptibility surface representing relative wildfire hazard potential.

---

### 4. Exposure Assessment

Exposure was modeled using:

* Population Density
* Wildland–Urban Interface (WUI)
* Developed Land Indicators

The exposure surface identifies populations and infrastructure potentially affected by wildfire events.

---

### 5. Community Vulnerability Assessment

A vulnerability index was developed using demographic and socioeconomic indicators representing community sensitivity and adaptive capacity.

Indicators include:

* Poverty
* Older Adult Population
* Income Characteristics
* Disability Indicators

The resulting vulnerability surface identifies communities that may experience disproportionate impacts during wildfire events.

---

### 6. Integrated Wildfire Risk Assessment

Wildfire susceptibility, exposure, and vulnerability layers were integrated to generate a composite wildfire risk surface.

The final risk map identifies locations where wildfire hazards intersect with exposed populations and vulnerable communities.

---

## Model Performance

The Random Forest wildfire susceptibility model achieved:

| Metric    | Value |
| --------- | ----- |
| Accuracy  | 96.1% |
| Precision | 95.8% |
| Recall    | 96.4% |
| F1 Score  | 96.1% |
| ROC-AUC   | 0.994 |

Feature importance analysis identified precipitation, elevation, land cover, slope, and proximity to settlements as key wildfire predictors.

---
## Key Findings

The GeoAI framework successfully identified spatial patterns of wildfire susceptibility, exposure, and integrated risk across Butte County, California.

### Wildfire Susceptibility

Wildfire susceptibility was concentrated primarily within the mountainous, forested, and upland regions of central, eastern, northeastern, and southeastern Butte County. Lower susceptibility values were generally observed within the flatter western valley areas. These patterns suggest that topography, vegetation characteristics, precipitation, and proximity to human activities play important roles in wildfire occurrence.

### Wildfire Exposure

Wildfire exposure was concentrated within developed areas, transportation corridors, and Wildland–Urban Interface (WUI) zones. Statistical analysis indicated a mean exposure index of 0.119 and a median value of 0.106, suggesting that most locations experience relatively low exposure while a smaller number of areas contain concentrated populations, infrastructure, and assets that may be affected by wildfire events.

### Integrated Wildfire Risk

The integrated wildfire risk assessment revealed that risk is not uniformly distributed across Butte County. Elevated risk was concentrated primarily within central and eastern portions of the county where wildfire susceptibility, exposure, and community vulnerability overlap. In contrast, much of the western valley region exhibited relatively low wildfire risk due to lower modeled wildfire susceptibility despite the presence of developed land.

### Implications for Climate Resilience

The results demonstrate the value of integrating machine learning, geospatial analytics, exposure assessment, and socioeconomic vulnerability indicators into a unified wildfire risk framework. The resulting products can support climate adaptation planning, hazard mitigation, environmental justice assessments, public health preparedness, and resource prioritization efforts.

---

## Census API Configuration

This project uses demographic and socioeconomic data obtained through the U.S. Census Bureau API.

The Census API is required for generating both:

* Population Exposure Layers
* Community Vulnerability Layers

### Obtain a Census API Key

Request a free Census API key:

https://api.census.gov/data/key_signup.html

### Configure the API Key

Open:

```text
src/download/population.py
src/download/vulnerability.py
```

Replace:

```python
CENSUS_API_KEY = "YOUR_CENSUS_API_KEY"
```

with your personal Census API key.

### Download Population Data

```bash
python src/download/population.py
```

### Download Vulnerability Data

```bash
python src/download/vulnerability.py
```

### Census API Documentation

https://www.census.gov/data/developers/data-sets.html

---



## Workflow Execution

The project was designed as a reproducible command-line geospatial workflow. Core data acquisition, preprocessing, feature engineering, machine learning, exposure assessment, vulnerability assessment, and risk modeling steps are executed through Python scripts rather than Jupyter notebooks.

This approach improves reproducibility, automation, scalability, and transparency while reducing manual processing steps.

### 1. Data Acquisition

Download all required datasets:

```bash
python src/download/download_boundary.py
python src/download/download_dem.py
python src/download/landcover.py
python src/download/population.py
python src/download/precipitation.py
python src/download/roads.py
python src/download/vulnerability.py
python src/download/wildfire.py
```

### 2. Data Preprocessing

Standardize coordinate systems, spatial extent, raster alignment, and resolution:

```bash
python src/preprocessing/align.py
python src/preprocessing/clip.py
python src/preprocessing/reproject.py
python src/preprocessing/standardize.py
```

### 3. Feature Engineering

Generate terrain and distance-based predictors used by the machine learning model:

```bash
python src/features/distance.py
python src/features/terrain.py
```

### 4. Wildfire Susceptibility Modeling

Prepare training data, train the Random Forest model, evaluate model performance, and generate the wildfire susceptibility surface:

```bash
python src/modeling/training_data.py
python src/modeling/labels.py
python src/modeling/random_forest.py
python src/modeling/evaluation.py
python src/modeling/feature_importance.py
python src/modeling/susceptibility.py
```

### 5. Exposure Assessment

Generate population density, Wildland–Urban Interface (WUI), and exposure layers:

```bash
python src/exposure/population_raster.py
python src/exposure/wui.py
python src/exposure/exposure.py
```

### 6. Vulnerability Assessment

Generate the community vulnerability index:

```bash
python src/exposure/vulnerability_index.py
```

### 7. Wildfire Risk Assessment

Integrate susceptibility, exposure, and vulnerability layers into a composite wildfire risk surface:

```bash
python src/risk/risk.py
```

### 8. Results Exploration

Three Jupyter notebooks are provided for visualization, interpretation, and quality assurance:

```text
01_model_evaluation.ipynb
02_susceptibility_mapping.ipynb
03_risk_assessment.ipynb
```

The notebooks are intended for analysis and interpretation of model outputs rather than execution of the primary processing workflow.

---


## Technology Stack

### Programming & Workflow

* Python
* Jupyter Notebook
* Linux (WSL Ubuntu)
* Git & GitHub
* Conda

### Geospatial Analysis

* GeoPandas
* Rasterio
* Rioxarray
* WhiteboxTools
* OSMnx

### Machine Learning

* Scikit-learn
* Random Forest

### Visualization

* Matplotlib
* ArcGIS Pro

---

## Repository Structure

## Repository Structure

```text
.
├── README.md
├── LICENSE
├── environment.yaml
│
├── config/
│   └── config.yaml
│
├── data/
│   ├── raw/
│   ├── processed/
│   ├── features/
│   └── training/
│
├── notebooks/
│   ├── 01_model_evaluation.ipynb
│   ├── 02_susceptibility_mapping.ipynb
│   └── 03_risk_assessment.ipynb
│
├── outputs/
│   ├── feature_importance/
│   ├── figures/
│   ├── maps/
│   ├── model_evaluation/
│   └── models/
│
├── src/
│   ├── download/
│   ├── preprocessing/
│   ├── features/
│   ├── modeling/
│   ├── exposure/
│   └── risk/
```

---

## Reproducibility

This repository is designed as a reproducible geospatial machine learning workflow. All major analytical steps—from data acquisition through risk assessment—are automated through modular Python scripts and documented notebooks.

Key reproducibility features include:

* Version control with Git/GitHub
* Environment management with Conda
* Automated preprocessing workflows
* Modular Python scripts
* Open geospatial data sources
* Reproducible machine learning workflows

---

## Future Work

Potential future enhancements include:

* Explainable AI (SHAP) analysis
* Climate projection integration
* Environmental justice hotspot analysis
* Interactive web GIS deployment
* Multi-county scaling across California
* Temporal wildfire forecasting

---

## License

This project is licensed under the MIT License.
