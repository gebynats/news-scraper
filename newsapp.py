import streamlit as st
import requests
from bs4 import BeautifulSoup

st.set_page_config(page_title="Dashboard Berita Detikcom", layout="wide")

st.title("📰 Dashboard Berita Saham")
st.subheader("Topik: Saham")

# ========== Fungsi Scraping Daftar Berita ==========
def scrape_detik(keyword):
    url = f"https://www.detik.com/search/searchall?query={keyword}+Jawa+Barat&siteid=2"
    headers = {'User-Agent': 'Mozilla/5.0'}
    response = requests.get(url, headers=headers)

    soup = BeautifulSoup(response.text, 'html.parser')  # ganti parser agar aman

    articles = soup.find_all('article')

    results = []
    for article in articles[:5]:  # Ambil 5 berita teratas
        title = article.find('h2').get_text(strip=True)
        link = article.find('a')['href']
        time = article.find('span', class_='date').get_text(strip=True) if article.find('span', class_='date') else '-'
        results.append({'title': title, 'link': link, 'time': time})
    
    return results

# ========== Fungsi Ambil Isi Berita ==========
def scrape_summary(link):
    headers = {'User-Agent': 'Mozilla/5.0'}
    response = requests.get(link, headers=headers)
    soup = BeautifulSoup(response.text, 'html.parser')

    # Biasanya isi berita di Detik ada di div class 'detail__body-text'
    paragraphs = soup.find_all('p')
    content = ''
    for p in paragraphs[:3]:  # Ambil 3 paragraf pertama untuk summary
        content += p.get_text(strip=True) + ' '

    return content

# ========== Tampilan Dashboard ==========
topics = ['saham']

for topic in topics:
    st.header(f'🗞️ Berita {topic.capitalize()}')
    articles = scrape_detik(topic)

    if articles:
        for article in articles:
            st.write(f"### {article['title']}")
            st.write(f"*{article['time']}*")
            st.write(f"[Baca Selengkapnya]({article['link']})")

            # Ambil ringkasan berita
            with st.spinner('Mengambil ringkasan...'):
                summary = scrape_summary(article['link'])
                if summary:
                    st.write(summary)
                else:
                    st.write("Ringkasan tidak tersedia.")

            st.write("---")
    else:
        st.write("Tidak ada berita terbaru untuk topik ini.")
