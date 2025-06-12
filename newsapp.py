import streamlit as st
import requests
from bs4 import BeautifulSoup

st.set_page_config(page_title="Dashboard Berita Detikcom", layout="wide")

st.title("📰 Dashboard Berita Saham")
st.subheader("Topik: Saham di Jawa Barat")

# ========== Fungsi Scraping Daftar Berita ==========
def scrape_detik(keyword):
    url = f"https://www.detik.com/search/searchall?query={keyword}+Jawa+Barat&siteid=2"
    headers = {'User-Agent': 'Mozilla/5.0'}
    response = requests.get(url, headers=headers)

    soup = BeautifulSoup(response.text, 'html.parser')
    articles = soup.find_all('article')

    results = []
    for article in articles[:10]:  # Ambil 10 berita, nanti disaring
        try:
            title = article.find('h2').get_text(strip=True)
            link = article.find('a')['href']
            time = article.find('span', class_='date').get_text(strip=True) if article.find('span', class_='date') else '-'
            results.append({'title': title, 'link': link, 'time': time})
        except:
            continue  # Jika ada elemen yang hilang, skip
    return results

# ========== Fungsi Scrape Isi Berita ==========
def scrape_summary(link):
    headers = {'User-Agent': 'Mozilla/5.0'}
    response = requests.get(link, headers=headers)
    soup = BeautifulSoup(response.text, 'html.parser')

    paragraphs = soup.find_all('p')
    content = ''
    for p in paragraphs[:5]:  # Ambil 5 paragraf pertama
        content += p.get_text(strip=True) + ' '

    return content

# ========== Fungsi Filter Relevansi ==========
def is_relevant(content, keywords=['saham', 'emiten', 'bursa', 'IHSG', 'BEI']):
    for keyword in keywords:
        if keyword.lower() in content.lower():
            return True
    return False

# ========== Tampilan Dashboard ==========
topics = ['saham']

for topic in topics:
    st.header(f'🗞️ Berita {topic.capitalize()}')
    articles = scrape_detik(topic)

    if articles:
        for article in articles:
            # Ambil ringkasan berita
            with st.spinner('Mengambil dan memfilter berita...'):
                summary = scrape_summary(article['link'])
                
                # Cek apakah berita relevan
                if is_relevant(summary):
                    st.write(f"### {article['title']}")
                    st.write(f"*{article['time']}*")
                    st.write(f"[Baca Selengkapnya]({article['link']})")
                    st.write(summary)
                    st.write("---")
                else:
                    st.write(f"🔍 Berita '{article['title']}' tidak relevan, dilewati.")
    else:
        st.write("Tidak ada berita terbaru untuk topik ini.")
