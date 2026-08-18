import streamlit as st

from src.theme import apply_cybersecurity_theme


st.set_page_config(
    page_title="Home",
    page_icon="🏠",
    layout="wide"
)

apply_cybersecurity_theme()


st.markdown("""
# Machine Learning-Based Network Intrusion Detection System

### Project Objectives

- Detect malicious network traffic
- Identify attack categories
- Improve E-Voting security
- Provide real-time predictions

---

### Dataset

CICIDS2017

---

### Machine Learning Model

✅ Tuned Random Forest

---

### Features

- Batch Prediction
- Threat Dashboard
- Dataset Explorer
- Model Performance
- About
- Attack Analysis
- Alert
- Real Time Monitor
""")

