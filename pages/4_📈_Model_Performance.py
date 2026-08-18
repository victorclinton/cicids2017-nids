import streamlit as st
import pandas as pd
import numpy as np
from pathlib import Path
import plotly.express as px
from src.theme import apply_cybersecurity_theme
apply_cybersecurity_theme()
# ============================================================
# PAGE CONFIG
# ============================================================

st.set_page_config(
    page_title="Model Performance",
    page_icon="📈",
    layout="wide"
)


# ============================================================
# PROJECT PATH
# ============================================================


RESULTS_DIR = Path(
    r"C:\Users\USER\Desktop\CICDS2017-nids\results"
)

PERFORMANCE_FILE = RESULTS_DIR / "model_performance.csv"
CONFUSION_FILE = RESULTS_DIR / "rf_confusion_matrix.csv"
REPORT_FILE = RESULTS_DIR / "rf_classification_report.csv"
# ============================================================
# TITLE
# ============================================================

st.title("📈 Model Performance")

st.markdown(
    """
    Evaluate the performance of the trained machine learning
    model used for network intrusion detection.
    """
)

st.divider()


# ============================================================
# CHECK RESULTS DIRECTORY
# ============================================================

if not RESULTS_DIR.exists():

    st.error(
        f"❌ Results directory was not found:\n\n"
        f"`{RESULTS_DIR}`"
    )

    st.stop()


# ============================================================
# CHECK PERFORMANCE FILE
# ============================================================

if not PERFORMANCE_FILE.exists():

    st.warning(
        "⚠️ Model performance results have not been generated yet."
    )

    st.info(
        """
        Run the Random Forest training/evaluation script first.
        """
    )

    st.stop()


# ============================================================
# LOAD MODEL PERFORMANCE
# ============================================================

try:

    performance_df = pd.read_csv(
        PERFORMANCE_FILE
    )

except Exception as e:

    st.error(
        f"❌ Could not load model performance file:\n\n{e}"
    )

    st.stop()


# ============================================================
# VALIDATE PERFORMANCE COLUMNS
# ============================================================

required_columns = [
    "Model",
    "Accuracy",
    "Precision",
    "Recall",
    "F1_Score"
]

missing_columns = [
    column
    for column in required_columns
    if column not in performance_df.columns
]

if missing_columns:

    st.error(
        "❌ The model performance file is missing "
        f"these columns: {missing_columns}"
    )

    st.stop()


# ============================================================
# CONVERT METRICS TO NUMERIC
# ============================================================

metric_columns = [
    "Accuracy",
    "Precision",
    "Recall",
    "F1_Score"
]

if "Macro_F1" in performance_df.columns:

    metric_columns.append("Macro_F1")

if "ROC_AUC" in performance_df.columns:

    metric_columns.append("ROC_AUC")


for column in metric_columns:

    performance_df[column] = pd.to_numeric(
        performance_df[column],
        errors="coerce"
    )


# ============================================================
# MODEL SELECTION
# ============================================================

st.subheader("🤖 Model Selection")

selected_model = st.selectbox(
    "Select model:",
    performance_df["Model"].dropna().unique()
)


selected_row = performance_df[
    performance_df["Model"] == selected_model
].iloc[0]


# ============================================================
# MAIN METRICS
# ============================================================

st.subheader("📊 Evaluation Metrics")

col1, col2, col3, col4, col5 = st.columns(5)


with col1:

    st.metric(
        "Accuracy",
        f"{selected_row['Accuracy'] * 100:.2f}%"
    )


with col2:

    st.metric(
        "Precision",
        f"{selected_row['Precision'] * 100:.2f}%"
    )


with col3:

    st.metric(
        "Recall",
        f"{selected_row['Recall'] * 100:.2f}%"
    )


with col4:

    st.metric(
        "Weighted F1",
        f"{selected_row['F1_Score'] * 100:.2f}%"
    )


with col5:

    if "Macro_F1" in performance_df.columns:

        st.metric(
            "Macro F1",
            f"{selected_row['Macro_F1'] * 100:.2f}%"
        )

    else:

        st.metric(
            "Macro F1",
            "N/A"
        )


# ============================================================
# ROC-AUC
# ============================================================

if "ROC_AUC" in performance_df.columns:

    st.metric(
        "ROC-AUC",
        f"{selected_row['ROC_AUC'] * 100:.2f}%"
    )


st.divider()


# ============================================================
# MODEL COMPARISON
# ============================================================

st.subheader("⚖️ Model Comparison")

comparison_columns = [
    "Model",
    "Accuracy",
    "Precision",
    "Recall",
    "F1_Score"
]

if "Macro_F1" in performance_df.columns:

    comparison_columns.append("Macro_F1")

if "ROC_AUC" in performance_df.columns:

    comparison_columns.append("ROC_AUC")


comparison_df = performance_df[
    comparison_columns
].copy()


for column in comparison_columns[1:]:

    comparison_df[column] = (
        comparison_df[column] * 100
    ).round(2)


comparison_df = comparison_df.rename(
    columns={
        "F1_Score": "Weighted F1",
        "Macro_F1": "Macro F1",
        "ROC_AUC": "ROC-AUC"
    }
)


st.dataframe(
    comparison_df,
    use_container_width=True,
    hide_index=True
)


# ============================================================
# PERFORMANCE CHART
# ============================================================

st.subheader("📊 Performance Comparison")

chart_df = comparison_df.set_index(
    "Model"
)


chart_columns = [
    column
    for column in [
        "Accuracy",
        "Precision",
        "Recall",
        "Weighted F1",
        "Macro F1"
    ]
    if column in chart_df.columns
]


st.bar_chart(
    chart_df[chart_columns]
)


# ============================================================
# BEST MODEL
# ============================================================

st.divider()

st.subheader("🏆 Best Performing Model")


best_model_row = performance_df.loc[
    performance_df["F1_Score"].idxmax()
]


st.success(
    f"""
    **Best Model:** {best_model_row['Model']}

    **Accuracy:** {best_model_row['Accuracy'] * 100:.2f}%

    **Weighted F1:** {best_model_row['F1_Score'] * 100:.2f}%

    **Precision:** {best_model_row['Precision'] * 100:.2f}%

    **Recall:** {best_model_row['Recall'] * 100:.2f}%
    """
)


# ============================================================
# CONFUSION MATRIX
# ============================================================

st.divider()

st.header("🔢 Confusion Matrix")

if not CONFUSION_FILE.exists():

    st.warning(
        "⚠️ Confusion matrix file was not found."
    )

else:

    try:

        cm_df = pd.read_csv(
            CONFUSION_FILE,
            index_col=0
        )

        cm_df.index = cm_df.index.astype(str)
        cm_df.columns = cm_df.columns.astype(str)

        st.caption(
            f"Confusion matrix for: **{selected_model}**"
        )

        # ----------------------------------------------------
        # Heatmap
        # ----------------------------------------------------

        fig_cm = px.imshow(
            cm_df,
            text_auto=True,
            aspect="auto",
            labels={
                "x": "Predicted Class",
                "y": "Actual Class",
                "color": "Number of Samples"
            },
            title="Random Forest Confusion Matrix"
        )

        fig_cm.update_layout(
            height=750
        )

        st.plotly_chart(
            fig_cm,
            use_container_width=True
        )

        # ----------------------------------------------------
        # Raw matrix
        # ----------------------------------------------------

        with st.expander(
            "🔍 View Confusion Matrix Data"
        ):

            st.dataframe(
                cm_df,
                use_container_width=True
            )

    except Exception as e:

        st.error(
            f"❌ Could not load confusion matrix:\n\n{e}"
        )


# ============================================================
# CLASSIFICATION REPORT
# ============================================================

st.divider()

st.header("📋 Classification Report")

if not REPORT_FILE.exists():

    st.warning(
        "⚠️ Classification report file was not found."
    )

else:

    try:

        report_df = pd.read_csv(
            REPORT_FILE,
            index_col=0
        )

        # Remove unnecessary support formatting issues
        report_df = report_df.replace(
            [np.inf, -np.inf],
            np.nan
        )

        st.caption(
            "Performance for each individual network traffic class."
        )

        # ----------------------------------------------------
        # Display formatted report
        # ----------------------------------------------------

        display_report = report_df.copy()

        for column in [
            "precision",
            "recall",
            "f1-score"
        ]:

            if column in display_report.columns:

                display_report[column] = (
                    display_report[column] * 100
                ).round(2)

        if "support" in display_report.columns:

            display_report["support"] = (
                display_report["support"]
                .round(0)
                .astype("Int64")
            )

        st.dataframe(
            display_report,
            use_container_width=True
        )

        # ----------------------------------------------------
        # Class-level F1 chart
        # ----------------------------------------------------

        class_report = report_df.copy()

        # Remove summary rows
        summary_rows = [
            "accuracy",
            "macro avg",
            "weighted avg"
        ]

        class_report = class_report[
            ~class_report.index.isin(summary_rows)
        ]

        if "f1-score" in class_report.columns:

            f1_chart = (
                class_report[
                    ["f1-score"]
                ]
                .reset_index()
            )

            f1_chart.columns = [
                "Class",
                "F1 Score"
            ]

            f1_chart["F1 Score"] = (
                f1_chart["F1 Score"] * 100
            ).round(2)

            fig_f1 = px.bar(
                f1_chart,
                x="F1 Score",
                y="Class",
                orientation="h",
                text="F1 Score",
                title="F1-Score by Network Traffic Class"
            )

            fig_f1.update_traces(
                texttemplate="%{text:.2f}%",
                textposition="outside"
            )

            fig_f1.update_layout(
                height=650,
                yaxis={
                    "categoryorder": "total ascending"
                }
            )

            st.plotly_chart(
                fig_f1,
                use_container_width=True
            )

    except Exception as e:

        st.error(
            f"❌ Could not load classification report:\n\n{e}"
        )


# ============================================================
# INTERPRETATION
# ============================================================

st.divider()

st.header("📝 Performance Interpretation")

accuracy = selected_row["Accuracy"] * 100
precision = selected_row["Precision"] * 100
recall = selected_row["Recall"] * 100
f1 = selected_row["F1_Score"] * 100


st.markdown(
    f"""
    The **{selected_model}** achieved an overall accuracy of
    **{accuracy:.2f}%** on the test data.

    Its weighted precision was **{precision:.2f}%**, while its
    weighted recall was **{recall:.2f}%**. The weighted F1-score
    was **{f1:.2f}%**.

    The confusion matrix provides additional information about
    how well the model distinguishes between the different
    network traffic classes, while the classification report
    provides class-level precision, recall and F1-scores.
    """
)


# ============================================================
# RAW PERFORMANCE DATA
# ============================================================

with st.expander("🔍 View Raw Model Performance Data"):

    st.dataframe(
        performance_df,
        use_container_width=True,
        hide_index=True
    )


# ============================================================
# FOOTER
# ============================================================

st.divider()

st.caption(
    "Machine Learning Based Network Intrusion Detection "
    "System for Securing E-Voting Systems"
)