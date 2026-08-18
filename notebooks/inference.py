import os
import time
import warnings
import joblib
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns
from sklearn.metrics import accuracy_score, classification_report, f1_score

warnings.filterwarnings("ignore")

# Set visualization styles
sns.set_theme(style="whitegrid")
plt.rcParams.update({"axes.titlesize": 11, "axes.labelsize": 10})


# -------------------------------------------------------------------------
# 1. Preprocessing Function
# -------------------------------------------------------------------------
def preprocess_input(
    df_input, feature_cols, scaler, log_features=None, verbose=True
):
    """Preprocess raw network flow data for inference.

    Parameters
    ----------
    df_input     : pd.DataFrame — raw network flow data
    feature_cols : list         — expected feature column names
    scaler       : fitted RobustScaler
    log_features : list         — features that need log1p transform
    verbose      : bool         — print processing steps

    Returns
    -------
    X_scaled : np.ndarray — model-ready feature matrix
    """
    df = df_input.copy()

    if verbose:
        print(f"Input shape: {df.shape}")

    # Step 1: Strip column name whitespace
    df.columns = df.columns.str.strip()

    # Step 2: Drop known non-feature columns if present
    DROP_COLS = [
        "Flow ID",
        "Source IP",
        "Destination IP",
        "Timestamp",
        "source_file",
        "Label",
        "y_binary",
        "y_multi",
        "Is_Attack",
        "Fwd Header Length.1",
        "Protocol_Name",
    ]
    df.drop(
        columns=[c for c in DROP_COLS if c in df.columns], inplace=True
    )

    # Step 3: Replace Inf with NaN
    df.replace([np.inf, -np.inf], np.nan, inplace=True)

    # Step 4: Feature engineering (match training)
    def safe(col):
        return (
            df[col] if col in df.columns else pd.Series(0, index=df.index)
        )

    fwd = safe("Total Fwd Packets")
    bwd = safe("Total Backward Packets")
    df["Fwd_Bwd_Pkt_Ratio"] = fwd / (fwd + bwd + 1)
    df["Bytes_Per_Packet"] = safe("Flow Bytes/s") / (
        safe("Flow Packets/s") + 1
    )
    df["Header_Payload_Ratio"] = safe("Fwd Header Length") / (
        safe("Total Length of Fwd Packets") + 1
    )
    df["IAT_Fwd_Bwd_Ratio"] = safe("Fwd IAT Mean") / (
        safe("Bwd IAT Mean") + 1
    )
    df["Pkt_Size_Asymmetry"] = safe("Fwd Packet Length Mean") - safe(
        "Bwd Packet Length Mean"
    )
    df["Win_Size_Ratio"] = safe("Init_Win_bytes_forward") / (
        safe("Init_Win_bytes_backward").abs() + 1
    )
    for flag, src in [
        ("Has_SYN", "SYN Flag Count"),
        ("Has_RST", "RST Flag Count"),
        ("Has_FIN", "FIN Flag Count"),
    ]:
        df[flag] = (safe(src) > 0).astype(int)

    # Step 5: Log transforms
    if log_features:
        for feat in log_features:
            orig = feat.replace("log_", "")
            if orig in df.columns:
                df[feat] = np.log1p(df[orig].clip(lower=0))

    # Step 6: Fill any remaining NaN with 0
    df.fillna(0, inplace=True)

    # Step 7: Align columns to training feature set
    missing_cols = set(feature_cols) - set(df.columns)
    extra_cols = set(df.columns) - set(feature_cols)

    if verbose and missing_cols:
        print(f"  ⚠️  Missing columns filled with 0: {missing_cols}")
    if verbose and extra_cols:
        print(f"  ℹ️  Extra columns dropped: {len(extra_cols)}")

    # Add missing columns as 0
    for col in missing_cols:
        df[col] = 0

    # Select and reorder to match training
    X = df[feature_cols].values

    # Step 8: Scale
    X_scaled = scaler.transform(X)

    if verbose:
        print(f"Output shape : {X_scaled.shape}")
        print("✅ Preprocessing complete")

    return X_scaled


# -------------------------------------------------------------------------
# 2. Prediction Function
# -------------------------------------------------------------------------
def predict_traffic(
    df_input,
    model,
    scaler,
    le,
    feature_cols,
    log_features=None,
    threshold=0.5,
    verbose=True,
):
    """Predict attack type for raw network flow data.

    Parameters
    ----------
    df_input     : pd.DataFrame — raw network flows
    model        : fitted classifier
    scaler       : fitted RobustScaler
    le           : fitted LabelEncoder
    feature_cols : list of expected feature names
    log_features : list of log-transformed feature names
    threshold    : float — min confidence to flag as ATTACK
    verbose      : bool  — print prediction summary

    Returns
    -------
    results_df : pd.DataFrame with columns:
                 Predicted_Label, Confidence, Is_Attack, Risk_Level
    """
    start = time.time()

    # Preprocess
    X_scaled = preprocess_input(
        df_input, feature_cols, scaler, log_features, verbose
    )

    # Predict
    y_pred = model.predict(X_scaled)
    y_prob = model.predict_proba(X_scaled)
    confidence = y_prob.max(axis=1) * 100

    # Decode labels
    pred_labels = le.inverse_transform(y_pred)
    is_attack = (pred_labels != "BENIGN").astype(int)

    # Risk level based on confidence
    def risk_level(label, conf):
        if label == "BENIGN":
            return "SAFE"
        elif conf >= 90:
            return "🔴 HIGH"
        elif conf >= 70:
            return "🟠 MEDIUM"
        else:
            return "🟡 LOW"

    risk = [risk_level(l, c) for l, c in zip(pred_labels, confidence)]

    elapsed = time.time() - start

    # Build results DataFrame
    results_df = pd.DataFrame(
        {
            "Predicted_Label": pred_labels,
            "Confidence (%)": confidence.round(2),
            "Is_Attack": is_attack,
            "Risk_Level": risk,
        }
    )

    # Add per-class probabilities
    prob_df = pd.DataFrame(
        y_prob * 100, columns=[f"P({c})" for c in le.classes_]
    ).round(2)
    results_df = pd.concat(
        [results_df.reset_index(drop=True), prob_df.reset_index(drop=True)],
        axis=1,
    )

    if verbose:
        n_attacks = is_attack.sum()
        n_benign = len(is_attack) - n_attacks
        print("\n--- Prediction Summary ---")
        print(f"  Total flows  : {len(results_df):,}")
        print(
            f"  Benign       : {n_benign:,}  ({n_benign/len(results_df)*100:.1f}%)"
        )
        print(
            f"  Attacks      : {n_attacks:,}  ({n_attacks/len(results_df)*100:.1f}%)"
        )
        print(f"  Inference time : {elapsed*1000:.1f} ms")
        if n_attacks > 0:
            print("\n  Attack breakdown:")
            atk = (
                results_df[results_df["Is_Attack"] == 1]["Predicted_Label"]
                .value_counts()
            )
            for label, cnt in atk.items():
                print(f"    {str(label):<40}: {cnt:,}")

    return results_df


def predict_dataframe(
    df,
    model,
    scaler,
    label_encoder,
    feature_cols,
    log_features=None,
    verbose=False,
):
    """
    Predict attacks from a pandas DataFrame.
    """

    return predict_traffic(
        df_input=df,
        model=model,
        scaler=scaler,
        le=label_encoder,
        feature_cols=feature_cols,
        log_features=log_features,
        verbose=verbose,
    )


def predict_from_csv(
    csv_path,
    model,
    scaler,
    label_encoder,
    feature_cols,
    log_features=None,
    verbose=False,
):
    """
    Predict attacks from a CSV file.
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

# -------------------------------------------------------------------------
# Main Execution Pipeline
# -------------------------------------------------------------------------
if __name__ == "__main__":
    MODEL_DIR = "tuned_models"
    PREP_DIR = "preprocessed"

    print("Loading saved artifacts...")
    feat_df = pd.read_csv(f"{PREP_DIR}/feature_names.csv")
    FEATURE_COLS = feat_df.iloc[:, 0].tolist()

    X_test_scaled = np.load(f"{PREP_DIR}/X_test_scaled.npy")
    y_test_multi = np.load(f"{PREP_DIR}/y_test_multi.npy")
    X_test_raw = np.load(f"{PREP_DIR}/X_test.npy")

    X_test_raw_df = pd.DataFrame(X_test_raw, columns=FEATURE_COLS)
    model = joblib.load(f"{MODEL_DIR}/tuned_random_forest.pkl")
    scaler = joblib.load(f"{PREP_DIR}/robust_scaler.pkl")
    le = joblib.load(f"{PREP_DIR}/label_encoder.pkl")

    CLASS_NAMES = [str(c) for c in le.classes_]
    N_CLASSES = len(CLASS_NAMES)

    print("✅ Artifacts loaded successfully")
    print("   Model          : Tuned Random Forest")
    print(f"   Classes        : {N_CLASSES}")
    print(f"   Features       : {len(FEATURE_COLS)}")
    print(f"   Class names    : {CLASS_NAMES}\n")

    # 1. Test single samples
    X_test_df = pd.DataFrame(
        (
            X_test_scaled
            if isinstance(X_test_scaled, np.ndarray)
            else X_test_scaled.values
        ),
        columns=FEATURE_COLS,
    )

    benign_idx = np.where(y_test_multi == le.transform(["BENIGN"])[0])[0][0]
    single_benign = X_test_df.iloc[[benign_idx]].copy()

    attack_idx = np.where(y_test_multi != le.transform(["BENIGN"])[0])[0][0]
    single_attack = X_test_df.iloc[[attack_idx]].copy()

    print("=== Testing on a BENIGN sample ===")
    result_benign = predict_traffic(
        single_benign, model, scaler, le, FEATURE_COLS, verbose=True
    )
    print("\nResult:")
    print(
        result_benign[
            ["Predicted_Label", "Confidence (%)", "Is_Attack", "Risk_Level"]
        ]
    )

    print("\n=== Testing on an ATTACK sample ===")
    result_attack = predict_traffic(
        single_attack, model, scaler, le, FEATURE_COLS, verbose=True
    )
    print("\nResult:")
    print(
        result_attack[
            ["Predicted_Label", "Confidence (%)", "Is_Attack", "Risk_Level"]
        ]
    )

    actual = le.inverse_transform([y_test_multi[attack_idx]])[0]
    print(f"\nActual label : {actual}")
    print(f"Predicted    : {result_attack['Predicted_Label'].iloc[0]}")
    print(f"Correct      : {actual == result_attack['Predicted_Label'].iloc[0]}")

    # 2. Test batch prediction
    np.random.seed(42)
    batch_idx = np.random.choice(len(X_test_df), size=500, replace=False)
    X_batch = X_test_df.iloc[batch_idx].copy()
    y_batch = y_test_multi[batch_idx]

    print(f"\nBatch size: {len(X_batch):,} flows")
    print("Running batch inference...\n")

    batch_results = predict_traffic(
        X_batch, model, scaler, le, FEATURE_COLS, verbose=True
    )

    # 3. Evaluate Batch Accuracy
    actual_labels = le.inverse_transform(y_batch)
    pred_labels = batch_results["Predicted_Label"].values
    correct = (actual_labels == pred_labels).sum()

    print(
        f"\nBatch Accuracy : {correct}/{len(y_batch)} = {correct/len(y_batch)*100:.2f}%"
    )

    wrong_idx = np.where(actual_labels != pred_labels)[0]
    print(f"Misclassified  : {len(wrong_idx)} flows")
    if len(wrong_idx) > 0:
        print("\nMisclassification breakdown:")
        wrong_df = pd.DataFrame(
            {
                "Actual": actual_labels[wrong_idx],
                "Predicted": pred_labels[wrong_idx],
                "Confidence": batch_results["Confidence (%)"].values[wrong_idx],
            }
        )
        print(
            wrong_df.groupby(["Actual", "Predicted"])
            .size()
            .reset_index(name="Count")
            .sort_values("Count", ascending=False)
            .to_string(index=False)
        )

