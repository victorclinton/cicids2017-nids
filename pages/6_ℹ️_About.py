import streamlit as st
from src.theme import apply_cybersecurity_theme
apply_cybersecurity_theme()
# ============================================================
# PAGE CONFIGURATION
# ============================================================

st.set_page_config(
    page_title="About",
    page_icon="ℹ️",
    layout="wide"
)


# ============================================================
# PAGE TITLE
# ============================================================

st.title("ℹ️ About the Network Intrusion Detection System")

st.markdown(
    """
    ### Machine Learning-Based Network Intrusion Detection System

    This application is designed to analyze network traffic and
    identify potentially malicious activity using a trained
    machine learning classification model.
    """
)

st.divider()


# ============================================================
# SYSTEM OVERVIEW
# ============================================================

st.header("🛡️ System Overview")

st.markdown(
    """
    The Network Intrusion Detection System (NIDS) analyzes network
    flow records and classifies them as either **BENIGN** traffic
    or a specific type of network attack.

    The system uses a trained **Random Forest classifier** to
    perform multi-class intrusion detection.

    The application provides both prediction and analytical
    capabilities through an interactive Streamlit interface.
    """
)


# ============================================================
# OBJECTIVES
# ============================================================

st.header("🎯 System Objectives")

objectives = [
    "Detect malicious network traffic.",
    "Classify detected traffic into different attack categories.",
    "Provide confidence scores for model predictions.",
    "Assign qualitative risk levels to detected traffic.",
    "Provide visual analytics for detected threats.",
    "Allow users to explore and inspect network datasets.",
    "Provide downloadable prediction results."
]

for objective in objectives:
    st.markdown(f"• {objective}")


st.divider()


# ============================================================
# HOW THE SYSTEM WORKS
# ============================================================

st.header("⚙️ How the System Works")

st.markdown(
    """
    The system follows a machine learning inference pipeline:
    """
)

steps = [
    ("1️⃣", "Dataset Upload",
     "The user uploads a network traffic dataset in CSV or Excel format."),

    ("2️⃣", "Data Preprocessing",
     "The input data is cleaned and transformed into the feature representation expected by the trained model."),

    ("3️⃣", "Feature Alignment",
     "The input features are aligned with the 69 features used by the trained model."),

    ("4️⃣", "Feature Scaling",
     "The processed features are transformed using the fitted RobustScaler."),

    ("5️⃣", "Model Prediction",
     "The Random Forest model predicts the class of each network flow."),

    ("6️⃣", "Confidence Calculation",
     "Prediction probabilities are used to calculate the model confidence."),

    ("7️⃣", "Risk Assessment",
     "Predictions are assigned qualitative risk levels."),

    ("8️⃣", "Visualization",
     "The prediction results are presented through dashboards and analytical pages.")
]


for icon, title, description in steps:

    st.markdown(
        f"""
        ### {icon} {title}

        {description}
        """
    )


st.divider()


# ============================================================
# APPLICATION MODULES
# ============================================================

st.header("📊 Application Modules")

modules = {
    "📦 Batch Prediction":
        "Upload network traffic data and perform batch intrusion detection.",

    "📊 Threat Dashboard":
        "Provides a high-level overview of detected threats, attack rates, and risk levels.",

    "🚨 Attack Analysis":
        "Provides detailed analysis of the different attack types detected by the model.",

    "📈 Model Performance":
        "Displays the evaluation results of the trained Random Forest model.",

    "📚 Dataset Explorer":
        "Allows users to inspect uploaded datasets, including structure, statistics, missing values, and class distributions.",

    
}


for module, description in modules.items():

    with st.expander(module):

        st.write(description)


st.divider()


# ============================================================
# MACHINE LEARNING MODEL
# ============================================================

st.header("🤖 Machine Learning Model")

st.markdown(
    """
    ### Random Forest Classifier

    The primary intrusion detection model used by this application
    is a **Random Forest classifier**.

    Random Forest combines multiple decision trees to produce a
    final classification. This makes it suitable for complex
    classification problems involving many network traffic
    features.

    The trained model is loaded during inference together with
    the preprocessing artifacts required to transform new network
    traffic into the correct model input format.
    """
)


# ============================================================
# MODEL INPUT
# ============================================================

st.subheader("Model Input")

st.markdown(
    """
    The trained model expects **69 features**.

    Before prediction, incoming network traffic is processed so
    that its feature structure matches the feature representation
    used during model training.
    """
)


st.divider()


# ============================================================
# PREDICTION OUTPUT
# ============================================================

st.header("📋 Prediction Output")

st.markdown(
    """
    For each analyzed network flow, the system produces:

    - **Predicted Label** — the predicted traffic or attack type.
    - **Confidence (%)** — the highest prediction probability
      produced by the model.
    - **Is_Attack** — indicates whether the prediction represents
      malicious traffic.
    - **Risk_Level** — a qualitative assessment based on the
      prediction confidence.
    """
)


st.divider()


# ============================================================
# SUPPORTED ATTACK CLASSES
# ============================================================

st.header("🚨 Supported Attack Categories")

attack_classes = [
    "BENIGN",
    "Bot",
    "DDoS",
    "DoS GoldenEye",
    "DoS Hulk",
    "DoS Slowhttptest",
    "DoS slowloris",
    "FTP-Patator",
    "Heartbleed",
    "Infiltration",
    "PortScan",
    "SSH-Patator",
    "Web Attack_Brute Force",
    "Web Attack_Sql Injection",
    "Web Attack_XSS"
]


cols = st.columns(3)

for index, attack in enumerate(attack_classes):

    with cols[index % 3]:

        st.markdown(
            f"• **{attack}**"
        )


st.divider()


# ============================================================
# TECHNOLOGY STACK
# ============================================================

st.header("💻 Technology Stack")

tech_stack = {
    "Programming Language": "Python",
    "Machine Learning": "Scikit-learn",
    "Data Processing": "Pandas / NumPy",
    "Visualization": "Matplotlib",
    "Web Application": "Streamlit",
    "Model": "Random Forest Classifier",
    "Dataset": "CICIDS2017"
}


for technology, value in tech_stack.items():

    st.markdown(
        f"**{technology}:** {value}"
    )


st.divider()


# ============================================================
# USER WORKFLOW
# ============================================================

st.header("🚀 Recommended Workflow")

st.markdown(
    """
    For a typical analysis session:

    **1. Dataset Explorer**

    Upload and inspect your network traffic dataset.

    **2. Batch Prediction**

    Upload the dataset and run the trained model.

    **3. Threat Dashboard**

    Review the overall security status and detected threats.

    **4. Attack Analysis**

    Investigate individual attack categories in greater detail.

    **5. Model Performance**

    Review the performance of the trained Random Forest model.

    **6. Export Results**

    Download the prediction results for further analysis.
    """
)


st.divider()


# ============================================================
# DISCLAIMER
# ============================================================

st.header("⚠️ Important Note")

st.info(
    """
    This system is a machine learning-based intrusion detection
    tool. Its predictions should be interpreted as analytical
    assistance rather than an absolute determination of whether
    network activity is malicious.

    The quality of predictions depends on the quality and
    characteristics of the input data and the training process.
    """
)


st.divider()


# ============================================================
# FOOTER
# ============================================================

st.caption(
    "Machine Learning-Based Network Intrusion Detection System"
)