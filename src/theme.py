import streamlit as st


def apply_cybersecurity_theme():

    st.markdown(
        """
        <style>

        /* =====================================================
           MAIN APPLICATION BACKGROUND
        ===================================================== */

        .stApp {
            background-color: #0B1120 !important;
            color: #F8FAFC !important;
        }


        /* =====================================================
           MAIN CONTENT
        ===================================================== */

        .main .block-container {
            padding-top: 2rem;
            padding-bottom: 2rem;
            max-width: 1400px;
        }


        /* =====================================================
           SIDEBAR
        ===================================================== */

        section[data-testid="stSidebar"] {
            background-color: #080D18 !important;
            border-right: 1px solid #1E293B !important;
        }

        section[data-testid="stSidebar"] * {
            color: #F8FAFC !important;
        }


        /* =====================================================
           HEADINGS
        ===================================================== */

        h1,
        h2,
        h3,
        h4,
        h5,
        h6 {
            color: #F8FAFC !important;
            font-weight: 700 !important;
        }


        /* =====================================================
           NORMAL TEXT
        ===================================================== */

        p,
        label {
            color: #CBD5E1 !important;
        }


        /* =====================================================
           METRIC CARDS
        ===================================================== */

        div[data-testid="stMetric"] {
            background-color: #111827 !important;
            border: 1px solid #334155 !important;
            border-radius: 12px !important;
            padding: 15px !important;
        }

        div[data-testid="stMetricLabel"] {
            color: #94A3B8 !important;
            font-weight: 600 !important;
        }

        div[data-testid="stMetricValue"] {
            color: #00E5FF !important;
            font-weight: 700 !important;
        }


        /* =====================================================
           TEXT INPUTS
        ===================================================== */

        div[data-baseweb="input"] {
            background-color: #1E293B !important;
            border: 1px solid #334155 !important;
            border-radius: 8px !important;
        }

        div[data-baseweb="input"]:focus-within {
            border-color: #00E5FF !important;
            box-shadow: 0 0 0 1px #00E5FF !important;
        }

        input {
            background-color: transparent !important;
            color: #F8FAFC !important;
            font-weight: 600 !important;
        }

        input::placeholder {
            color: #64748B !important;
        }


        /* =====================================================
           SELECTBOX
        ===================================================== */

        div[data-baseweb="select"] > div {
            background-color: #1E293B !important;
            border: 1px solid #334155 !important;
            color: #F8FAFC !important;
        }

        div[data-baseweb="select"] span {
            color: #F8FAFC !important;
        }


        /* =====================================================
           MAIN BUTTONS
        ===================================================== */

        .stButton > button {
            width: 100% !important;

            background-color: #00E5FF !important;

            color: #07111F !important;

            border: 1px solid #00E5FF !important;

            border-radius: 8px !important;

            min-height: 44px !important;

            font-size: 16px !important;

            font-weight: 700 !important;

            transition:
                background-color 0.2s ease,
                border-color 0.2s ease,
                box-shadow 0.2s ease !important;
        }


        /* ACTUAL BUTTON TEXT */

        .stButton > button p,
        .stButton > button span,
        .stButton > button div {
            color: #07111F !important;

            font-weight: 700 !important;

            font-size: 16px !important;
        }


        /* BUTTON HOVER */

        .stButton > button:hover {
            background-color: #67E8F9 !important;

            border-color: #67E8F9 !important;

            color: #020617 !important;

            box-shadow:
                0 0 12px rgba(0, 229, 255, 0.45) !important;
        }


        .stButton > button:hover p,
        .stButton > button:hover span,
        .stButton > button:hover div {
            color: #020617 !important;

            font-weight: 700 !important;
        }


        /* BUTTON FOCUS */

        .stButton > button:focus {
            background-color: #00E5FF !important;

            border-color: #00E5FF !important;

            color: #07111F !important;

            box-shadow:
                0 0 0 2px rgba(0, 229, 255, 0.25) !important;
        }


        /* =====================================================
           DOWNLOAD BUTTON
        ===================================================== */

        .stDownloadButton > button {
            width: 100% !important;

            background-color: #00E5FF !important;

            color: #07111F !important;

            border: 1px solid #00E5FF !important;

            border-radius: 8px !important;

            min-height: 44px !important;

            font-size: 16px !important;

            font-weight: 700 !important;
        }


        .stDownloadButton > button p,
        .stDownloadButton > button span,
        .stDownloadButton > button div {
            color: #07111F !important;

            font-weight: 700 !important;

            font-size: 16px !important;
        }


        .stDownloadButton > button:hover {
            background-color: #67E8F9 !important;

            border-color: #67E8F9 !important;

            color: #020617 !important;

            box-shadow:
                0 0 12px rgba(0, 229, 255, 0.45) !important;
        }


        /* =====================================================
           NUMBER INPUT
        ===================================================== */

        div[data-testid="stNumberInput"] {
            color: #F8FAFC !important;
        }


        div[data-testid="stNumberInput"] input {
            background-color: #111827 !important;

            color: #F8FAFC !important;

            border: 1px solid #475569 !important;

            font-weight: 600 !important;

            font-size: 16px !important;
        }


        div[data-testid="stNumberInput"] input:focus {
            border-color: #00E5FF !important;

            box-shadow:
                0 0 0 1px #00E5FF !important;
        }


        /* PLUS / MINUS BUTTONS */

        div[data-testid="stNumberInput"] button {
            background-color: #1E293B !important;

            color: #00E5FF !important;

            border: none !important;
        }


        /* PLUS / MINUS ICONS */

        div[data-testid="stNumberInput"] button svg {
            color: #00E5FF !important;

            fill: #00E5FF !important;

            stroke: #00E5FF !important;
        }


        div[data-testid="stNumberInput"] button:hover {
            background-color: #334155 !important;

            color: #67E8F9 !important;
        }


        div[data-testid="stNumberInput"] button:hover svg {
            color: #67E8F9 !important;

            fill: #67E8F9 !important;

            stroke: #67E8F9 !important;
        }


        /* =====================================================
           FILE UPLOADER
        ===================================================== */

        section[data-testid="stFileUploaderDropzone"] {
            background-color: #111827 !important;

            border: 1px dashed #475569 !important;

            border-radius: 10px !important;
        }


        section[data-testid="stFileUploaderDropzone"]:hover {
            border-color: #00E5FF !important;
        }


        /* FILE UPLOADER TEXT */

        section[data-testid="stFileUploaderDropzone"] p,
        section[data-testid="stFileUploaderDropzone span"] {
            color: #CBD5E1 !important;
        }


        /* =====================================================
           BROWSE FILES BUTTON
        ===================================================== */

        section[data-testid="stFileUploaderDropzone"] button {
            background-color: #00E5FF !important;

            color: #07111F !important;

            border: 1px solid #00E5FF !important;

            border-radius: 8px !important;

            font-weight: 700 !important;

            min-height: 40px !important;
        }


        section[data-testid="stFileUploaderDropzone"] button p,
        section[data-testid="stFileUploaderDropzone"] button span,
        section[data-testid="stFileUploaderDropzone"] button div {
            color: #07111F !important;

            font-weight: 700 !important;
        }


        section[data-testid="stFileUploaderDropzone"] button:hover {
            background-color: #67E8F9 !important;

            border-color: #67E8F9 !important;

            box-shadow:
                0 0 10px rgba(0, 229, 255, 0.45) !important;
        }


        /* =====================================================
           DATAFRAME
        ===================================================== */

        div[data-testid="stDataFrame"] {
            border: 1px solid #334155 !important;

            border-radius: 10px !important;

            overflow: hidden;
        }


        /* =====================================================
           ALERT / INFO BOXES
        ===================================================== */

        div[data-testid="stAlert"] {
            border-radius: 10px !important;
        }


        /* =====================================================
           DIVIDERS
        ===================================================== */

        hr {
            border-color: #1E293B !important;
        }


        /* =====================================================
           SCROLLBAR
        ===================================================== */

        ::-webkit-scrollbar {
            width: 8px;
            height: 8px;
        }

        ::-webkit-scrollbar-track {
            background: #0B1120;
        }

        ::-webkit-scrollbar-thumb {
            background: #334155;

            border-radius: 10px;
        }

        ::-webkit-scrollbar-thumb:hover {
            background: #00E5FF;
        }


        /* =====================================================
           LINKS
        ===================================================== */

        a {
            color: #00E5FF !important;
        }


        /* =====================================================
           CHECKBOXES
        ===================================================== */

        div[data-testid="stCheckbox"] label {
            color: #CBD5E1 !important;

            font-weight: 600 !important;
        }


        /* =====================================================
           RADIO BUTTONS
        ===================================================== */

        div[data-testid="stRadio"] label {
            color: #CBD5E1 !important;

            font-weight: 600 !important;
        }
          /* =====================================================
           CYBERSECURITY DASHBOARD CARDS
        ===================================================== */
        
        div[data-testid="stMetric"] {
            background: linear-gradient(
                145deg,
                #111827,
                #0F172A
            ) !important;
        
            border: 1px solid #334155 !important;
        
            border-radius: 14px !important;
        
            padding: 20px !important;
        
            min-height: 120px !important;
        
            box-shadow:
                0 4px 12px rgba(0, 0, 0, 0.35) !important;
        
            transition:
                transform 0.2s ease,
                border-color 0.2s ease,
                box-shadow 0.2s ease !important;
        }
        
        
        /* =====================================================
           CARD HOVER EFFECT
        ===================================================== */
        
        div[data-testid="stMetric"]:hover {
            transform: translateY(-3px) !important;
        
            border-color: #00E5FF !important;
        
            box-shadow:
                0 0 18px rgba(0, 229, 255, 0.18) !important;
        }
        
        
        /* =====================================================
           CARD LABEL
        ===================================================== */
        
        div[data-testid="stMetricLabel"] {
            color: #94A3B8 !important;
        
            font-size: 14px !important;
        
            font-weight: 700 !important;
        
            letter-spacing: 0.3px !important;
        }
        
        
        /* =====================================================
           CARD VALUE
        ===================================================== */
        
        div[data-testid="stMetricValue"] {
            color: #F8FAFC !important;
        
            font-size: 30px !important;
        
            font-weight: 800 !important;
        
            letter-spacing: 0.5px !important;
        }
        
        
        /* =====================================================
           METRIC DELTA
        ===================================================== */
        
        div[data-testid="stMetricDelta"] {
            font-weight: 700 !important;
        }
        
        
        /* =====================================================
           METRIC CARD CONTAINER
        ===================================================== */
        
        div[data-testid="stMetric"] > div {
            gap: 8px !important;
        }

        </style>
        """,
        unsafe_allow_html=True
    )