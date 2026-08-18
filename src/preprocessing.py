import numpy as np
import pandas as pd
from sklearn.base import TransformerMixin


def preprocess_input(
    df_input: pd.DataFrame,
    feature_cols: list[str],
    scaler: TransformerMixin,
    log_features: list[str] | None = None,
    verbose: bool = False,
):
    """
    Preprocess raw CICIDS2017 network-flow data for inference.

    The preprocessing reproduces the engineered features required
    by the trained Random Forest model.
    """

    # ============================================================
    # 1. VALIDATE INPUT
    # ============================================================

    if not isinstance(df_input, pd.DataFrame):
        raise TypeError("df_input must be a pandas DataFrame.")

    if df_input.empty:
        raise ValueError("Input DataFrame is empty.")

    df = df_input.copy()

    if verbose:
        print(f"Input shape: {df.shape}")

    # ============================================================
    # 2. CLEAN COLUMN NAMES
    # ============================================================

    df.columns = (
        df.columns
        .astype(str)
        .str.strip()
    )

    # ============================================================
    # 3. DROP NON-FEATURE COLUMNS
    # ============================================================

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

    existing_drop_cols = [
        col for col in DROP_COLS
        if col in df.columns
    ]

    if existing_drop_cols:
        df.drop(
            columns=existing_drop_cols,
            inplace=True
        )

    # ============================================================
    # 4. CONVERT DATA TO NUMERIC
    # ============================================================

    for col in df.columns:
        df[col] = pd.to_numeric(
            df[col],
            errors="coerce"
        )

    # ============================================================
    # 5. REPLACE INF WITH NaN
    # ============================================================

    df.replace(
        [np.inf, -np.inf],
        np.nan,
        inplace=True
    )

    # ============================================================
    # 6. SAFE COLUMN ACCESS
    # ============================================================

    def safe(column: str) -> pd.Series:

        if column in df.columns:
            return pd.to_numeric(
                df[column],
                errors="coerce"
            ).fillna(0)

        return pd.Series(
            0.0,
            index=df.index
        )

    # ============================================================
    # 7. FEATURE ENGINEERING
    # ============================================================

    fwd_packets = safe(
        "Total Fwd Packets"
    )

    bwd_packets = safe(
        "Total Backward Packets"
    )

    # ------------------------------------------------------------
    # Fwd/Bwd Packet Ratio
    # ------------------------------------------------------------

    df["Fwd_Bwd_Pkt_Ratio"] = (
        fwd_packets /
        (fwd_packets + bwd_packets + 1)
    )

    # ------------------------------------------------------------
    # Bytes Per Packet
    # ------------------------------------------------------------

    flow_bytes = safe(
        "Flow Bytes/s"
    )

    flow_packets = safe(
        "Flow Packets/s"
    )

    df["Bytes_Per_Packet"] = (
        flow_bytes /
        (flow_packets + 1)
    )

    # ------------------------------------------------------------
    # Header Payload Ratio
    # ------------------------------------------------------------

    fwd_header = safe(
        "Fwd Header Length"
    )

    fwd_bytes = safe(
        "Total Length of Fwd Packets"
    )

    df["Header_Payload_Ratio"] = (
        fwd_header /
        (fwd_bytes + 1)
    )

    # ------------------------------------------------------------
    # Forward / Backward IAT Ratio
    # ------------------------------------------------------------

    fwd_iat = safe(
        "Fwd IAT Mean"
    )

    bwd_iat = safe(
        "Bwd IAT Mean"
    )

    df["IAT_Fwd_Bwd_Ratio"] = (
        fwd_iat /
        (bwd_iat + 1)
    )

    # ------------------------------------------------------------
    # Packet Size Asymmetry
    # ------------------------------------------------------------

    fwd_packet_mean = safe(
        "Fwd Packet Length Mean"
    )

    bwd_packet_mean = safe(
        "Bwd Packet Length Mean"
    )

    df["Pkt_Size_Asymmetry"] = (
        fwd_packet_mean -
        bwd_packet_mean
    )

    # ------------------------------------------------------------
    # Window Size Ratio
    # ------------------------------------------------------------

    init_win_forward = safe(
        "Init_Win_bytes_forward"
    )

    init_win_backward = safe(
        "Init_Win_bytes_backward"
    )

    df["Win_Size_Ratio"] = (
        init_win_forward /
        (init_win_backward.abs() + 1)
    )

    # ============================================================
    # 8. TCP FLAG FEATURES
    # ============================================================

    flag_features = {
        "Has_SYN": "SYN Flag Count",
        "Has_RST": "RST Flag Count",
        "Has_FIN": "FIN Flag Count",
    }

    for new_name, source_name in flag_features.items():

        df[new_name] = (
            safe(source_name) > 0
        ).astype(int)

    # ============================================================
    # 9. CREATE REQUIRED LOG FEATURES
    # ============================================================

    # If log_features were supplied, use them.
    # Otherwise automatically identify log_ features
    # from the model's expected feature list.

    required_log_features = [
        feature
        for feature in feature_cols
        if feature.startswith("log_")
    ]

    if log_features is not None:

        required_log_features = list(
            set(required_log_features) |
            set(log_features)
        )

    for log_feature in required_log_features:

        original_feature = log_feature[
            len("log_"):
        ]

        if original_feature in df.columns:

            values = pd.to_numeric(
                df[original_feature],
                errors="coerce"
            ).fillna(0)

            df[log_feature] = np.log1p(
                values.clip(lower=0)
            )

        else:

            # If the original feature doesn't exist,
            # create the required model feature as zero.
            df[log_feature] = 0.0

    # ============================================================
    # 10. FILL REMAINING MISSING VALUES
    # ============================================================

    df.replace(
        [np.inf, -np.inf],
        np.nan,
        inplace=True
    )

    df.fillna(
        0,
        inplace=True
    )

    # ============================================================
    # 11. CHECK FEATURE ALIGNMENT
    # ============================================================

    missing_cols = [
        col
        for col in feature_cols
        if col not in df.columns
    ]

    extra_cols = [
        col
        for col in df.columns
        if col not in feature_cols
    ]

    if verbose:

        print(
            f"Model expects: {len(feature_cols)} features"
        )

        print(
            f"Features available after engineering: "
            f"{len(df.columns)}"
        )

        print(
            f"Missing model features: "
            f"{len(missing_cols)}"
        )

        print(
            f"Extra columns: "
            f"{len(extra_cols)}"
        )

        if missing_cols:

            print("\nMissing features:")

            for col in missing_cols:
                print(f" - {col}")

    # ============================================================
    # 12. STOP IF REQUIRED FEATURES ARE STILL MISSING
    # ============================================================

    if missing_cols:

        raise ValueError(
            "Required model features are missing after "
            "preprocessing:\n"
            + "\n".join(
                f" - {col}"
                for col in missing_cols
            )
        )

    # ============================================================
    # 13. SELECT EXACT MODEL FEATURES
    # ============================================================

    X = df[
        feature_cols
    ].copy()

    # Ensure numeric
    X = X.apply(
        pd.to_numeric,
        errors="coerce"
    )

    X.fillna(
        0,
        inplace=True
    )

    # ============================================================
    # 14. SCALE USING DATAFRAME
    # ============================================================

    try:

        X_scaled = scaler.transform(X)

    except Exception as e:

        raise RuntimeError(
            "Scaling failed. "
            "Check that the inference features match "
            "the features used when fitting the scaler."
        ) from e

    # ============================================================
    # 15. FINAL VALIDATION
    # ============================================================

    if verbose:

        print(
            f"\nOutput shape: {X_scaled.shape}"
        )

        print(
            "Expected shape: "
            f"(number_of_rows, {len(feature_cols)})"
        )

        print(
            "NaN values:",
            np.isnan(X_scaled).sum()
        )

        print(
            "Infinite values:",
            np.isinf(X_scaled).sum()
        )

        print(
            "✅ Preprocessing complete"
        )

    return X_scaled