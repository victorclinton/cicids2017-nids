import pandas as pd


def assign_risk(predicted_label, confidence):
    """
    Assign a qualitative risk level based on
    prediction class and model confidence.
    """

    # Benign traffic is considered low risk
    if predicted_label == "BENIGN":
        return "Low"

    # Attack with low confidence
    if confidence < 70:
        return "Medium"

    # Attack with moderate/high confidence
    return "High"


def predict(
    processed_df,
    model,
    label_encoder,
):
    """
    Run inference on preprocessed network traffic.

    Parameters
    ----------
    processed_df : np.ndarray
        Scaled feature matrix returned by preprocess_input().

    model : sklearn classifier
        Trained Random Forest model.

    label_encoder : LabelEncoder
        Encoder used during training.

    Returns
    -------
    pd.DataFrame
        Prediction results.
    """

    # ============================================================
    # 1. PREDICT ENCODED LABELS
    # ============================================================

    pred_ids = model.predict(
        processed_df
    )

    # ============================================================
    # 2. PREDICT PROBABILITIES
    # ============================================================

    probabilities = model.predict_proba(
        processed_df
    )

    # ============================================================
    # 3. CALCULATE CONFIDENCE
    # ============================================================

    confidence = (
        probabilities.max(axis=1) * 100
    )

    # ============================================================
    # 4. DECODE LABELS
    # ============================================================

    predicted_labels = (
        label_encoder.inverse_transform(
            pred_ids
        )
    )

    # ============================================================
    # 5. IDENTIFY ATTACKS
    # ============================================================

    is_attack = (
        predicted_labels != "BENIGN"
    )

    # ============================================================
    # 6. ASSIGN RISK
    # ============================================================

    risk_level = [
        assign_risk(
            label,
            score
        )
        for label, score
        in zip(
            predicted_labels,
            confidence
        )
    ]

    # ============================================================
    # 7. CREATE RESULTS DATAFRAME
    # ============================================================

    results = pd.DataFrame({

        "Predicted_Label":
            predicted_labels,

        "Confidence (%)":
            confidence.round(2),

        "Is_Attack":
            is_attack,

        "Risk_Level":
            risk_level,

    })

    return results