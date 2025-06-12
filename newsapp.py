import streamlit as st
import requests
from bs4 import BeautifulSoup
import pandas as pd

st.set_page_config(page_title="Dashboard Berita Detikcom", layout="wide")

st.title("📰 Dashboard Berita Jawa Barat dari Detikcom")
st.subheader("Topik: Pertanian, Manufaktur, Perdagangan")

# ========== Fungsi Scraping Detikcom ==========
def scrape_detik(keyword):
    url = f"https://www.detik.com/search/searchall?query={keyword}+Jawa+Barat&siteid=2"
    headers = {'User-Agent': 'Mozilla/5.0'}
    response = requests.get(url, headers=headers)

    soup = BeautifulSoup(response.text, 'lxml')
    articles = soup.find_all('article')

    results = []
    for article in articles[:5]:  # Ambil 5 berita teratas
        title = article.find('h2').get_text(strip=True)
        link = article.find('a')['href']
        time = article.find('span', class_='date').get_text(strip=True) if article.find('span', class_='date') else '-'
        results.append({'title': title, 'link': link, 'time': time})
    
    return results

# ========== Tampilan Dashboard ==========
topics = ['pertanian', 'manufaktur', 'perdagangan']

for topic in topics:
    st.header(f'🗞️ Berita {topic.capitalize()}')
    articles = scrape_detik(topic)

    if articles:
        for article in articles:
            st.write(f"### {article['title']}")
            st.write(f"[Baca Selengkapnya]({article['link']})")
            st.write(f"*{article['time']}*")
            st.write("---")
    else:
        st.write("Tidak ada berita terbaru untuk topik ini.")
