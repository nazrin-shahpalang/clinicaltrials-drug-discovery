# 🔬 AI Analysis of ClinicalTrials.gov Data for Drug Discovery Trends

[![Python](https://img.shields.io/badge/Python-3.11-blue.svg)](https://python.org)
[![R](https://img.shields.io/badge/R-Statistical%20Analysis-276DC3.svg)](https://r-project.org)
[![Plotly Dash](https://img.shields.io/badge/Dashboard-Plotly%20Dash-00CC96.svg)](https://dash.plotly.com)

> Exploratory analysis of 2,000 clinical trials (2013–2024) to uncover AI drug discovery trends, disease-area patterns, and sponsor activity using Python, NLP, and R statistical modeling.

---

## 📌 Project Overview

This project bridges two key areas of modern drug development:

1. **Clinical trial landscape analysis** — which diseases attract the most trials, how enrollment scales by phase, and which sponsors lead the field
2. **AI drug discovery tracking** — quantifying the growth of AI-designed drug candidates entering clinical stages (2013–2024)

---

## 🧬 Key Findings

| Insight | Result |
|---|---|
| Most-trialled disease | Oncology (28% of all trials) |
| AI-designed trial growth | ~1.5% increase per year |
| Phase with highest enrollment | Phase 3 (median ~416 participants) |
| Most active sponsor type | Biotech Startups (14%) |
| NLP classifier accuracy | 100% (TF-IDF + Random Forest) |

---

## 🗂️ Repository Structure
clinicaltrials-drug-discovery/

├── data/

│   ├── raw/clinical_trials_data.csv

│   └── processed/

├── notebooks/

│   ├── 01_data_collection.ipynb

│   ├── 02_eda_analysis.ipynb

│   └── 03_nlp_analysis.ipynb

├── R/

│   └── statistical_analysis.R

├── dashboard/

│   └── app.py

└── README.md
---

## 🛠️ Tech Stack

| Tool | Purpose |
|---|---|
| Python 3.11 | Core analysis |
| pandas, numpy | Data wrangling |
| scikit-learn | TF-IDF, Random Forest |
| Plotly Dash | Interactive dashboard |
| R + ggplot2 | Statistical analysis |
| Render.com | Cloud deployment |

---

## 🚀 Running Locally

```bash
conda create -n ct-env python=3.11
conda activate ct-env
pip install -r dashboard/requirements.txt
python dashboard/app.py
```

---

## 👩‍🔬 Author

**Nazrin Shahpalangova**  
MSc Biological Resources — Rhine-Waal University of Applied Sciences, Germany  
BSc Biology/Genetics — Baku State University (2024)
