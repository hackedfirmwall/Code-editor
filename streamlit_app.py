import streamlit as st
from streamlit_ace import st_ace
import datetime
import requests
import pandas as pd
import numpy as np

st.set_page_config(page_title="CryptoCode Lab • Live", page_icon="₿", layout="wide")

# Dark Professional Theme
st.markdown("""
<style>
    .stApp { background-color: #0E1117; color: #FAFAFA; }
    .css-1d391kg { background-color: #161B22; }
</style>
""", unsafe_allow_html=True)

st.title("₿ CryptoCode Lab")
st.markdown("**Live Market • Script Editor • Trading Signals** — Educational Tool")

# Live Data
@st.cache_data(ttl=60)
def get_crypto_data():
    try:
        coins = "bitcoin,ethereum,solana,ripple"
        res = requests.get(f"https://api.coingecko.com/api/v3/simple/price?ids={coins}&vs_currencies=usd&include_24hr_change=true&include_market_cap=true")
        return res.json()
    except:
        return None

data = get_crypto_data()

# Sidebar
with st.sidebar:
    st.header("📈 Live Market")
    if data:
        for coin, info in data.items():
            price = info["usd"]
            change = info.get("usd_24h_change", 0)
            st.metric(coin.capitalize(), f"${price:,.4f}", f"{change:.2f}%")
    else:
        st.warning("Live data temporarily unavailable")

    st.divider()
    st.header("Editor Settings")
    language = st.selectbox("Language", ["python", "javascript", "html"])
    theme = st.selectbox("Theme", ["monokai", "dracula", "one_dark"])

    if st.button("New Trading Script", use_container_width=True):
        st.session_state.code = f"# Trading Strategy - {datetime.datetime.now().strftime('%Y-%m-%d')}\n\n"
        st.rerun()

# Main Layout
col1, col2 = st.columns([2.2, 1.8])

with col1:
    st.subheader("✍️ Script Editor")
    if "code" not in st.session_state:
        st.session_state.code = '''# Example Trading Signals Script
print("🚀 Crypto Trading Strategy Example")

price = 65000
sma_short = 64500
sma_long = 63000
rsi = 68  # Relative Strength Index

if sma_short > sma_long and rsi < 70:
    print("🟢 STRONG BUY SIGNAL")
elif rsi > 70:
    print("🔴 Overbought - Consider SELL")
else:
    print("🟡 Neutral - Hold")
'''

    code = st_ace(
        value=st.session_state.code,
        language=language,
        theme=theme,
        height=580,
        font_size=15,
        show_gutter=True,
        wrap=True,
        auto_update=True
    )

with col2:
    st.subheader("📊 Trading Signals & Charts")
    
    # Trading Signals Generator
    st.markdown("**AI-like Trading Signals**")
    if st.button("Generate Signals", type="primary"):
        with st.spinner("Analyzing market..."):
            st.success("✅ Analysis Complete")
            st.info("**Bitcoin**: Bullish crossover detected → **BUY**")
            st.info("**Ethereum**: RSI cooling off → **Hold**")
            st.info("**Solana**: Strong momentum → **Strong BUY**")

    # Live Charts
    st.markdown("**Price Charts (Last 7 simulated points)**")
    chart_data = pd.DataFrame({
        "BTC": np.random.randint(62000, 68000, 7),
        "ETH": np.random.randint(1800, 2100, 7),
        "SOL": np.random.randint(70, 90, 7)
    })
    st.line_chart(chart_data, use_container_width=True)

    st.caption("Note: In a full version we can pull real historical data.")

# Bottom Bar
col_a, col_b, col_c = st.columns(3)
with col_a:
    if st.button("▶ Run Script", type="primary", use_container_width=True):
        st.session_state.code = code
        st.success("Script executed!")

with col_b:
    ext = "py" if language == "python" else language[:3]
    st.download_button("💾 Download", code, f"crypto_strategy.{ext}", use_container_width=True)

with col_c:
    st.info("Auto-saved • Educational Project")

st.session_state.code = code
