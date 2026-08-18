import streamlit as st
import plotly.express as px
from src.theme import apply_cybersecurity_theme
apply_cybersecurity_theme()
# ============================================================
# PAGE CONFIGURATION
# ============================================================

st.set_page_config(
    page_title="Attack Analysis",
    page_icon="🎯",
    layout="wide",
)


# ============================================================
# TITLE
# ============================================================

st.title("🎯 Attack Analysis")

st.markdown(
    """
Analyze the attacks detected by the machine learning model,
including attack types, frequency, confidence and risk levels.
"""
)

st.divider()


# ============================================================
# CHECK FOR PREDICTION RESULTS
# ============================================================

if "batch_results" not in st.session_state:

    st.info(
        "ℹ️ No prediction results are currently available."
    )

    st.markdown(
        """
        Please go to **Batch Prediction**, upload a CSV or
        Excel file, and run the intrusion detection model first.
        """
    )

    st.stop()


# ============================================================
# LOAD RESULTS
# ============================================================

results = st.session_state["batch_results"].copy()


# ============================================================
# BASIC STATISTICS
# ============================================================

total_records = len(results)

attack_results = results[
    results["Is_Attack"] == True
].copy()

attack_count = len(attack_results)

benign_count = (
    total_records - attack_count
)

attack_rate = (
    attack_count / total_records * 100
    if total_records > 0
    else 0
)


# ============================================================
# PAGE SUMMARY
# ============================================================

st.header("📊 Attack Overview")

col1, col2, col3, col4 = st.columns(4)

with col1:

    st.metric(
        "Total Traffic",
        f"{total_records:,}"
    )

with col2:

    st.metric(
        "Total Attacks",
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
        f"{attack_rate:.2f}%"
    )


# ============================================================
# NO ATTACKS
# ============================================================

if attack_results.empty:

    st.success(
        "✅ No attacks were detected in the current dataset."
    )

    st.stop()


# ============================================================
# ATTACK TYPE COUNTS
# ============================================================

attack_counts = (
    attack_results["Predicted_Label"]
    .value_counts()
    .reset_index()
)

attack_counts.columns = [
    "Attack Type",
    "Count"
]

attack_counts["Percentage"] = (
    attack_counts["Count"]
    / attack_count
    * 100
).round(2)


# ============================================================
# TOP ATTACK
# ============================================================

top_attack = attack_counts.iloc[0]

st.info(
    f"""
    🎯 **Most frequently detected attack:** 
    **{top_attack['Attack Type']}**

    Detected instances: **{int(top_attack['Count']):,}**
    ({top_attack['Percentage']:.2f}% of all detected attacks)
    """
)


# ============================================================
# ATTACK TYPE DISTRIBUTION
# ============================================================

st.divider()

st.header("🎯 Attack Type Distribution")

fig_attack = px.bar(
    attack_counts,
    x="Count",
    y="Attack Type",
    orientation="h",
    text="Count",
    title="Detected Attack Types"
)

fig_attack.update_traces(
    textposition="outside"
)

fig_attack.update_layout(
    height=650,
    yaxis=dict(
        categoryorder="total ascending"
    )
)

st.plotly_chart(
    fig_attack,
    use_container_width=True
)


# ============================================================
# TWO-COLUMN ANALYSIS
# ============================================================

col1, col2 = st.columns(2)


# ============================================================
# ATTACK PERCENTAGE
# ============================================================

with col1:

    st.subheader("📈 Attack Composition")

    fig_composition = px.pie(
        attack_counts,
        names="Attack Type",
        values="Count",
        hole=0.4,
        title="Composition of Detected Attacks"
    )

    fig_composition.update_traces(
        textposition="inside",
        textinfo="percent"
    )

    st.plotly_chart(
        fig_composition,
        use_container_width=True
    )


# ============================================================
# CONFIDENCE DISTRIBUTION
# ============================================================

with col2:

    st.subheader("🎯 Prediction Confidence")

    fig_confidence = px.histogram(
        attack_results,
        x="Confidence (%)",
        nbins=20,
        title="Attack Prediction Confidence"
    )

    fig_confidence.update_layout(
        height=450
    )

    st.plotly_chart(
        fig_confidence,
        use_container_width=True
    )


# ============================================================
# RISK ANALYSIS
# ============================================================

st.divider()

st.header("⚠️ Attack Risk Analysis")


risk_attack_counts = (
    attack_results["Risk_Level"]
    .value_counts()
    .reindex(
        ["Low", "Medium", "High"],
        fill_value=0
    )
    .reset_index()
)

risk_attack_counts.columns = [
    "Risk Level",
    "Count"
]


col1, col2 = st.columns(2)


# ============================================================
# RISK BAR CHART
# ============================================================

with col1:

    fig_risk = px.bar(
        risk_attack_counts,
        x="Risk Level",
        y="Count",
        text="Count",
        title="Risk Level Among Attacks"
    )

    fig_risk.update_traces(
        textposition="outside"
    )

    st.plotly_chart(
        fig_risk,
        use_container_width=True
    )


# ============================================================
# RISK PIE CHART
# ============================================================

with col2:

    fig_risk_pie = px.pie(
        risk_attack_counts,
        names="Risk Level",
        values="Count",
        hole=0.4,
        title="Attack Risk Composition"
    )

    fig_risk_pie.update_traces(
        textposition="inside",
        textinfo="label+percent"
    )

    st.plotly_chart(
        fig_risk_pie,
        use_container_width=True
    )


# ============================================================
# ATTACK TYPE TABLE
# ============================================================

st.divider()

st.header("📋 Attack Statistics")

display_attack_counts = attack_counts.copy()

display_attack_counts["Count"] = (
    display_attack_counts["Count"]
    .astype(int)
)

display_attack_counts["Percentage"] = (
    display_attack_counts["Percentage"]
    .astype(str)
    + "%"
)

display_attack_counts = (
    display_attack_counts.rename(
        columns={
            "Count": "Detected Count"
        }
    )
)

st.dataframe(
    display_attack_counts,
    use_container_width=True,
    hide_index=True
)


# ============================================================
# ATTACK TYPE FILTER
# ============================================================

st.divider()

st.header("🔎 Attack Investigation")

attack_types = sorted(
    attack_results["Predicted_Label"]
    .unique()
)

selected_attack = st.selectbox(
    "Select an attack type to investigate",
    attack_types
)


selected_results = attack_results[
    attack_results["Predicted_Label"]
    == selected_attack
]


# ============================================================
# SELECTED ATTACK METRICS
# ============================================================

selected_count = len(
    selected_results
)

selected_percentage = (
    selected_count / attack_count * 100
)


col1, col2, col3 = st.columns(3)

with col1:

    st.metric(
        "Detected Instances",
        f"{selected_count:,}"
    )

with col2:

    st.metric(
        "Percentage of Attacks",
        f"{selected_percentage:.2f}%"
    )

with col3:

    average_confidence = (
        selected_results["Confidence (%)"]
        .mean()
    )

    st.metric(
        "Average Confidence",
        f"{average_confidence:.2f}%"
    )


# ============================================================
# SELECTED ATTACK RISK DISTRIBUTION
# ============================================================

selected_risk = (
    selected_results["Risk_Level"]
    .value_counts()
    .reindex(
        ["Low", "Medium", "High"],
        fill_value=0
    )
    .reset_index()
)

selected_risk.columns = [
    "Risk Level",
    "Count"
]


fig_selected_risk = px.bar(
    selected_risk,
    x="Risk Level",
    y="Count",
    text="Count",
    title=f"Risk Distribution — {selected_attack}"
)

fig_selected_risk.update_traces(
    textposition="outside"
)

st.plotly_chart(
    fig_selected_risk,
    use_container_width=True
)


# ============================================================
# SELECTED ATTACK RECORDS
# ============================================================

with st.expander(
    f"🔎 View {selected_attack} Records"
):

    st.dataframe(
        selected_results.head(500),
        use_container_width=True,
        height=450
    )

    st.caption(
        "Showing the first 500 records for performance."
    )


# ============================================================
# DOWNLOAD ATTACK RESULTS
# ============================================================

st.divider()

st.subheader("⬇️ Export Attack Analysis")

attack_csv = attack_results.to_csv(
    index=False
).encode("utf-8")

st.download_button(
    label="Download Attack Records",
    data=attack_csv,
    file_name="detected_attacks.csv",
    mime="text/csv",
    use_container_width=True
)


# ============================================================
# FOOTER
# ============================================================

st.divider()

st.caption(
    "Machine Learning Based Network Intrusion Detection "
    "System for Securing E-Voting Systems"
)