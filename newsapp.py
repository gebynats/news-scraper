import streamlit as st
import yfinance as yf
import pandas as pd
import time

st.set_page_config(page_title="IDX Sector Monitor", layout="wide")
st.title("📈 Real-Time IDX Sector Performance Monitor")

sectors = {
    'Banking': ['BBCA.JK', 'BBRI.JK', 'BMRI.JK', 'BBNI.JK'],
    'Consumer': ['ICBP.JK', 'UNVR.JK', 'MYOR.JK', 'KLBF.JK'],
    'Energy': ['PGAS.JK', 'PTBA.JK', 'ADRO.JK', 'ITMG.JK'],
    'Telco': ['TLKM.JK', 'EXCL.JK', 'ISAT.JK']
}

refresh_interval = st.number_input('Refresh Interval (seconds)', min_value=5, max_value=3600, value=60)

if st.button('Start Monitoring'):
    placeholder = st.empty()

    while True:
        sector_perf = {}

        for sector, tickers in sectors.items():
            gains = []
            for ticker in tickers:
                data = yf.Ticker(ticker).history(period='1d', interval='1m')
                if not data.empty:
                    open_price = data.iloc[0]['Open']
                    current_price = data['Close'].iloc[-1]
                    change_pct = ((current_price - open_price) / open_price) * 100
                    gains.append(change_pct)

            avg_gain = sum(gains) / len(gains) if gains else 0
            sector_perf[sector] = avg_gain

        sorted_sector = dict(sorted(sector_perf.items(), key=lambda x: x[1], reverse=True))
        top_sector = list(sorted_sector.keys())[0]

        st.subheader(f"🔥 Best Performing Sector: {top_sector} ({sorted_sector[top_sector]:.2f}%)")

        stocks = sectors[top_sector]
        stock_data = []

        for stock in stocks:
            ticker = yf.Ticker(stock)
            hist = ticker.history(period='5d', interval='1m')

            if len(hist) > 0:
                current_price = hist['Close'].iloc[-1]
                sma_20 = hist['Close'].rolling(window=20).mean().iloc[-1]
                sma_50 = hist['Close'].rolling(window=50).mean().iloc[-1]

                recommendation = 'Buy' if current_price > sma_20 > sma_50 else 'Hold'

                stock_data.append({
                    'Stock': stock,
                    'Current Price': current_price,
                    'SMA 20': sma_20,
                    'SMA 50': sma_50,
                    'Recommendation': recommendation
                })

        df = pd.DataFrame(stock_data)

        with placeholder.container():
            st.write(f"⏱️ Updated at: {pd.Timestamp.now()}")
            st.dataframe(df)

        time.sleep(refresh_interval)
