import streamlit as st
import plotly.express as px

from src.theme import apply_cybersecurity_theme
apply_cybersecurity_theme()
st.set_page_config(
    page_title="ML-Based NIDS for E-Voting",
    page_icon="🛡️",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.title("🛡️ Machine Learning-Based Network Intrusion Detection System")

st.markdown("""
Welcome to the **Machine Learning-Based Network Intrusion Detection System (NIDS)** developed for securing E-Voting systems.

Use the navigation menu on the left to explore the application.
""")

st.info("Select a page from the sidebar to begin.")

