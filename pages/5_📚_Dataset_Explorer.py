import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt
from src.theme import apply_cybersecurity_theme
apply_cybersecurity_theme()
# ============================================================
# PAGE CONFIGURATION
# ============================================================

st.set_page_config(
    page_title="Dataset Explorer",
    page_icon="📚",
    layout="wide"
)


# ============================================================
# PAGE TITLE
# ============================================================

st.title("📚 Dataset Explorer")

st.markdown(
    """
    Explore and inspect the network traffic dataset used by the
    machine learning-based intrusion detection system.
    """
)

st.divider()


# ============================================================
# FILE UPLOAD
# ============================================================

uploaded = st.file_uploader(
    "📂 Upload Dataset",
    type=["csv", "xlsx", "xls"]
)


if uploaded is None:

    st.info(
        "Upload a CSV or Excel file to begin exploring the dataset."
    )

    st.stop()


# ============================================================
# LOAD DATASET
# ============================================================

try:

    if uploaded.name.lower().endswith(".csv"):

        df = pd.read_csv(
            uploaded,
            low_memory=False
        )

    else:

        df = pd.read_excel(uploaded)

except Exception as e:

    st.error(
        f"❌ Unable to read the dataset: {e}"
    )

    st.stop()


# ============================================================
# BASIC CLEANING FOR EXPLORATION
# ============================================================

df.columns = df.columns.str.strip()


# ============================================================
# DATASET OVERVIEW
# ============================================================

st.subheader("📊 Dataset Overview")


total_rows = len(df)
total_columns = len(df.columns)

missing_cells = int(
    df.isna().sum().sum()
)

duplicate_rows = int(
    df.duplicated().sum()
)


col1, col2, col3, col4 = st.columns(4)


with col1:

    st.metric(
        "Rows",
        f"{total_rows:,}"
    )


with col2:

    st.metric(
        "Columns",
        f"{total_columns:,}"
    )


with col3:

    st.metric(
        "Missing Values",
        f"{missing_cells:,}"
    )


with col4:

    st.metric(
        "Duplicate Rows",
        f"{duplicate_rows:,}"
    )


st.divider()


# ============================================================
# DATA PREVIEW
# ============================================================

st.subheader("👀 Dataset Preview")


preview_rows = st.slider(
    "Number of rows to display",
    min_value=5,
    max_value=100,
    value=10,
    step=5
)


st.dataframe(
    df.head(preview_rows),
    use_container_width=True,
    hide_index=True
)


st.divider()


# ============================================================
# DATA TYPES
# ============================================================

st.subheader("🔤 Feature Information")


feature_info = pd.DataFrame({
    "Feature": df.columns,
    "Data Type": df.dtypes.astype(str).values,
    "Missing Values": df.isna().sum().values,
    "Unique Values": [
        df[col].nunique(dropna=True)
        for col in df.columns
    ]
})


st.dataframe(
    feature_info,
    use_container_width=True,
    hide_index=True
)


st.divider()


# ============================================================
# MISSING VALUE ANALYSIS
# ============================================================

st.subheader("⚠️ Missing Value Analysis")


missing = (
    df.isna()
    .sum()
    .sort_values(ascending=False)
)

missing = missing[missing > 0]


if missing.empty:

    st.success(
        "✅ No missing values were detected."
    )

else:

    missing_df = pd.DataFrame({
        "Feature": missing.index,
        "Missing Values": missing.values,
        "Missing (%)": (
            missing.values / len(df) * 100
        ).round(2)
    })

    st.dataframe(
        missing_df,
        use_container_width=True,
        hide_index=True
    )


st.divider()


# ============================================================
# DUPLICATE ANALYSIS
# ============================================================

st.subheader("🔁 Duplicate Records")


if duplicate_rows == 0:

    st.success(
        "✅ No duplicate rows were detected."
    )

else:

    st.warning(
        f"⚠️ {duplicate_rows:,} duplicate rows were detected."
    )


st.divider()


# ============================================================
# NUMERIC SUMMARY
# ============================================================

st.subheader("📈 Numerical Statistics")


numeric_df = df.select_dtypes(
    include="number"
)


if numeric_df.shape[1] > 0:

    st.dataframe(
        numeric_df.describe()
        .T
        .round(3),
        use_container_width=True
    )

else:

    st.info(
        "No numerical features were found."
    )


st.divider()


# ============================================================
# LABEL / CLASS DISTRIBUTION
# ============================================================

st.subheader("🎯 Class Distribution")


# Look for common label column names
label_candidates = [
    "Label",
    "label",
    "Class",
    "class",
    "y_multi",
    "y_binary"
]


label_column = next(
    (
        col
        for col in label_candidates
        if col in df.columns
    ),
    None
)


if label_column is not None:

    class_counts = (
        df[label_column]
        .value_counts(dropna=False)
    )

    col1, col2 = st.columns(2)


    with col1:

        class_table = pd.DataFrame({
            "Class": class_counts.index.astype(str),
            "Count": class_counts.values,
            "Percentage": (
                class_counts.values
                / len(df)
                * 100
            ).round(2)
        })

        st.dataframe(
            class_table,
            use_container_width=True,
            hide_index=True
        )


    with col2:

        fig, ax = plt.subplots(
            figsize=(7, 5)
        )

        class_counts.plot(
            kind="bar",
            ax=ax
        )

        ax.set_xlabel("Class")
        ax.set_ylabel("Number of Records")
        ax.set_title(
            f"Distribution of {label_column}"
        )

        plt.xticks(
            rotation=45,
            ha="right"
        )

        plt.tight_layout()

        st.pyplot(
            fig,
            use_container_width=True
        )

        plt.close(fig)

else:

    st.info(
        "No standard label/class column was detected "
        "in this dataset."
    )


st.divider()


# ============================================================
# DATASET SUMMARY
# ============================================================

st.subheader("📋 Dataset Summary")


st.write(
    f"""
    **Dataset:** `{uploaded.name}`

    **Rows:** {total_rows:,}

    **Features:** {total_columns:,}

    **Numerical Features:** {numeric_df.shape[1]:,}

    **Categorical Features:** {
        df.select_dtypes(include="object").shape[1]
    :,}

    **Missing Cells:** {missing_cells:,}

    **Duplicate Rows:** {duplicate_rows:,}
    """
)


# ============================================================
# DOWNLOAD
# ============================================================

st.divider()

st.subheader("📥 Export Dataset")


st.download_button(
    label="Download Dataset as CSV",
    data=df.to_csv(index=False).encode("utf-8"),
    file_name="dataset_export.csv",
    mime="text/csv",
    use_container_width=True
)