import streamlit as st
from datetime import datetime
from src.theme import apply_cybersecurity_theme
# ============================================================
# PAGE CONFIGURATION
# ============================================================

st.set_page_config(
    page_title="Security Alerts",
    page_icon="⚠️",
    layout="wide"
)

apply_cybersecurity_theme()
# ============================================================
# PAGE TITLE
# ============================================================

st.title("🚨 Alerts & Incident Management")

st.write(
    "Monitor detected security threats and identify "
    "high-priority network intrusion incidents."
)

st.divider()


# ============================================================
# GET PREDICTION RESULTS
# ============================================================

results = None

# Priority:
# 1. realtime_results
# 2. realtime_live_results
# 3. batch_results

if "realtime_results" in st.session_state:

    results = st.session_state[
        "realtime_results"
    ].copy()

elif "realtime_live_results" in st.session_state:

    results = st.session_state[
        "realtime_live_results"
    ].copy()

elif "batch_results" in st.session_state:

    results = st.session_state[
        "batch_results"
    ].copy()


# ============================================================
# CHECK WHETHER RESULTS EXIST
# ============================================================

if results is None or results.empty:

    st.warning(
        "⚠️ No prediction results are available yet."
    )

    st.info(
        "Please run the Real-Time Monitor or Batch "
        "Prediction first."
    )

    st.stop()


# ============================================================
# DISPLAY AVAILABLE COLUMNS
# ============================================================

# This is useful while testing.
# You can remove it later.

# st.write("Available columns:", list(results.columns))


# ============================================================
# CREATE Is_Attack IF IT DOES NOT EXIST
# ============================================================

if "Is_Attack" not in results.columns:

    if "Predicted_Label" not in results.columns:

        st.error(
            "❌ Prediction results do not contain "
            "'Predicted_Label'."
        )

        st.write(
            "Available columns:",
            list(results.columns)
        )

        st.stop()


    # --------------------------------------------------------
    # CICIDS2017:
    # BENIGN = normal traffic
    # Everything else = attack
    # --------------------------------------------------------

    results["Is_Attack"] = (
        results["Predicted_Label"]
        .astype(str)
        .str.strip()
        .str.upper()
        .ne("BENIGN")
    )


# ============================================================
# CREATE ALERT TIME IF MISSING
# ============================================================

if "Alert_Time" not in results.columns:

    results["Alert_Time"] = (
        datetime.now().strftime(
            "%Y-%m-%d %H:%M:%S"
        )
    )


# ============================================================
# CREATE ALERT ID IF MISSING
# ============================================================

if "Alert_ID" not in results.columns:

    alert_ids = []

    for i in range(len(results)):

        alert_ids.append(
            f"ALT-{i + 1:06d}"
        )

    results["Alert_ID"] = alert_ids


# ============================================================
# CREATE CONFIDENCE COLUMN IF MISSING
# ============================================================

if "Confidence (%)" not in results.columns:

    results["Confidence (%)"] = 0.0


# ============================================================
# CREATE RISK LEVEL IF MISSING
# ============================================================

if "Risk_Level" not in results.columns:

    def calculate_risk(row):

        # Benign traffic
        if not row["Is_Attack"]:
            return "Low"

        try:

            confidence = float(
                row["Confidence (%)"]
            )

        except:

            confidence = 0


        if confidence >= 80:

            return "High"

        elif confidence >= 50:

            return "Medium"

        else:

            return "Low"


    results["Risk_Level"] = (
        results.apply(
            calculate_risk,
            axis=1
        )
    )


# ============================================================
# EXTRACT ONLY ATTACKS
# ============================================================

alerts = results[
    results["Is_Attack"] == True
].copy()


# ============================================================
# CHECK FOR ATTACKS
# ============================================================

if alerts.empty:

    st.success(
        "✅ No security attacks were detected."
    )

    st.info(
        "The prediction results contain traffic, "
        "but no records were classified as attacks."
    )

    st.stop()


# ============================================================
# ALERT SUMMARY
# ============================================================

total_alerts = len(alerts)

high_risk = (
    alerts["Risk_Level"]
    .astype(str)
    .str.lower()
    .eq("high")
    .sum()
)

medium_risk = (
    alerts["Risk_Level"]
    .astype(str)
    .str.lower()
    .eq("medium")
    .sum()
)

low_risk = (
    alerts["Risk_Level"]
    .astype(str)
    .str.lower()
    .eq("low")
    .sum()
)


# ============================================================
# SUMMARY METRICS
# ============================================================

col1, col2, col3, col4 = st.columns(4)

with col1:

    st.metric(
        "🚨 Total Alerts",
        f"{total_alerts:,}"
    )

with col2:

    st.metric(
        "🔴 High Risk",
        f"{high_risk:,}"
    )

with col3:

    st.metric(
        "🟠 Medium Risk",
        f"{medium_risk:,}"
    )

with col4:

    st.metric(
        "🟢 Low Risk",
        f"{low_risk:,}"
    )


st.divider()


# ============================================================
# FILTERS
# ============================================================

st.subheader("🔎 Alert Filters")

filter_col1, filter_col2 = st.columns(2)


# ------------------------------------------------------------
# FILTER BY RISK LEVEL
# ------------------------------------------------------------

with filter_col1:

    risk_options = [
        "All",
        "High",
        "Medium",
        "Low"
    ]

    selected_risk = st.selectbox(
        "Risk Level",
        risk_options
    )


# ------------------------------------------------------------
# FILTER BY ATTACK TYPE
# ------------------------------------------------------------

with filter_col2:

    attack_types = sorted(
        alerts[
            "Predicted_Label"
        ]
        .astype(str)
        .unique()
        .tolist()
    )

    selected_attack = st.selectbox(
        "Attack Type",
        ["All"] + attack_types
    )


# ============================================================
# APPLY FILTERS
# ============================================================

filtered_alerts = alerts.copy()


if selected_risk != "All":

    filtered_alerts = filtered_alerts[
        filtered_alerts["Risk_Level"]
        .astype(str)
        .str.lower()
        ==
        selected_risk.lower()
    ]


if selected_attack != "All":

    filtered_alerts = filtered_alerts[
        filtered_alerts["Predicted_Label"]
        .astype(str)
        ==
        selected_attack
    ]


# ============================================================
# DISPLAY ALERT COUNT
# ============================================================

st.write(
    f"Showing **{len(filtered_alerts):,}** "
    f"security alert(s)"
)


# ============================================================
# SELECT DISPLAY COLUMNS
# ============================================================

display_columns = [
    "Alert_ID",
    "Alert_Time",
    "Predicted_Label",
    "Confidence (%)",
    "Is_Attack",
    "Risk_Level"
]


# Only use columns that actually exist

display_columns = [
    column
    for column in display_columns
    if column in filtered_alerts.columns
]


# ============================================================
# DISPLAY ALERT TABLE
# ============================================================

st.subheader("🚨 Detected Security Alerts")

st.dataframe(
    filtered_alerts[
        display_columns
    ],
    width="stretch",
    hide_index=True
)


# ============================================================
# ATTACK DISTRIBUTION
# ============================================================

st.divider()

st.subheader("📊 Attack Distribution")

attack_distribution = (
    filtered_alerts[
        "Predicted_Label"
    ]
    .value_counts()
    .reset_index()
)

attack_distribution.columns = [
    "Attack Type",
    "Count"
]

st.dataframe(
    attack_distribution,
    width="stretch",
    hide_index=True
)


# ============================================================
# DOWNLOAD ALERTS
# ============================================================

st.divider()

csv_data = filtered_alerts[
    display_columns
].to_csv(
    index=False
).encode("utf-8")


st.download_button(
    label="⬇️ Download Alerts as CSV",
    data=csv_data,
    file_name="security_alerts.csv",
    mime="text/csv",
    width="stretch"
)