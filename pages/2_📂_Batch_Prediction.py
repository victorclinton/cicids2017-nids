import streamlit as st
import pandas as pd
import plotly.express as px
from src.model_loader import load_artifacts
from src.inference import predict_dataframe
from src.theme import apply_cybersecurity_theme
apply_cybersecurity_theme()
# ============================================================
# PAGE CONFIGURATION
# ============================================================

st.set_page_config(
    page_title="Batch Prediction",
    page_icon="🛡️",
    layout="wide",
)


# ============================================================
# PAGE TITLE
# ============================================================

st.title("🛡️ Batch Network Intrusion Detection")

st.markdown(
    """
Upload a CICIDS2017 network traffic file and use the trained
Random Forest model to detect network attacks.

**Supported formats:** CSV and Excel (`.xlsx`, `.xls`)
"""
)


# ============================================================
# LOAD MODEL ARTIFACTS
# ============================================================

@st.cache_resource
def get_artifacts():

    return load_artifacts()


try:

    model, scaler, label_encoder, feature_cols = get_artifacts()

except Exception as e:

    st.error(
        f"❌ Failed to load model artifacts: {e}"
    )

    st.stop()


# ============================================================
# FILE UPLOAD
# ============================================================

st.subheader("📁 Upload Network Traffic")

uploaded_file = st.file_uploader(
    "Choose a CSV or Excel file",
    type=["csv", "xlsx", "xls"],
    help=(
        "Upload a CICIDS2017 network traffic file "
        "containing the raw network-flow features."
    ),
)


# ============================================================
# READ UPLOADED FILE
# ============================================================

if uploaded_file is not None:

    try:

        file_name = uploaded_file.name.lower()

        # ----------------------------------------------------
        # CSV
        # ----------------------------------------------------

        if file_name.endswith(".csv"):

            df = pd.read_csv(
                uploaded_file,
                low_memory=False
            )

        # ----------------------------------------------------
        # EXCEL
        # ----------------------------------------------------

        elif file_name.endswith(
            (".xlsx", ".xls")
        ):

            df = pd.read_excel(
                uploaded_file
            )

        else:

            st.error(
                "❌ Unsupported file format."
            )

            st.stop()

    except Exception as e:

        st.error(
            f"❌ Could not read the uploaded file: {e}"
        )

        st.stop()

    # ========================================================
    # FILE INFORMATION
    # ========================================================

    st.success(
        f"✅ File loaded successfully: "
        f"**{uploaded_file.name}**"
    )

    col1, col2, col3 = st.columns(3)

    with col1:

        st.metric(
            "Rows",
            f"{len(df):,}"
        )

    with col2:

        st.metric(
            "Columns",
            f"{len(df.columns):,}"
        )

    with col3:

        st.metric(
            "Model Features",
            f"{len(feature_cols):,}"
        )

    # ========================================================
    # DATA PREVIEW
    # ========================================================

    with st.expander(
        "👁️ Preview Uploaded Data",
        expanded=False
    ):

        st.dataframe(
            df.head(100),
            use_container_width=True,
            height=400
        )

    # ========================================================
    # RUN PREDICTION
    # ========================================================

    st.divider()

    run_prediction = st.button(
        "🚀 Run Intrusion Detection",
        type="primary",
        use_container_width=True
    )

    if run_prediction:

        try:

            # ------------------------------------------------
            # Run inference
            # ------------------------------------------------

            with st.spinner(
                "🔄 Processing network traffic and "
                "running predictions..."
            ):

                results = predict_dataframe(
                    df=df,
                    model=model,
                    scaler=scaler,
                    label_encoder=label_encoder,
                    feature_cols=feature_cols,
                    log_features=None,
                    verbose=False,
            )

            # Store results in session state
            st.session_state[
                "batch_results"
            ] = results

            st.success(
                "✅ Prediction completed successfully."
            )

        except Exception as e:

            st.error(
                f"❌ Prediction failed: {e}"
            )

            st.stop()


# ============================================================
# DISPLAY RESULTS
# ============================================================

if "batch_results" in st.session_state:

    results = st.session_state[
        "batch_results"
    ]

    st.divider()

    st.header(
        "📊 Detection Results"
    )

    # ========================================================
    # BASIC COUNTS
    # ========================================================

    total_records = len(results)

    attack_count = int(
        results["Is_Attack"].sum()
    )

    benign_count = (
        total_records -
        attack_count
    )

    attack_percentage = (
        attack_count /
        total_records *
        100
        if total_records > 0
        else 0
    )

    high_count = int(
        (results["Risk_Level"] == "High").sum()
    )

    medium_count = int(
        (results["Risk_Level"] == "Medium").sum()
    )

    low_count = int(
        (results["Risk_Level"] == "Low").sum()
    )

    # ========================================================
    # METRICS
    # ========================================================

    col1, col2, col3, col4 = st.columns(4)

    with col1:

        st.metric(
            "Total Traffic",
            f"{total_records:,}"
        )

    with col2:

        st.metric(
            "Detected Attacks",
            f"{attack_count:,}"
        )

    with col3:

        st.metric(
            "Benign Traffic",
            f"{benign_count:,}"
        )

    with col4:

        st.metric(
            "Attack Rate",
            f"{attack_percentage:.2f}%"
        )

    # ========================================================
    # RISK METRICS
    # ========================================================

    st.subheader(
        "⚠️ Risk Distribution"
    )

    col1, col2, col3 = st.columns(3)

    with col1:

        st.metric(
            "🟢 Low Risk",
            f"{low_count:,}"
        )

    with col2:

        st.metric(
            "🟡 Medium Risk",
            f"{medium_count:,}"
        )

    with col3:

        st.metric(
            "🔴 High Risk",
            f"{high_count:,}"
        )

# ============================================================
# DISPLAY RESULTS
# ============================================================


if "batch_results" in st.session_state:

    results = st.session_state["batch_results"]

    # ========================================================
    # SUMMARY STATISTICS
    # ========================================================

    total_records = len(results)

    attack_count = int(
        results["Is_Attack"].sum()
    )

    benign_count = (
        total_records - attack_count
    )

    attack_percentage = (
        attack_count / total_records * 100
        if total_records > 0
        else 0
    )

    high_count = int(
        (results["Risk_Level"] == "High").sum()
    )

    medium_count = int(
        (results["Risk_Level"] == "Medium").sum()
    )

    low_count = int(
        (results["Risk_Level"] == "Low").sum()
    )

    
    # ========================================================
    # VISUAL ANALYTICS
    # ========================================================

    st.divider()

    st.header("📈 Visual Analytics")

    # --------------------------------------------------------
    # Attack vs Benign
    # --------------------------------------------------------

    st.subheader("🛡️ Benign vs Attack Traffic")

    attack_vs_benign = pd.DataFrame({
        "Traffic Type": [
            "Benign",
            "Attack"
        ],
        "Count": [
            benign_count,
            attack_count
        ]
    })

    fig_attack = px.pie(
        attack_vs_benign,
        names="Traffic Type",
        values="Count",
        hole=0.45,
        title="Benign vs Attack Traffic"
    )

    fig_attack.update_traces(
        textposition="inside",
        textinfo="label+percent"
    )

    st.plotly_chart(
        fig_attack,
        use_container_width=True
    )

    # --------------------------------------------------------
    # Attack Type + Risk Distribution
    # --------------------------------------------------------

    col1, col2 = st.columns(2)

    # ========================================================
    # ATTACK TYPE DISTRIBUTION
    # ========================================================

    with col1:

        st.subheader("🎯 Attack Type Distribution")

        attack_results = results[
            results["Is_Attack"] == True
        ]

        attack_counts = (
            attack_results[
                "Predicted_Label"
            ]
            .value_counts()
            .reset_index()
        )

        attack_counts.columns = [
            "Attack Type",
            "Count"
        ]

        if not attack_counts.empty:

            fig_attacks = px.bar(
                attack_counts,
                x="Count",
                y="Attack Type",
                orientation="h",
                title="Detected Attack Types"
            )

            fig_attacks.update_layout(
                height=550,
                yaxis=dict(
                    categoryorder="total ascending"
                )
            )

            st.plotly_chart(
                fig_attacks,
                use_container_width=True
            )

        else:

            st.info(
                "No attacks were detected."
            )

    # ========================================================
    # RISK DISTRIBUTION
    # ========================================================

    with col2:

        st.subheader("⚠️ Risk Distribution")

        risk_counts = (
            results[
                "Risk_Level"
            ]
            .value_counts()
            .reset_index()
        )

        risk_counts.columns = [
            "Risk Level",
            "Count"
        ]

        fig_risk = px.bar(
            risk_counts,
            x="Risk Level",
            y="Count",
            title="Risk Level Distribution"
        )

        fig_risk.update_layout(
            height=550
        )

        st.plotly_chart(
            fig_risk,
            use_container_width=True
        )

    # ========================================================
    # TOP 10 ATTACK TYPES
    # ========================================================

    st.subheader("🔝 Top 10 Detected Attack Types")

    if not attack_counts.empty:

        top_attacks = attack_counts.head(10)

        fig_top = px.bar(
            top_attacks,
            x="Attack Type",
            y="Count",
            title="Top 10 Detected Attack Types"
        )

        fig_top.update_layout(
            height=450,
            xaxis_tickangle=-45
        )

        st.plotly_chart(
            fig_top,
            use_container_width=True
        )

    # ========================================================
    # ATTACK SUMMARY
    # ========================================================

    st.subheader("📋 Attack Summary")

    if not attack_counts.empty:

        attack_summary = attack_counts.copy()

        attack_summary["Percentage"] = (
            attack_summary["Count"]
            / attack_count
            * 100
        ).round(2)

        attack_summary = attack_summary.rename(
            columns={
                "Count": "Detected Count"
            }
        )

        st.dataframe(
            attack_summary,
            use_container_width=True,
            hide_index=True
        )

    # ========================================================
    # PREDICTION RESULTS
    # ========================================================

    st.subheader("🔎 Prediction Results")

    st.dataframe(
        results.head(500),
        use_container_width=True,
        height=500
    )

    st.caption(
        "Showing the first 500 predictions. "
        "Download the complete results below."
    )

    # ========================================================
    # DOWNLOAD CSV
    # ========================================================

    csv_data = results.to_csv(
        index=False
    ).encode("utf-8")

    st.download_button(
        label="⬇️ Download Results as CSV",
        data=csv_data,
        file_name="intrusion_detection_results.csv",
        mime="text/csv",
        use_container_width=True
    )

    # ========================================================
    # DOWNLOAD EXCEL
    # ========================================================

    try:

        import io

        excel_buffer = io.BytesIO()

        with pd.ExcelWriter(
            excel_buffer,
            engine="openpyxl"
        ) as writer:

            results.to_excel(
                writer,
                index=False,
                sheet_name="Predictions"
            )

        excel_buffer.seek(0)

        st.download_button(
            label="⬇️ Download Results as Excel",
            data=excel_buffer,
            file_name="intrusion_detection_results.xlsx",
            mime=(
                "application/vnd.openxmlformats-"
                "officedocument.spreadsheetml.sheet"
            ),
            use_container_width=True
        )

    except Exception as e:

        st.warning(
            f"Excel download unavailable: {e}"
        )