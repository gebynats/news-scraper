import streamlit as st
import requests
from bs4 import BeautifulSoup
import html2text

# ========== Konfigurasi Halaman ==========
st.set_page_config(page_title="Dashboard Berita CNBC Indonesia", layout="wide")

# ========== Custom CSS ==========
st.markdown("""
    <style>
        .stApp {
            background: #ffffff;
        }
        .card {
            background: #f9f9f9;
            padding: 20px;
            border-radius: 15px;
            box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
            margin-bottom: 20px;
            min-height: 250px;
        }
        .title {
            font-size: 18px;
            font-weight: bold;
            color: #000000;
        }
        .summary {
            font-size: 14px;
            color: #333333;
        }
        .time {
            font-size: 12px;
            color: #555555;
        }
        a {
            color: #0d6efd;
            text-decoration: none;
            font-weight: bold;
        }
    </style>
""", unsafe_allow_html=True)

# ========== Judul ==========
st.title("📈 Dashboard Berita CNBC Indonesia")
st.subheader("💼 Berita Pasar Modal dan Saham Jawa Barat")

# ========== Fungsi Scrape RSS ==========
def scrape_cnbc_rss():
    RSS_URL = "https://www.cnbcindonesia.com/market/rss"
    resp = requests.get(RSS_URL_
