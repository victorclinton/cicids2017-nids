import streamlit as st
import pandas as pd
import time
from datetime import datetime

import plotly.graph_objects as go
from src.model_loader import load_artifacts
from src.inference import predict_dataframe
from src.theme import apply_cybersecurity_theme
apply_cybersecurity_theme()
# ============================================================
# PAGE CONFIGURATION
# ============================================================

st.set_page_config(
    page_title="Real-Time Monitor",
    page_icon="🟢",
    layout="wide"
)


# ============================================================
# LOAD MODEL ARTIFACTS
# ============================================================

@st.cache_resource
def load_model_artifacts():
    return load_artifacts()


try:

    model, scaler, label_encoder, feature_cols = (
        load_model_artifacts()
    )

except Exception as e:

    st.error("❌ Failed to load model artifacts.")
    st.exception(e)
    st.stop()


# ============================================================
# PAGE TITLE
# ============================================================

st.title("🟢 Real-Time Network Traffic Monitor")

st.write(
    "Simulate real-time network intrusion detection "
    "using the trained machine learning model."
)

st.divider()

st.success("✅ Model artifacts loaded successfully.")


# ============================================================
# UPLOAD TRAFFIC DATA
# ============================================================

st.subheader("📂 Traffic Data")

uploaded_file = st.file_uploader(
    "Upload CICIDS2017 traffic data",
    type=["csv", "xlsx"]
)


if uploaded_file is None:

    st.info(
        "Please upload a CSV or Excel file "
        "to begin monitoring."
    )

    st.stop()


# ============================================================
# READ DATASET
# ============================================================

try:

    if uploaded_file.name.lower().endswith(".csv"):

        df = pd.read_csv(
            uploaded_file,
            low_memory=False
        )

    else:

        df = pd.read_excel(uploaded_file)

except Exception as e:

    st.error(
        "❌ Unable to read the uploaded file."
    )

    st.exception(e)

    st.stop()


# ============================================================
# DISPLAY DATASET INFORMATION
# ============================================================

st.success(
    f"✅ File uploaded successfully: "
    f"{uploaded_file.name}"
)

st.write(
    f"Dataset shape: {df.shape[0]:,} rows × "
    f"{df.shape[1]:,} columns"
)

st.dataframe(
    df.head(10),
    width="stretch"
)

st.divider()


# ============================================================
# INITIALIZE ALERT HISTORY
# ============================================================

if "alert_history" not in st.session_state:

    st.session_state["alert_history"] = pd.DataFrame(
        columns=[
            "Alert_ID",
            "Alert_Time",
            "Predicted_Label",
            "Confidence (%)",
            "Risk_Level"
        ]
    )


# ============================================================
# INITIALIZE ALERT COUNTER
# ============================================================

if "alert_counter" not in st.session_state:

    st.session_state["alert_counter"] = 0


# ============================================================
# MONITORING CONTROLS
# ============================================================

st.subheader("⚙️ Monitoring Controls")

batch_size = st.number_input(
    "Number of records per update",
    min_value=10,
    max_value=1000,
    value=100,
    step=10
)


start_monitoring = st.button(
    "▶️ Start Monitoring",
    width="stretch"
)


# ============================================================
# START MONITORING
# ============================================================

if start_monitoring:

    # ========================================================
    # INITIALIZE MONITORING VARIABLES
    # ========================================================

    total_rows = len(df)

    processed_rows = 0

    total_attacks = 0

    total_benign = 0

    batch_number = 0

    all_results = []

    # History used by the time-series chart
    time_series_history = []

    # ========================================================
    # CREATE STREAMLIT PLACEHOLDERS
    # ========================================================

    status_placeholder = st.empty()

    progress_bar = st.progress(0)

    metrics_placeholder = st.empty()

    # Main chart
    time_series_placeholder = st.empty()

    # Heatmap
    heatmap_placeholder = st.empty()

    # Donut
    donut_placeholder = st.empty()

    # Recent alerts table
    alerts_placeholder = st.empty()

    # Full prediction table
    results_placeholder = st.empty()


    # ========================================================
    # MONITORING LOOP
    # ========================================================

    while processed_rows < total_rows:

        batch_number += 1


        # ====================================================
        # DETERMINE CURRENT BATCH
        # ====================================================

        start_row = processed_rows

        end_row = min(
            start_row + batch_size,
            total_rows
        )

        current_batch = df.iloc[
            start_row:end_row
        ].copy()


        # ====================================================
        # UPDATE MONITORING STATUS
        # ====================================================

        status_placeholder.info(
            f"🟢 Monitoring active — "
            f"Batch {batch_number} | "
            f"Processing records "
            f"{start_row + 1:,}–{end_row:,} "
            f"of {total_rows:,}"
        )


        # ====================================================
        # RUN MODEL PREDICTION
        # ====================================================

        try:

            batch_results = predict_dataframe(
                df=current_batch,
                model=model,
                scaler=scaler,
                label_encoder=label_encoder,
                feature_cols=feature_cols,
                log_features=None,
                verbose=False
            )

        except Exception as e:

            st.error(
                "❌ Prediction failed."
            )

            st.exception(e)

            break


        # ====================================================
        # CHECK PREDICTION LABEL
        # ====================================================

        if "Predicted_Label" not in batch_results.columns:

            st.error(
                "❌ Prediction results do not contain "
                "'Predicted_Label'."
            )

            st.write(
                "Available prediction columns:",
                list(batch_results.columns)
            )

            break


        # ====================================================
        # CREATE Is_Attack
        # ====================================================

        if "Is_Attack" not in batch_results.columns:

            batch_results["Is_Attack"] = (
                batch_results["Predicted_Label"]
                .astype(str)
                .str.strip()
                .str.upper()
                .ne("BENIGN")
            )


        # ====================================================
        # ADD ALERT TIME
        # ====================================================

        current_time = datetime.now()

        batch_results["Alert_Time"] = (
            current_time.strftime(
                "%Y-%m-%d %H:%M:%S"
            )
        )


        # ====================================================
        # GENERATE UNIQUE ALERT IDS
        # ====================================================

        number_of_predictions = len(
            batch_results
        )

        start_id = (
            st.session_state["alert_counter"]
            + 1
        )

        end_id = (
            st.session_state["alert_counter"]
            + number_of_predictions
        )

        alert_ids = [
            f"ALT-{i:06d}"
            for i in range(
                start_id,
                end_id + 1
            )
        ]

        batch_results["Alert_ID"] = alert_ids

        st.session_state[
            "alert_counter"
        ] = end_id


        # ====================================================
        # CREATE CONFIDENCE COLUMN
        # ====================================================

        if "Confidence (%)" not in batch_results.columns:

            batch_results[
                "Confidence (%)"
            ] = 0.0

        else:

            batch_results[
                "Confidence (%)"
            ] = pd.to_numeric(
                batch_results[
                    "Confidence (%)"
                ],
                errors="coerce"
            ).fillna(0)


        # ====================================================
        # CREATE RISK LEVEL
        # ====================================================

        if "Risk_Level" not in batch_results.columns:

            def calculate_risk(row):

                if not row["Is_Attack"]:

                    return "Low"

                confidence = float(
                    row["Confidence (%)"]
                )

                if confidence >= 80:

                    return "High"

                elif confidence >= 50:

                    return "Medium"

                else:

                    return "Low"


            batch_results["Risk_Level"] = (
                batch_results.apply(
                    calculate_risk,
                    axis=1
                )
            )


        # ====================================================
        # COUNT ATTACKS
        # ====================================================

        batch_attacks = int(
            batch_results[
                "Is_Attack"
            ].sum()
        )

        batch_benign = (
            len(batch_results)
            - batch_attacks
        )


        total_attacks += batch_attacks

        total_benign += batch_benign

        processed_rows = end_row


        # ====================================================
        # STORE BATCH RESULTS
        # ====================================================

        all_results.append(
            batch_results
        )


        # ====================================================
        # COMBINE ALL RESULTS
        # ====================================================

        live_results = pd.concat(
            all_results,
            ignore_index=True
        )


        st.session_state[
            "realtime_live_results"
        ] = live_results.copy()


        # ====================================================
        # SAVE ATTACKS TO ALERT HISTORY
        # ====================================================

        current_attacks = batch_results[
            batch_results["Is_Attack"] == True
        ].copy()


        if not current_attacks.empty:

            new_alerts = current_attacks[
                [
                    "Alert_ID",
                    "Alert_Time",
                    "Predicted_Label",
                    "Confidence (%)",
                    "Risk_Level"
                ]
            ].copy()

            st.session_state[
                "alert_history"
            ] = pd.concat(
                [
                    st.session_state[
                        "alert_history"
                    ],
                    new_alerts
                ],
                ignore_index=True
            )


        # ====================================================
        # UPDATE PROGRESS
        # ====================================================

        progress = (
            processed_rows / total_rows
            if total_rows > 0
            else 1
        )

        progress_bar.progress(
            min(progress, 1.0)
        )


        # ====================================================
        # CALCULATE ATTACK RATE
        # ====================================================

        attack_rate = (
            total_attacks
            / processed_rows
            * 100
            if processed_rows > 0
            else 0
        )


        # ====================================================
        # LIVE METRICS
        # ====================================================

        with metrics_placeholder.container():

            col1, col2, col3, col4 = (
                st.columns(4)
            )

            with col1:

                st.metric(
                    "Traffic Processed",
                    f"{processed_rows:,}"
                )

            with col2:

                st.metric(
                    "🚨 Attacks",
                    f"{total_attacks:,}"
                )

            with col3:

                st.metric(
                    "✅ Normal Traffic",
                    f"{total_benign:,}"
                )

            with col4:

                st.metric(
                    "Attack Rate",
                    f"{attack_rate:.2f}%"
                )


        # ====================================================
        # 1. TIME-SERIES TRAFFIC + ATTACK CHART
        # ====================================================

        # Add one observation for the current batch

        time_series_history.append(
            {
                "Time": current_time,
                "Traffic": len(batch_results),
                "Attacks": batch_attacks
            }
        )


        time_series_df = pd.DataFrame(
            time_series_history
        )


        fig_time = go.Figure()


        # ----------------------------------------------------
        # TOTAL TRAFFIC
        # ----------------------------------------------------

        fig_time.add_trace(
            go.Scatter(
            x=time_series_df["Time"],
            y=time_series_df["Traffic"],
            mode="lines+markers",
            name="Total Traffic",
            line=dict(
                color="blue",
                width=3
            ),
            marker=dict(
                color="blue",
                size=7
            ),
            fill="tozeroy"
            )   
        )

        # ----------------------------------------------------
        # ATTACK TRAFFIC
        # ----------------------------------------------------

        fig_time.add_trace(
            go.Scatter(
            x=time_series_df["Time"],
            y=time_series_df["Attacks"],
            mode="lines+markers",
            name="Attack Traffic",
            line=dict(
                color="red",
                width=3
            ),
            marker=dict(
                color="red",
                size=7
                )
            )
        )

        fig_time.update_layout(

            title="📈 Real-Time Traffic & Attack Activity",

            xaxis_title="Time",

            yaxis_title="Number of Network Flows",

            height=450,

            hovermode="x unified",

            legend=dict(
                orientation="h",
                yanchor="bottom",
                y=1.02,
                xanchor="left",
                x=0
            )
        )


        with time_series_placeholder.container():

            st.subheader(
                "📈 Traffic & Attack Activity Over Time"
            )

            st.caption(
                "The chart shows the number of network "
                "flows and detected attacks during each "
                "monitoring update."
            )

            st.plotly_chart(
                fig_time,
                width="stretch",
                key=f"time_series_{batch_number}"
            )


        # ====================================================
        # 2. ATTACK ACTIVITY HEATMAP
        # ====================================================

        heatmap_data = live_results.copy()

        heatmap_data["Time"] = (
            pd.to_datetime(
                heatmap_data["Alert_Time"]
            )
        )

        # Use the prediction labels as attack types

        attack_only = heatmap_data[
            heatmap_data["Is_Attack"] == True
        ].copy()


        if not attack_only.empty:

            attack_only["Time_Bin"] = (
                attack_only["Time"]
                .dt.strftime("%H:%M:%S")
            )


            heatmap_table = pd.crosstab(
                attack_only[
                    "Predicted_Label"
                ],
                attack_only[
                    "Time_Bin"
                ]
            )


            fig_heatmap = go.Figure(
                data=go.Heatmap(
                    z=heatmap_table.values,
                    x=heatmap_table.columns,
                    y=heatmap_table.index,
                    hoverongaps=False
                )
            )


            fig_heatmap.update_layout(

                title="🔥 Attack Activity Heatmap",

                xaxis_title="Time",

                yaxis_title="Attack Type",

                height=400
            )


            with heatmap_placeholder.container():

                st.plotly_chart(
                    fig_heatmap,
                    width="stretch",
                    key=f"heatmap_{batch_number}"
                )

        else:

            with heatmap_placeholder.container():

                st.info(
                    "🟢 No attack activity available "
                    "for the heatmap yet."
                )


        # ====================================================
        # 3. CURRENT CLASS DISTRIBUTION — DONUT
        # ====================================================

        class_distribution = (
            live_results[
                "Predicted_Label"
            ]
            .value_counts()
            .reset_index()
        )

        class_distribution.columns = [
            "Class",
            "Count"
        ]


        fig_donut = go.Figure(
            data=[
                go.Pie(
                    labels=class_distribution[
                        "Class"
                    ],
                    values=class_distribution[
                        "Count"
                    ],
                    hole=0.55
                )
            ]
        )


        fig_donut.update_layout(
            title="🥧 Current Traffic Classification",
            height=400
        )


        with donut_placeholder.container():

            st.plotly_chart(
                fig_donut,
                width="stretch",
                key=f"donut_{batch_number}"
            )


        # ====================================================
        # 4. RECENT FLAGGED RECORDS
        # ====================================================

        with alerts_placeholder.container():

            st.subheader(
                "🚨 Recent Security Alerts"
            )


            recent_alerts = (
                st.session_state[
                    "alert_history"
                ]
                .tail(20)
                .copy()
            )


            if not recent_alerts.empty:

                st.dataframe(
                    recent_alerts[
                        [
                            "Alert_ID",
                            "Alert_Time",
                            "Predicted_Label",
                            "Confidence (%)",
                            "Risk_Level"
                        ]
                    ],
                    width="stretch",
                    hide_index=True
                )

            else:

                st.success(
                    "🟢 No security alerts detected yet."
                )


        # ====================================================
        # FULL LIVE PREDICTION RESULTS
        # ====================================================

        with results_placeholder.container():

            st.subheader(
                "📊 Live Prediction Results"
            )

            st.dataframe(
                live_results.tail(100),
                width="stretch",
                hide_index=True
            )


        # ====================================================
        # SIMULATION DELAY
        # ====================================================

        time.sleep(1)


    # ========================================================
    # MONITORING COMPLETED
    # ========================================================

    if processed_rows >= total_rows:

        status_placeholder.success(
            f"✅ Monitoring completed. "
            f"Processed {total_rows:,} records."
        )

        progress_bar.progress(1.0)


        # ====================================================
        # SAVE FINAL RESULTS
        # ====================================================

        final_results = pd.concat(
            all_results,
            ignore_index=True
        )


        st.session_state[
            "realtime_results"
        ] = final_results.copy()


        # ====================================================
        # SAVE TO BATCH RESULTS
        # ====================================================

        st.session_state[
            "batch_results"
        ] = final_results.copy()


        st.success(
            "✅ Real-time monitoring results "
            "have been saved."
        )