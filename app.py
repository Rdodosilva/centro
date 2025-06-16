import pandas as pd
import streamlit as st
import plotly.express as px

# Configuração da página
st.set_page_config(page_title="Dashboard Coleta Centro", page_icon="🚛", layout="wide")

# CSS moderno — dark premium + glass effect
st.markdown("""
    <style>
    html, body, [class*="css"] {
        background-color: #0F0F0F;
        color: white;
        font-family: 'Segoe UI', sans-serif;
    }

    .stApp {
        background-color: #0F0F0F;
    }

    h1, h2, h3, h4, h5, h6 {
        color: white;
    }

    .stMetric {
        background: rgba(255, 255, 255, 0.05);
        border: 1px solid rgba(0, 255, 255, 0.4);
        borde
