import pandas as pd
import streamlit as st
import plotly.express as px

# 🔧 Configurações da página
st.set_page_config(page_title="Coleta Centro", page_icon="🚛", layout="wide")

# 🎨 Estilo personalizado 100% preto com textos brancos
st.markdown("""
    <style>
        * {
            color: white !important;
        }
        html, body, [class*="css"] {
            background-color: #000000 !important;
        }
        .stApp {
            background-color: #000000 !important;
        }
        .stSelectbox div, .stSelectbox label, .stSelectbox span {
            background-color: #111111 !important;
            color: white !important;
        }
        .stMetric {
            background: rgba(255, 255, 255, 0.05);
            border: 1px solid rgba(0, 255, 255, 0.3);
            border-radius: 12px;
            padding: 10px;
        }
    </style>
""", unsafe_allow_html=
