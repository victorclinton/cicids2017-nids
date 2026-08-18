"""
Inference module for the Network Intrusion Detection System.

This module orchestrates the complete prediction pipeline:
1. Load raw data
2. Preprocess features
3. Run model inference
4. Return prediction results
"""

from pathlib import Path
import pandas as pd

from src.preprocessing import preprocess_input
from src.predictor import predict


def predict_dataframe(
    df: pd.DataFrame,
    model,
    scaler,
    label_encoder,
    feature_cols,
    log_features=None,
    verbose: bool = False,
) -> pd.DataFrame:
    """
    Predict network traffic from a pandas DataFrame.

    Parameters
    ----------
    df : pd.DataFrame
        Raw network traffic data.

    model : sklearn estimator
        Trained Random Forest model.

    scaler : fitted scaler
        RobustScaler used during training.

    label_encoder : LabelEncoder
        Encoder used during training.

    feature_cols : list[str]
        Feature names expected by the model.

    log_features : list[str] | None
        Features requiring log transformation.

    verbose : bool
        Display preprocessing information.

    Returns
    -------
    pd.DataFrame
        Prediction results.
    """

    X_scaled = preprocess_input(
        df_input=df,
        feature_cols=feature_cols,
        scaler=scaler,
        log_features=log_features,
        verbose=verbose,
    )

    results = predict(
        processed_df=X_scaled,
        model=model,
        label_encoder=label_encoder,
    )

    return results


def predict_from_csv(
    csv_path: str | Path,
    model,
    scaler,
    label_encoder,
    feature_cols,
    log_features=None,
    verbose: bool = False,
) -> pd.DataFrame:
    """
    Predict network traffic from a CSV file.
    """

    df = pd.read_csv(csv_path)

    return predict_dataframe(
        df=df,
        model=model,
        scaler=scaler,
        label_encoder=label_encoder,
        feature_cols=feature_cols,
        log_features=log_features,
        verbose=verbose,
    )