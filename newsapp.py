import streamlit as st
import requests
import pandas as pd

st.set_page_config(page_title="Dashboard Berita Jawa Barat", layout="wide")

st.title("📊 Dashboard Berita Jawa Barat")
st.subheader("Topik: Pertanian, Manufaktur, Perdagangan")

# ======== Fungsi Ambil Berita ===========
def get_news(query):
    API_KEY = 'YOUR_NEWSAPI_KEY'  # Ganti dengan API Key kamu
    url = f'https://newsapi.org/v2/everything?q={query}&language=id&sortBy=publishedAt&apiKey={API_KEY}'
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()['articles']
    else:
        return []

# ======== Ambil Berita Per Topik ===========
topics = ['pertanian', 'manufaktur', 'perdagangan']

for topic in topics:
    st.header(f'🗞️ Berita {topic.capitalize()}')
    query = f"Jawa Barat {topic}"
    articles = get_news(query)

    if articles:
        for article in articles[:5]:  # Batasi 5 berita per topik
            st.write(f"### {article['title']}")
            st.write(article['description'])
            st.write(f"[Baca Selengkapnya]({article['url']})")
            st.write(f"*{article['publishedAt']}*")
            st.write("---")
    else:
        st.write("Tidak ada berita terbaru untuk topik ini.")
