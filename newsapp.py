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
    resp = requests.get(RSS_URL)
    soup = BeautifulSoup(resp.text, "xml")
    items = soup.find_all("item")[:15]
    results = []
    for it in items:
        title = it.find("title").text
        link = it.find("link").text
        pub = it.find("pubDate").text
        desc_html = it.find("description").text
        desc = html2text.html2text(desc_html).strip().replace('\n', ' ')
        results.append({"title": title, "link": link, "time": pub, "summary": desc})
    return results

# ========== Ambil Data ==========
articles = scrape_cnbc_rss()

# ========== Search Filter ==========
search_query = st.text_input("🔍 Cari Berita (contoh: saham, IHSG, emiten)", "").lower()

if articles:
    filtered_articles = [a for a in articles if search_query in a['title'].lower() or search_query in a['summary'].lower()]

    if filtered_articles:
        cols = st.columns(3)

        for idx, art in enumerate(filtered_articles):
            with cols[idx % 3]:
                st.markdown('<div class="card">', unsafe_allow_html=True)
                st.markdown(f"<div class='title'>📊 {art['title']}</div>", unsafe_allow_html=True)
                st.markdown(f"<div class='time'>🕒 {art['time']}</div>", unsafe_allow_html=True)
                st.write(f"[🔗 Baca Selengkapnya]({art['link']})")
                st.markdown(f"<div class='summary'>{art['summary'][:200]}...</div>", unsafe_allow_html=True)
                st.markdown('</div>', unsafe_allow_html=True)
    else:
        st.warning("❗ Berita dengan kata kunci tersebut tidak ditemukan.")
else:
    st.write("⛔ Tidak ada berita terbaru saat ini.")
