# 🔐 Network Intrusion Detection System using CIC-IDS2017

![Python](https://img.shields.io/badge/Python-3.9%2B-blue?logo=python)
![scikit-learn](https://img.shields.io/badge/scikit--learn-1.3%2B-orange?logo=scikit-learn)
![XGBoost](https://img.shields.io/badge/XGBoost-2.0%2B-red)
![LightGBM](https://img.shields.io/badge/LightGBM-4.0%2B-green)
![CatBoost](https://img.shields.io/badge/CatBoost-1.2%2B-yellow)
![License](https://img.shields.io/badge/License-MIT-lightgrey)

A complete end-to-end **Machine Learning pipeline** for detecting network intrusions and classifying attack types using the **CIC-IDS2017** dataset. The pipeline covers data ingestion, exploratory data analysis, feature engineering, model training, hyperparameter tuning, and a production-ready inference system.

---

## 📋 Table of Contents

- [Project Overview](#-project-overview)
- [Dataset](#-dataset)
- [Pipeline Architecture](#-pipeline-architecture)
- [Results](#-results)
- [Project Structure](#-project-structure)
- [Installation](#-installation)
- [How to Run](#-how-to-run)
- [Key Findings](#-key-findings)
- [Technologies Used](#-technologies-used)
- [Author](#-author)

---

## 🎯 Project Overview

This project builds a **multi-class network intrusion detection system (NIDS)** capable of classifying network traffic into **15 categories** — one benign class and 14 distinct attack types — in real time.

**Key achievements:**
- Processed **2,830,744** real network flow records from the CIC-IDS2017 dataset
- Engineered **69 features** from 78 raw flow statistics including 10 new derived features
- Compared **5 ML classifiers** (Decision Tree, Random Forest, XGBoost, LightGBM, CatBoost)
- Achieved **99.825% accuracy** and **87.27% Macro F1** with the tuned Random Forest
- Built a production-ready inference pipeline that processes **8,600+ flows/second**

---

## 📊 Dataset

**Source:** [Canadian Institute for Cybersecurity — CIC-IDS2017](https://www.unb.ca/cic/datasets/ids-2017.html)

| Property | Value |
|---|---|
| Total Records | 2,830,744 |
| Raw Features | 78 |
| Attack Classes | 14 |
| Capture Period | July 3–7, 2017 |
| Tool | CICFlowMeter |

### Attack Types Covered

| Attack | Count | Category |
|---|---|---|
| BENIGN | ~2,073,000 | Normal Traffic |
| DoS Hulk | 231,073 | Denial of Service |
| PortScan | 158,930 | Reconnaissance |
| DDoS | 128,027 | Distributed DoS |
| DoS GoldenEye | 10,293 | Denial of Service |
| FTP-Patator | 7,938 | Brute Force |
| SSH-Patator | 5,897 | Brute Force |
| DoS Slowloris | 5,796 | Denial of Service |
| DoS Slowhttptest | 5,499 | Denial of Service |
| Bot | 1,966 | Botnet |
| Web Attack — Brute Force | 1,507 | Web Attack |
| Web Attack — XSS | 652 | Web Attack |
| Infiltration | 36 | Infiltration |
| Web Attack — SQL Injection | 21 | Web Attack |
| Heartbleed | 11 | Vulnerability Exploit |

### Known Data Quality Issues Handled
- Duplicate column `Fwd Header Length.1` — dropped
- Infinity values in `Flow Bytes/s` and `Flow Packets/s` — replaced with NaN
- Leading/trailing whitespace in column names — stripped
- Duplicate rows — removed

---

## 🏗️ Pipeline Architecture

```
Raw CSV Files (8 files, ~1GB)
        │
        ▼
┌─────────────────────┐
│  Data Loading &     │
│  Merging            │  → 2,830,744 rows × 79 columns
└─────────────────────┘
        │
        ▼
┌─────────────────────┐
│  Exploratory Data   │
│  Analysis           │  → Univariate + Bivariate Analysis
└─────────────────────┘
        │
        ▼
┌─────────────────────┐
│  Feature            │
│  Engineering        │  → 69 final features (10 new derived)
└─────────────────────┘
        │
        ▼
┌─────────────────────┐
│  Class Imbalance    │
│  Handling           │  → RandomUnderSampler + RandomOverSampler
└─────────────────────┘
        │
        ▼
┌─────────────────────┐
│  Model Training     │
│  (5 classifiers)    │  → RF, XGBoost, LightGBM, CatBoost, DT
└─────────────────────┘
        │
        ▼
┌─────────────────────┐
│  Hyperparameter     │
│  Tuning             │  → RandomizedSearchCV + StratifiedKFold
└─────────────────────┘
        │
        ▼
┌─────────────────────┐
│  Inference          │
│  Pipeline           │  → 8,600+ flows/second
└─────────────────────┘
```

---

## 📈 Results

### Model Comparison (Before Tuning)

| Model | Accuracy | Weighted F1 | Macro F1 | Train Time |
|---|---|---|---|---|
| Decision Tree | — | — | — | — |
| Random Forest | — | — | — | — |
| XGBoost | — | — | — | — |
| LightGBM | — | — | — | — |
| CatBoost | — | — | — | — |

> *Fill in your actual values from the Model Building notebook*

### Hyperparameter Tuning — Top 2 Models

| Model | Accuracy | Weighted F1 | Macro F1 | Weighted Recall |
|---|---|---|---|---|
| **Tuned Random Forest** ⭐ | **99.825%** | **99.829%** | **87.270%** | **99.825%** |
| Tuned XGBoost | 99.740% | 99.757% | 82.130% | 99.740% |

### Best Model — Tuned Random Forest

```
Best Hyperparameters:
  n_estimators     : (from your tuning results)
  max_depth        : (from your tuning results)
  min_samples_split: (from your tuning results)
  min_samples_leaf : (from your tuning results)
  max_features     : (from your tuning results)
  class_weight     : balanced
```

### Inference on Full Dataset (2,830,744 flows)

| Metric | Value |
|---|---|
| Total Flows | 2,830,744 |
| Benign Detected | 2,702,789 (95.5%) |
| Attacks Detected | 127,955 (4.5%) |
| Throughput | 8,600+ flows/second |

---

## 📁 Project Structure

```
cicids2017-nids/
│
├── notebooks/
│   ├── 01_EDA.ipynb
│   ├── 02_Univariate_Analysis.ipynb
│   ├── 03_Bivariate_Analysis.ipynb
│   ├── 04_Feature_Engineering.ipynb
│   ├── 05_Model_Building.ipynb
│   ├── 06_Hyperparameter_Tuning.ipynb
│   └── 07_Inference_Pipeline.ipynb
│
├── preprocessed/
│   ├── X_train.npy
│   ├── X_test.npy
│   ├── X_train_scaled.npy
│   ├── X_test_scaled.npy
│   ├── y_train_multi.npy
│   ├── y_test_multi.npy
│   ├── feature_names.csv
│   ├── label_encoder.pkl
│   └── robust_scaler.pkl
│
├── tuned_models/
│   ├── tuned_random_forest.pkl
│   ├── tuned_xgboost.pkl
│   ├── rf_cv_results.csv
│   └── xgb_cv_results.csv
│
├── inference_results/
│   ├── predictions.csv
│   ├── attacks_only.csv
│   ├── classification_report.csv
│   ├── summary_metrics.csv
│   ├── attack_breakdown.csv
│   └── cicids2017_inference_pipeline.pkl
│
├── deployment/
│   └── cicids2017_inference_pipeline.pkl
│
├── requirements.txt
└── README.md
```

---

## ⚙️ Installation

### 1. Clone the repository
```bash
git clone https://github.com/victorclinton/cicids2017-nids.git
cd cicids2017-nids
```

### 2. Create a virtual environment
```bash
python -m venv venv
venv\Scripts\activate        # Windows
source venv/bin/activate     # Mac/Linux
```

### 3. Install dependencies
```bash
pip install -r requirements.txt
```

### `requirements.txt`
```
pandas>=2.0.0
numpy>=1.24.0
scikit-learn>=1.3.0
imbalanced-learn>=0.11.0
xgboost>=2.0.0
lightgbm>=4.0.0
catboost>=1.2.0
matplotlib>=3.7.0
seaborn>=0.12.0
scipy>=1.11.0
joblib>=1.3.0
jupyter>=1.0.0
```

---

## 🚀 How to Run

### Option 1 — Run the full pipeline from scratch

Open and run the notebooks in order:

```
01_EDA.ipynb                  ← Start here
02_Univariate_Analysis.ipynb
03_Bivariate_Analysis.ipynb
04_Feature_Engineering.ipynb
05_Model_Building.ipynb
06_Hyperparameter_Tuning.ipynb
07_Inference_Pipeline.ipynb   ← Final predictions
```

### Option 2 — Run inference only (using saved model)

```python
import joblib
import pandas as pd
import numpy as np

# Load pipeline bundle
bundle = joblib.load('deployment/cicids2017_inference_pipeline.pkl')

# Load your raw network traffic CSV
df_new = pd.read_csv('your_network_traffic.csv',
                     encoding='utf-8', low_memory=False)

# Predict
from sklearn.preprocessing import RobustScaler

scaler       = bundle['scaler']
model        = bundle['model']
le           = bundle['label_encoder']
feature_cols = bundle['feature_cols']
log_features = bundle['log_features']

# Run prediction (see Inference_Pipeline.ipynb for full function)
# results = predict_traffic(df_new, model, scaler, le, feature_cols, log_features)
# print(results[['Predicted_Label', 'Confidence (%)', 'Risk_Level']])
```

### Dataset Download

Download the CIC-IDS2017 dataset from:
[https://www.unb.ca/cic/datasets/ids-2017.html](https://www.unb.ca/cic/datasets/ids-2017.html)

Place all 8 CSV files in a folder and update `DATA_PATH` in the notebooks.

---

## 🔍 Key Findings

**Feature Engineering**
- `Init_Win_bytes_backward` was the single strongest predictor — attack flows typically show `-1` (no TCP handshake) while benign flows show `65535` (modern OS default)
- `Fwd_Bwd_Pkt_Ratio` (new derived feature) effectively identifies scan and flood attacks — attack flows approach ratio of `1.0` (no server response)
- Flow rate features (`Flow Bytes/s`, `Flow Packets/s`) showed extreme right skew and required `log1p` transformation

**Class Imbalance**
- BENIGN traffic dominated at 83% of all records
- RandomUnderSampler (BENIGN: 1.6M → 150K) + RandomOverSampler (rare classes to 5K) reduced training data from 2M to ~510K rows — making training feasible without MemoryError

**Model Performance**
- Random Forest outperformed XGBoost on Macro F1 by **5.14%** — better at detecting rare attack classes (Heartbleed, Infiltration, SQL Injection)
- Tree-based models (RF, XGBoost, LightGBM, CatBoost) all significantly outperformed the Decision Tree baseline
- `class_weight='balanced'` combined with resampling gave the best minority class recall

**Inference**
- The trained pipeline processes **8,600+ flows/second** — suitable for near real-time network monitoring
- All 14 attack types are detectable with the correct log feature transforms applied at inference time

---

## 🛠️ Technologies Used

| Category | Tools |
|---|---|
| Language | Python 3.9+ |
| Data Processing | pandas, NumPy |
| Machine Learning | scikit-learn, XGBoost, LightGBM, CatBoost |
| Imbalanced Learning | imbalanced-learn (RandomOverSampler, RandomUnderSampler) |
| Visualisation | matplotlib, seaborn |
| Model Persistence | joblib |
| Environment | Jupyter Notebook, Anaconda |

---

## 👤 Author

**Victor Chinonyerem Ananaba**

[![LinkedIn](https://img.shields.io/badge/LinkedIn-Connect-blue?logo=linkedin)](https://linkedin.com/in/victor-ananaba-b206471a8)
[![GitHub](https://img.shields.io/badge/GitHub-victorclinton-black?logo=github)](https://github.com/victorclinton)

*Machine Operator transitioning into Data Analytics & Machine Learning*
*Background in Electrical Engineering | Python · scikit-learn · Power BI · Excel*

---

## 📄 License

This project is licensed under the MIT License.

---

> **Dataset Citation:**  
> Iman Sharafaldin, Arash Habibi Lashkari, and Ali A. Ghorbani,  
> "Toward Generating a New Intrusion Detection Dataset and Intrusion Traffic Characterization",  
> 4th International Conference on Information Systems Security and Privacy (ICISSP), 2018
