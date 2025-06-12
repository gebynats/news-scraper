import streamlit as st
import requests
from bs4 import BeautifulSoup

# ✅ Ini HARUS baris pertama
st.set_page_config(page_title="Dashboard Berita CNBC Indonesia", layout="wide")

# ========== Custom CSS for Background & Card ==========
def load_custom_css():
    st.markdown("""
        <style>
            body {
                background: linear-gradient(to right, #e0f7fa, #80deea);
            }
            .stApp {
                background: linear-gradient(to right, #e0f7fa, #80deea);
            }
            .card {
                background-color: white;
                padding: 20px;
                border-radius: 15px;
                box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
                margin-bottom: 20px;
            }
        </style>
        """, unsafe_allow_html=True)

load_custom_css()

st.title("📈 Dashboard Berita CNBC Indonesia")
st.subheader("Topik: Saham & Pasar Modal di Jawa Barat")

# ========== Fungsi Scraping CNBC ==========
def scrape_cnbc():
    url = 'https://www.cnbcindonesia.com/market'
    headers = {'User-Agent': 'Mozilla/5.0'}
    response = requests.get(url, headers=headers)

    soup = BeautifulSoup(response.text, 'html.parser')
    articles = soup.find_all('div', class_='list media_rows middle thumb')

    results = []
    for article in articles[:9]:  # Ambil 9 berita untuk 3 kolom
        try:
            title = article.find('h2').get_text(strip=True)
            link = article.find('a')['href']
            if not link.startswith('http'):
                link = 'https:' + link
            time = article.find('div', class_='date').get_text(strip=True)
            results.append({'title': title, 'link': link, 'time': time})
        except:
            continue
    return results

# ========== Fungsi Ambil Isi Berita ==========
def scrape_summary(link):
    headers = {'User-Agent': 'Mozilla/5.0'}
    response = requests.get(link, headers=headers)
    soup = BeautifulSoup(response.text, 'html.parser')

    try:
        paragraphs = soup.find_all('div', class_='detail_text')[0].find_all('p')
        content = ''
        for p in paragraphs[:3]:  # Ambil 3 paragraf pertama
            content += p.get_text(strip=True) + ' '
        return content
    except:
        return ''

# ========== Tampilan Dashboard ==========
articles = scrape_cnbc()

if articles:
    cols = st.columns(3)

    for idx, article in enumerate(articles):
        with cols[idx % 3]:
            st.markdown('<div class="card">', unsafe_allow_html=True)
            st.markdown(f"### 📊 {article['title']}")
            st.write(f"*🕒 {article['time']}*")
            st.write(f"[🔗 Baca Selengkapnya]({article['link']})")

            with st.expander("📄 Ringkasan Berita"):
                with st.spinner('📥 Mengambil ringkasan...'):
                    summary = scrape_summary(article['link'])
                    if summary:
                        st.write(summary)
                    else:
                        st.write("Ringkasan tidak tersedia.")
            st.markdown('</div>', unsafe_allow_html=True)
else:
    st.write("Tidak ada berita terbaru saat ini.")
