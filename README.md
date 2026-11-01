# Supporting Community Wildfire Preparedness in Butte County, California: An Integrated Geospatial Risk Assessment Framework
A reproducible GeoAI framework integrating Random Forest wildfire susceptibility modeling, population exposure, and socioeconomic vulnerability to assess wildfire risk in Butte County, California.

## Project Overview

Wildfires pose significant threats to communities through direct exposure to fire, smoke-related health impacts, infrastructure damage, displacement, and disruption of essential services. These impacts are not distributed equally, as communities differ in their exposure to wildfire hazards and their socioeconomic capacity to prepare for, respond to, and recover from wildfire events.

This project develops an integrated geospatial artificial intelligence (GeoAI) framework to assess wildfire risk in Butte County, California. The framework combines Random Forest machine learning for wildfire susceptibility modeling with population exposure and socioeconomic vulnerability assessments to identify areas where environmental hazards and community vulnerability intersect.

Using publicly available geospatial, environmental, demographic, and socioeconomic datasets, the project integrates multiple dimensions of wildfire risk into a spatial assessment framework. The resulting maps provide insights into the geographic distribution of wildfire susceptibility, population exposure, and composite wildfire risk.

The project aims to demonstrate how geospatial analysis and machine learning can support evidence-based wildfire preparedness, community resilience planning, and public health decision-making, particularly in communities facing elevated environmental and socioeconomic risks.

---

## Project Significance

Understanding where wildfire hazards intersect with population exposure and socioeconomic vulnerability is important for effective climate adaptation, community resilience, and public health preparedness.

By integrating machine learning, geospatial analytics, exposure assessment, and community vulnerability indicators, this project provides a reproducible framework for identifying areas of elevated wildfire risk.

The resulting workflow can support:

* Climate adaptation planning
* Community resilience initiatives
* Environmental justice assessments
* Hazard mitigation planning
* Public health preparedness
* Resource prioritization and decision support

---

## Project Objectives

The overall objective is to develop a reproducible geospatial risk assessment framework integrating wildfire susceptibility, population exposure, and socioeconomic vulnerability in Butte County, California.

The specific objectives are to:

1. **Develop a wildfire susceptibility model:** Apply Random Forest machine learning to environmental and anthropogenic predictors to generate a spatial representation of wildfire susceptibility.

2. **Assess population exposure:** Examine population density and Wildland–Urban Interface (WUI) distribution in relation to wildfire susceptibility to identify potentially exposed communities.

3. **Evaluate socioeconomic vulnerability:** Incorporate poverty, older adult population, income characteristics, and disability indicators to characterize spatial differences in community vulnerability.

4. **Integrate wildfire risk dimensions:** Combine wildfire susceptibility, population exposure, and socioeconomic vulnerability into a composite wildfire risk assessment framework.

5. **Generate decision-support maps:** Produce spatial outputs illustrating wildfire susceptibility, population exposure, and integrated wildfire risk across Butte County.

6. **Support public health and community preparedness:** Demonstrate how integrated geospatial analysis can inform targeted wildfire preparedness, climate resilience planning, and public health decision-making.
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

### Reproduce the Analysis

The complete workflow can be executed using the Python scripts described in the Workflow Execution section below.

Jupyter notebooks are provided for model evaluation, visualization, interpretation, and quality assurance of results.

---


## Study Area

Butte County is located in Northern California, USA, spanning portions of the northern Sacramento Valley and the Sierra Nevada foothills. The county has diverse environmental and geographical conditions, including varied terrain, vegetation, and land-use patterns.

Butte County was selected as the study area because of its history of destructive wildfire events, extensive Wildland–Urban Interface (WUI) development, diverse environmental conditions, and importance for climate resilience planning.

<img width="3300" height="2550" alt="Study area map showing Butte County, California, within the state of California" src="https://github.com/user-attachments/assets/7c8b2f8a-82c6-456e-afa0-e38f3fa51959" />


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
## Results

The GeoAI framework successfully identified spatial patterns of wildfire susceptibility, exposure, and integrated risk across Butte County, California.

### Wildfire Susceptibility Assessment

The Random Forest model successfully identified spatial patterns of wildfire susceptibility across Butte County, California. Areas classified as **high** and **very high susceptibility** were concentrated primarily in the eastern, southeastern, and central foothill and mountainous regions of the county. Elevated susceptibility was particularly evident around the communities of **Paradise**, **Magalia**, and portions of the Sierra Nevada foothills, whereas the western agricultural valley regions surrounding **Chico** and **Oroville** were characterized predominantly by low-susceptibility classes.

Model evaluation demonstrated excellent predictive performance, with a mean five-fold cross-validation ROC-AUC score of **0.988**, indicating a strong ability to distinguish wildfire-prone from non-prone locations. The low variability among folds suggests that the model generalized consistently across the study area.

Feature importance analysis revealed that **precipitation** was the most influential predictor, followed by **elevation (DEM)**, **land cover**, and **slope**. Variables representing proximity to settlements and roads exhibited moderate influence, while topographic wetness index (TWI) contributed comparatively less to model performance. These findings are consistent with previous studies demonstrating that climatic conditions, vegetation characteristics, and topographic factors strongly influence wildfire occurrence and spread across western North America (Jain et al., 2020). The importance of precipitation and elevation within the model further supports evidence that climate variability, fuel moisture conditions, and terrain-related processes play a critical role in shaping wildfire susceptibility patterns throughout California landscapes (Abatzoglou & Williams, 2016). Furthermore, recent climate assessments indicate that increasing temperatures, altered precipitation regimes, and prolonged drought conditions are expected to exacerbate wildfire hazards across many regions of the western United States (IPCC, 2022).

### Wildfire Exposure Assessment

The wildfire exposure assessment identified locations where populations and built environments are most likely to be affected by wildfire hazards. Exposure levels were generally highest within and around the urbanized and wildland–urban interface (WUI) environments surrounding **Chico**, **Paradise**, **Magalia**, and **Oroville**. Moderate to high exposure zones were concentrated near developed areas where residential communities, transportation infrastructure, and human activities intersect with wildfire-prone landscapes.

In contrast, large portions of the northern and eastern forested regions exhibited lower exposure despite elevated wildfire susceptibility because of lower population density and fewer built assets. This pattern highlights the distinction between wildfire hazard and exposure, as areas characterized by high wildfire potential do not necessarily correspond to locations where large populations or infrastructure are concentrated.

The observed spatial distribution aligns with previous research demonstrating that expansion of the wildland–urban interface has substantially increased the number of people, homes, and critical assets exposed to wildfire hazards across the United States (Radeloff et al., 2018). Studies conducted in California further indicate that residential development patterns within fire-prone landscapes are among the strongest predictors of wildfire exposure and structural losses (Syphard et al., 2019). The concentration of elevated exposure around Paradise, Magalia, Chico, and Oroville reflects the growing interaction between human settlements and wildfire-prone environments, a pattern increasingly observed throughout western North America (Kramer et al., 2019).

### Integrated Wildfire Risk Assessment

The integrated wildfire risk assessment combined wildfire susceptibility, exposure, and socioeconomic vulnerability indicators to identify locations where wildfire impacts may be most severe. High-risk and very-high-risk zones were concentrated across the central and eastern portions of Butte County, particularly surrounding **Paradise**, **Magalia**, and adjacent foothill communities. Additional pockets of elevated risk were identified near **Oroville** and along portions of the wildland–urban interface where wildfire hazards intersect with exposed populations and socially vulnerable communities.

The western agricultural valley regions exhibited generally lower risk levels despite containing populated areas because wildfire susceptibility remained comparatively low. Conversely, some mountainous areas displayed high wildfire susceptibility but lower overall risk because of reduced population exposure and limited concentrations of built infrastructure. These findings reinforce the principle that disaster risk is not determined solely by hazard occurrence but by the interaction of hazard, exposure, and vulnerability (IPCC, 2022).

The resulting risk map illustrates the importance of considering both physical wildfire processes and socioeconomic vulnerability when prioritizing mitigation and adaptation strategies. Communities located within the foothill and WUI environments of Butte County represent priority areas for wildfire preparedness, fuel reduction programs, evacuation planning, and resilience-building initiatives. Similar studies have shown that socially vulnerable populations often experience disproportionate impacts from wildfire events due to limited adaptive capacity, reduced access to resources, and greater challenges during evacuation and post-disaster recovery (Chas-Amil et al., 2022).

The concentration of high-risk zones around Paradise and Magalia is particularly noteworthy given the historical impacts of the 2018 Camp Fire, which demonstrated the severe consequences that can occur when wildfire hazards intersect with highly exposed and vulnerable communities. These findings are consistent with contemporary disaster-risk frameworks, which conceptualize risk as the interaction of hazard, exposure, and vulnerability rather than hazard alone (UNDRR, 2023).

Overall, the results demonstrate that wildfire risk within Butte County is spatially heterogeneous and driven by the interaction of environmental conditions, population exposure, and socioeconomic vulnerability. The developed geospatial framework provides a reproducible approach for identifying wildfire-prone areas and supporting evidence-based climate adaptation, environmental justice, land-use planning, and community resilience initiatives. Furthermore, the framework is transferable to other wildfire-prone regions and demonstrates how GIS, remote sensing, and machine learning can be integrated to support disaster risk reduction and climate adaptation planning.

---

## Census API Configuration

This project uses the U.S. Census Bureau API to obtain demographic and socioeconomic data used in the exposure and community vulnerability assessments.

### Obtain a Census API Key

Request a free Census API key:

* [Census API Key Signup](https://api.census.gov/data/key_signup.html)

### Configure the API Key

Update the following files:

```text
config/config.yaml
src/download/population.py
src/download/vulnerability.py
```

Replace:

```python
CENSUS_API_KEY = "YOUR_CENSUS_API_KEY"
```

with your personal Census API key.

### Download Census Data

Population data:

```bash
python src/download/population.py
```

Vulnerability data:

```bash
python src/download/vulnerability.py
```

### Documentation

* [Census Developers Documentation](https://www.census.gov/data/developers/data-sets.html)


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

## Reference

Abatzoglou, J. T., & Williams, A. P. (2016). Impact of anthropogenic climate change on wildfire across western US forests. Proceedings of the National Academy of Sciences, 113(42), 11770–11775.

Chas-Amil, M. L., Touza, J., García-Martínez, E., & Varela, E. (2022). Spatial patterns of social vulnerability in relation to wildfire risk. Landscape and Urban Planning, 228, 104566.

IPCC. (2022). Climate Change 2022: Impacts, Adaptation and Vulnerability. Working Group II Contribution to the Sixth Assessment Report of the Intergovernmental Panel on Climate Change.

Jain, P., Coogan, S. C. P., Subramanian, S. G., Crowley, M., Taylor, S., & Flannigan, M. D. (2020). A review of machine learning applications in wildfire science and management. Environmental Reviews, 28(4), 478–505.

Kramer, H. A., Mockrin, M. H., Alexandre, P. M., & Radeloff, V. C. (2019). High wildfire damage in interface communities in California. International Journal of Wildland Fire, 28(9), 641–650.

Radeloff, V. C., Helmers, D. P., Kramer, H. A., et al. (2018). Rapid growth of the US wildland–urban interface raises wildfire risk. Proceedings of the National Academy of Sciences, 115(13), 3314–3319.

Syphard, A. D., Keeley, J. E., & Massada, A. B. (2019). Housing arrangement and location determine the likelihood of housing loss due to wildfire. PLoS ONE, 7(3), e33954.

UNDRR. (2023). Global Assessment Report on Disaster Risk Reduction. United Nations Office for Disaster Risk Reduction.


## License

This project is licensed under the MIT License.
