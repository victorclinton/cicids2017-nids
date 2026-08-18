import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from src.theme import apply_cybersecurity_theme
apply_cybersecurity_theme()
# ============================================================
# PAGE CONFIGURATION
# ============================================================

st.set_page_config(
    page_title="Threat Dashboard",
    page_icon="📊",
    layout="wide"
)


# ============================================================
# PAGE TITLE
# ============================================================

st.title("📊 Threat Detection Dashboard")

st.markdown(
    """
    Monitor the security status of network traffic analyzed by
    the machine learning intrusion detection system.
    """
)

st.divider()


# ============================================================
# AUTO-REFRESHING DASHBOARD
# ============================================================

@st.fragment(run_every=2)
def live_dashboard():

    # ========================================================
    # GET PREDICTION RESULTS
    # ========================================================

    if "batch_results" in st.session_state:

        results = st.session_state["batch_results"]

        realtime_active = True

    elif "realtime_results" in st.session_state:

        results = st.session_state["realtime_results"]

        realtime_active = True

    else:

        st.warning(
            "⚠️ No prediction results are available yet."
        )

        st.info(
            "Go to Batch Prediction or Real-Time Monitor "
            "and run detection first."
        )

        return


    # ========================================================
    # REAL-TIME STATUS
    # ========================================================

    if realtime_active:

        st.success(
            "🟢 LIVE — Real-Time Monitoring Results Active"
        )

    else:

        st.info(
            "📦 Batch Prediction Results"
        )


    # ========================================================
    # BASIC VALIDATION
    # ========================================================

    required_columns = [
        "Predicted_Label",
        "Confidence (%)",
        "Is_Attack",
        "Risk_Level"
    ]


    missing_columns = [
        col
        for col in required_columns
        if col not in results.columns
    ]


    if missing_columns:

        st.error(
            "❌ Prediction results are missing these columns: "
            f"{missing_columns}"
        )

        return


    # ========================================================
    # CLEAN RESULTS
    # ========================================================

    results = results.copy()


    results["Confidence (%)"] = pd.to_numeric(
        results["Confidence (%)"],
        errors="coerce"
    )


    results["Is_Attack"] = (
        results["Is_Attack"].astype(bool)
    )


    results["Risk_Level"] = (
        results["Risk_Level"]
        .astype(str)
        .str.strip()
    )


    # ========================================================
    # CALCULATE SUMMARY
    # ========================================================

    total_flows = len(results)


    attack_count = int(
        results["Is_Attack"].sum()
    )


    benign_count = (
        total_flows - attack_count
    )


    attack_rate = (
        attack_count / total_flows * 100
        if total_flows > 0
        else 0
    )


    # ========================================================
    # SECURITY STATUS
    # ========================================================

    st.subheader("🛡️ Security Status")


    if attack_count == 0:

        st.success(
            "🟢 NO THREATS DETECTED — "
            "No malicious network traffic was identified."
        )


    elif attack_rate < 5:

        st.warning(
            f"🟡 LOW THREAT LEVEL — "
            f"{attack_count:,} potentially malicious flows detected."
        )


    elif attack_rate < 20:

        st.warning(
            f"🟠 ELEVATED THREAT LEVEL — "
            f"{attack_count:,} potentially malicious flows detected."
        )


    else:

        st.error(
            f"🔴 HIGH THREAT LEVEL — "
            f"{attack_count:,} potentially malicious flows detected."
        )


    st.divider()


    # ========================================================
    # SUMMARY METRICS
    # ========================================================

    st.subheader("Detection Summary")


    col1, col2, col3, col4 = st.columns(4)


    with col1:

        st.metric(
            "🌐 Total Flows",
            f"{total_flows:,}"
        )


    with col2:

        st.metric(
            "🚨 Attacks Detected",
            f"{attack_count:,}"
        )


    with col3:

        st.metric(
            "✅ Benign Traffic",
            f"{benign_count:,}"
        )


    with col4:

        st.metric(
            "📈 Attack Rate",
            f"{attack_rate:.2f}%"
        )


    st.divider()


    # ========================================================
    # TRAFFIC CLASSIFICATION
    # ========================================================

    st.subheader("Traffic Classification")


    col1, col2 = st.columns(2)


    # --------------------------------------------------------
    # BENIGN VS ATTACK
    # --------------------------------------------------------

    with col1:

        traffic_counts = pd.Series(
            {
                "Benign": benign_count,
                "Attack": attack_count
            }
        )


        fig, ax = plt.subplots(
            figsize=(6, 4)
        )


        traffic_counts.plot(
            kind="bar",
            ax=ax
        )


        ax.set_xlabel("")

        ax.set_ylabel(
            "Number of Flows"
        )

        ax.set_title(
            "Benign vs Attack Traffic"
        )


        plt.xticks(
            rotation=0
        )

        plt.tight_layout()


        st.pyplot(
            fig,
            use_container_width=True
        )


        plt.close(fig)


    # --------------------------------------------------------
    # RISK DISTRIBUTION
    # --------------------------------------------------------

    with col2:

        risk_counts = (
            results["Risk_Level"]
            .value_counts()
            .reindex(
                ["High", "Medium", "Low"],
                fill_value=0
            )
        )


        fig, ax = plt.subplots(
            figsize=(6, 4)
        )


        risk_counts.plot(
            kind="bar",
            ax=ax
        )


        ax.set_xlabel("")

        ax.set_ylabel(
            "Number of Flows"
        )

        ax.set_title(
            "Risk Level Distribution"
        )


        plt.xticks(
            rotation=0
        )

        plt.tight_layout()


        st.pyplot(
            fig,
            use_container_width=True
        )


        plt.close(fig)


    st.divider()


    # ========================================================
    # TOP DETECTED ATTACKS
    # ========================================================

    st.subheader(
        "🚨 Top Detected Attack Types"
    )


    attack_results = results[
        results["Is_Attack"] == True
    ]


    if not attack_results.empty:

        attack_types = (
            attack_results[
                "Predicted_Label"
            ]
            .value_counts()
            .head(10)
        )


        fig, ax = plt.subplots(
            figsize=(10, 5)
        )


        attack_types.sort_values().plot(
            kind="barh",
            ax=ax
        )


        ax.set_xlabel(
            "Number of Flows"
        )

        ax.set_ylabel(
            "Attack Type"
        )

        ax.set_title(
            "Top 10 Detected Attack Types"
        )


        plt.tight_layout()


        st.pyplot(
            fig,
            use_container_width=True
        )


        plt.close(fig)


    else:

        st.success(
            "✅ No attacks were detected."
        )


    st.divider()


    # ========================================================
    # HIGH-RISK TRAFFIC
    # ========================================================

    st.subheader(
        "🚨 High-Risk Traffic"
    )


    high_risk = results[
        results["Risk_Level"] == "High"
    ].copy()


    if not high_risk.empty:

        high_risk = high_risk.sort_values(
            "Confidence (%)",
            ascending=False
        )


        display_columns = [
            "Predicted_Label",
            "Confidence (%)",
            "Is_Attack",
            "Risk_Level"
        ]


        st.dataframe(
            high_risk[
                display_columns
            ].head(100),
            use_container_width=True,
            hide_index=True
        )


        st.caption(
            f"Showing the top 100 of "
            f"{len(high_risk):,} "
            f"high-risk predictions."
        )


    else:

        st.success(
            "✅ No high-risk traffic detected."
        )


    st.divider()


    # ========================================================
    # THREAT SUMMARY
    # ========================================================

    st.subheader(
        "📋 Threat Summary"
    )


    if not attack_results.empty:

        summary = (
            attack_results[
                "Predicted_Label"
            ]
            .value_counts()
            .reset_index()
        )


        summary.columns = [
            "Attack Type",
            "Count"
        ]


        summary["Percentage of Attacks"] = (
            summary["Count"]
            / attack_count
            * 100
        ).round(2)


        st.dataframe(
            summary,
            use_container_width=True,
            hide_index=True
        )


    else:

        st.info(
            "No attack summary is available because "
            "no attacks were detected."
        )


    st.divider()


    # ========================================================
    # DOWNLOAD RESULTS
    # ========================================================

    st.subheader(
        "📥 Export Detection Results"
    )


    csv_data = (
        results
        .to_csv(index=False)
        .encode("utf-8")
    )


    st.download_button(
        label="📥 Download Detection Results",
        data=csv_data,
        file_name="network_intrusion_predictions.csv",
        mime="text/csv",
        use_container_width=True
    )


# ============================================================
# RUN LIVE DASHBOARD
# ============================================================

live_dashboard()


# ============================================================
# FOOTER
# ============================================================

st.divider()

st.caption(
    "Network Intrusion Detection System — "
    "Threat Monitoring Dashboard"
)