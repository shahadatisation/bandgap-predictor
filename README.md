# Materials Band Gap Predictor using Composition-based ML

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

## The purpose behind this project
Band Gap refers to the difference of energy between the valence band and conduction band of a material's structure. It is a key property to determine whether a material is metal, semiconductor or insulator. This project explores whether a machine learning model can accurately predict band gap of a material using it's chemical data, using dataset from Materials Project. The purpose is to observe how the model learns data and how it decides importance of chemical properties of each material in this regard.

## Data
- **Source:** [Materials Project](https://materialsproject.org/) via the `mp-api` Python client.
- **Scale:** All stable inorganic materials. Total 33,973 entries.
- **Retrieved Columns:** Formula, Band Gap(eV), Formation Energy(eV/atom).
- **Data Classification:** All the materials were classified into 3 types - *Metal* (band_gap == 0), *Semiconductor* (band_gap <= 4), and *Insulator* (band_gap > 4) in later stages. 

## Underlying Process
1. **Featurization:** Each chemical formula was transformed into 132 numerical features using the MAGPIE (Materials Agnostic Platform for Informatics and Exploration) preset from `matminer`. These features encode elemental properties like electronegativity, atomic number, melting temperature, etc.

2. **Models:**
   - **Random Forest Regressor** (scikit-learn, 100 trees)
   - **Feedforward Neural Network** (PyTorch, 2 hidden layers, ReLU activations)

3. **Evaluation:** Data split 70/15/15 (train/validation/test). Features standardized using `StandardScaler`. Primary metric: Mean Absolute Error (MAE).

## Results 
| Model          | Train MAE (eV) | Validation MAE (eV) | Test MAE (eV) |
|----------------|----------------|---------------------|---------------|
| Random Forest  | 0.119          | 0.304               | 0.320         |
| Neural Network | 0.277          | 0.380               | 0.378         |

- **Parity plots** show both models perform well for band gaps >1 eV but significantly struggle with metals. The neural network occasionally predicts unphysical negative band gaps.
- **Class‑conditional errors** shows a better understanding :
  - Metals (MAE 0.131–0.157 eV) — small absolute error because the true value is exactly 0.
  - Non‑metals (MAE 0.504–0.593 eV) — error is much larger and dominates the overall metric.
- **Feature importance analysis** (Random Forest) showed that a single feature — `MagpieData mode MeltingT` (the most common melting temperature of the elements) — accounted for **42%** of the model’s decision power. The second‑most important feature, `MagpieData mean NdValence` (d‑electron count), is physically relevant but far less weighted.

## Key Finding : The model took a shortcut
The MeltingT feature acted as a separator between metal and non-metal. The model did not tried much to learn the underlying physics that controls the actual band gap values, rather it learned to identify metals co-relating MeltingT and their band gap ~0 eV. This resulted the MAE be much less for metals, but caused disproportionate error in non-metals. 

## Limitations
A. **Almost 50% of the dataset being metals** resulted the model being biased towards that easy shortcut. 
B. The features were *composition-based*, other important informations such as bond-lengths, molecular stuctures etc. aren't considered.

## What Future Work may include :
1. As the model was being biased towards the overwhelming amount of metals, training a separate classifier to filter the metal first and then regression model on non-metals may result the model to establish an importance backed by real physics.
2. Exploring whether only training on non-metals may produce a better prediction with more meaningful feature importance.

## Repository Structure
- `bandgap_predictor.ipynb` — Full workflow from data loading to results.
- `materials_data_full.csv` — Raw queried data (33,973 rows × 4 columns).
- `materials_data_eda.csv` — Data after exploratory analysis with additional columns.
- `materials_featurized.csv` — Final feature matrix and target for modeling.
- `requirements.txt` — Python dependencies.

## How to Run
1. Clone the repository:  
   `git clone https://github.com/shahadatisation/bandgap-predictor.git`
2. Create a virtual environment and install dependencies:  
   `python -m venv .venv`  
   `source .venv/bin/activate` (or `.venv\Scripts\activate` on Windows)  
   `pip install -r requirements.txt`
3. Run the Jupyter notebook `bandgap_predictor.ipynb` cell by cell.  
   *Note: To re‑query the Materials Project, you need an API key set as an environment variable `MP_API_KEY`.*

## Acknowledgments
- Data provided by the Materials Project, supported by the U.S. Department of Energy.
- This project was built as a self‑learning exercise in computational materials science and ML.
