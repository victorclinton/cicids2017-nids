import joblib
import pandas as pd
import streamlit as st

from src.config import MODEL_DIR


@st.cache_resource
def load_artifacts():

    model = joblib.load(
        MODEL_DIR / "tuned_random_forest.pkl"
    )

    scaler = joblib.load(
        MODEL_DIR / "robust_scaler.pkl"
    )

    label_encoder = joblib.load(
        MODEL_DIR / "label_encoder.pkl"
    )

    feature_cols = (
    pd.read_csv(
        MODEL_DIR / "feature_names.csv"
    )
    .iloc[:, 0]
    .tolist())

    return (
        model,
        scaler,
        label_encoder,
        feature_cols,
    )