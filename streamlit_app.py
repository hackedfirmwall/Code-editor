import streamlit as st

st.set_page_config(
    page_title="CryptoCode Lab",
    page_icon="₿",
    layout="wide",
    initial_sidebar_state="expanded"
)import streamlit as st
from streamlit_ace import st_ace
import datetime
import requests

st.set_page_config(
    page_title="CryptoCode Lab • Live Market",
    page_icon="₿",
    layout="wide"
)

# Header
st.title("₿ CryptoCode Lab")
st.markdown("**Professional Script Editor + Live Crypto Market** — Educational Purposes")

# Live Crypto Prices (Sidebar)
with st.sidebar:
    st.header("📊 Live Market")
    try:
        # Free CoinGecko API
        response = requests.get("https://api.coingecko.com/api/v3/simple/price?ids=bitcoin,ethereum,solana,ripple&vs_currencies=usd&include_24hr_change=true")
        data = response.json()
        
        coins = ["bitcoin", "ethereum", "solana", "ripple"]
        for coin in coins:
            price = data[coin]["usd"]
            change = data[coin]["usd_24h_change"]
            emoji = "🟢" if change >= 0 else "🔴"
            st.metric(
                label=coin.capitalize(),
                value=f"${price:,.2f}",
                delta=f"{change:.2f}%"
            )
    except:
        st.warning("Live prices unavailable (demo mode)")

    st.divider()
    
    st.header("Editor Settings")
    language = st.selectbox(
        "Language", 
        ["python", "javascript", "html", "markdown"]
    )
    
    theme = st.selectbox(
        "Theme", 
        ["monokai", "dracula", "github_light", "tomorrow_night"]
    )
    
    if st.button("New Crypto Script", use_container_width=True):
        st.session_state.code = f"# Crypto Trading Script - {datetime.datetime.now().strftime('%Y-%m-%d')}\n\n"
        st.rerun()

# Main Area - Split into Editor + Preview
col_editor, col_preview = st.columns([3, 2])

with col_editor:
    st.subheader("✍️ Script Editor")
    if "code" not in st.session_state:
        st.session_state.code = '''# Example Crypto Analysis Script
import pandas as pd
import numpy as np

print("🚀 Welcome to CryptoCode Lab!")
print("You can write trading bots, analysis scripts, or backtesters here.")

# Example: Simple moving average crossover logic
price = 65000
sma_short = 64000
sma_long = 63000

if sma_short > sma_long:
    print("🟢 BUY Signal - Bullish crossover")
else:
    print("🔴 SELL Signal")
'''

    code = st_ace(
        value=st.session_state.code,
        language=language,
        theme=theme,
        height=620,
        font_size=15,
        show_gutter=True,
        wrap=True,
        auto_update=True,
        key="crypto_editor"
    )

with col_preview:
    st.subheader("📈 Market Preview")
    st.info("Live charts & images can be added here (example below)")
    
    # Example crypto images / placeholders
    st.image("https://www.coingecko.com/coins/images/1/large/bitcoin.png", width=80)
    st.image("https://www.coingecko.com/coins/images/279/large/ethereum.png", width=80)
    
    # Simple live chart simulation
    st.line_chart([62000, 63500, 62800, 64500, 65800, 67200], use_container_width=True)
    
    st.caption("💡 You can connect real APIs or TradingView widgets in advanced versions.")

# Bottom Toolbar
col1, col2, col3 = st.columns(3)

with col1:
    if st.button("▶ Run Script", type="primary", use_container_width=True):
        st.session_state.code = code
        st.success("✅ Script ran successfully!")
        with st.expander("Output"):
            st.code("Output / Trading signals would appear here...", language="text")

with col2:
    ext = "py" if language == "python" else language[:3]
    st.download_button(
        "💾 Download Script",
        code,
        file_name=f"crypto_script.{ext}",
        use_container_width=True
    )

with col3:
    st.info("Auto-saved in browser • Educational Tool")

st.session_state.code = code
