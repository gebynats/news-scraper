import streamlit as st
import yfinance as yf
import pandas as pd
import plotly.graph_objects as go
import time

st.set_page_config(page_title="IDX45 Sector Monitor", layout="wide")
st.title("📈 IDX45 Sector Performance Monitor with Stock Search")

# Sektor dan saham IDX45
sectors = {
    'Banking': ['BBCA.JK', 'BBRI.JK', 'BMRI.JK', 'BBNI.JK', 'ARTO.JK'],
    'Consumer': ['ICBP.JK', 'UNVR.JK', 'MYOR.JK', 'KLBF.JK', 'SIDO.JK'],
    'Energy': ['PGAS.JK', 'PTBA.JK', 'ADRO.JK', 'ITMG.JK', 'MEDC.JK'],
    'Telco': ['TLKM.JK', 'EXCL.JK', 'ISAT.JK'],
    'Infrastructure': ['JSMR.JK', 'WSKT.JK', 'PTPP.JK'],
    'Misc': ['ASII.JK', 'ANTM.JK', 'INDF.JK', 'MDKA.JK']
}

all_stocks = [item for sublist in sectors.values() for item in sublist]
stock_choice = st.multiselect('🔎 Cari Saham (Optional)', all_stocks)

refresh_interval = st.number_input('Refresh Interval (seconds)', min_value=5, max_value=3600, value=60)

placeholder = st.empty()

while True:
    sector_perf = {}

    # Hitung performa sektor
    for sector, tickers in sectors.items():
        gains = []
        for ticker in tickers:
            data = yf.Ticker(ticker).history(period='2d', interval='1d')
            if len(data) >= 2:
                open_price = data['Close'].iloc[-2]
                current_price = data['Close'].iloc[-1]
                change_pct = ((current_price - open_price) / open_price) * 100
                gains.append(change_pct)

        avg_gain = sum(gains) / len(gains) if gains else 0
        sector_perf[sector] = avg_gain

    # Ambil sektor terbaik
    sorted_sector = dict(sorted(sector_perf.items(), key=lambda x: x[1], reverse=True))
    top_sector = list(sorted_sector.keys())[0]

    stocks = sectors[top_sector]
    stock_data = []

    # Proses saham di sektor terbaik
    for stock in stocks:
        ticker = yf.Ticker(stock)
        hist = ticker.history(period='7d', interval='1h')

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
                'Recommendation': recommendation,
                'Data': hist
            })

    df = pd.DataFrame(stock_data)

    with placeholder.container():
        st.subheader(f"🔥 Best Performing Sector: {top_sector} ({sorted_sector[top_sector]:.2f}%)")
        st.write(f"⏱️ Updated at: {pd.Timestamp.now()}")
        st.dataframe(df[['Stock', 'Current Price', 'SMA 20', 'SMA 50', 'Recommendation']])

        st.subheader("📈 Stock Charts (7 Days)")
        for stock_info in stock_data:
            st.write(f"### {stock_info['Stock']}")
            fig = go.Figure()

            fig.add_trace(go.Scatter(x=stock_info['Data'].index, y=stock_info['Data']['Close'], name='Price'))
            fig.add_trace(go.Scatter(x=stock_info['Data'].index, y=stock_info['Data']['Close'].rolling(window=20).mean(), name='SMA 20'))
            fig.add_trace(go.Scatter(x=stock_info['Data'].index, y=stock_info['Data']['Close'].rolling(window=50).mean(), name='SMA 50'))

            fig.update_layout(title=f"{stock_info['Stock']} - Last 7 Days", xaxis_title="Date", yaxis_title="Price", legend_title="Indicators")
            st.plotly_chart(fig, use_container_width=True)

        # Tambahkan filter saham manual
        if stock_choice:
            st.subheader("🔍 Performance of Selected Stocks")
            for selected_stock in stock_choice:
                ticker = yf.Ticker(selected_stock)
                hist = ticker.history(period='7d', interval='1h')

                if len(hist) > 0:
                    current_price = hist['Close'].iloc[-1]
                    sma_20 = hist['Close'].rolling(window=20).mean().iloc[-1]
                    sma_50 = hist['Close'].rolling(window=50).mean().iloc[-1]
                    recommendation = 'Buy' if current_price > sma_20 > sma_50 else 'Hold'

                    st.write(f"### {selected_stock} - Current Price: {current_price:.2f} ({recommendation})")
                    fig = go.Figure()
                    fig.add_trace(go.Scatter(x=hist.index, y=hist['Close'], name='Price'))
                    fig.add_trace(go.Scatter(x=hist.index, y=hist['Close'].rolling(window=20).mean(), name='SMA 20'))
                    fig.add_trace(go.Scatter(x=hist.index, y=hist['Close'].rolling(window=50).mean(), name='SMA 50'))
                    fig.update_layout(title=f"{selected_stock} - Last 7 Days", xaxis_title="Date", yaxis_title="Price", legend_title="Indicators")
                    st.plotly_chart(fig, use_container_width=True)

    time.sleep(refresh_interval)
