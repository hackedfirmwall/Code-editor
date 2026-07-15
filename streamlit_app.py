import streamlit as st
from streamlit_ace import st_ace
import datetime
import requests
import pandas as pd
import numpy as np

st.set_page_config(page_title="CryptoCode Lab", page_icon="₿", layout="wide")

# Dark Theme
st.markdown("""
<style>
    .stApp { background-color: #0E1117; color: #FAFAFA; }
    .css-1d391kg { background-color: #161B22; }
</style>
""", unsafe_allow_html=True)

# Initialize Session State
if "users" not in st.session_state:
    st.session_state.users = {}           # username: password
if "current_user" not in st.session_state:
    st.session_state.current_user = None
if "files" not in st.session_state:
    st.session_state.files = {"main.py": "# Welcome to your personal workspace!"}
if "code" not in st.session_state:
    st.session_state.code = "# Start coding here...\n"

# ====================== LOGIN / SIGNUP ======================
if st.session_state.current_user is None:
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.title("₿ CryptoCode Lab")
        st.markdown("**Educational Script Editor**")
        
        tab1, tab2 = st.tabs(["🔑 Login", "📝 Sign Up"])
        
        with tab1:
            username = st.text_input("Username", key="l_user")
            password = st.text_input("Password", type="password", key="l_pass")
            if st.button("Login", use_container_width=True):
                if username in st.session_state.users and st.session_state.users[username] == password:
                    st.session_state.current_user = username
                    st.rerun()
                else:
                    st.error("Invalid username or password")
        
        with tab2:
            new_user = st.text_input("Choose Username", key="s_user")
            new_pass = st.text_input("Choose Password", type="password", key="s_pass")
            if st.button("Create Account", use_container_width=True):
                if new_user and new_pass:
                    if new_user in st.session_state.users:
                        st.error("Username already exists")
                    else:
                        st.session_state.users[new_user] = new_pass
                        st.success("Account created successfully! Please Login.")
                else:
                    st.error("Please fill all fields")
else:
    # ====================== MAIN APP (Logged In) ======================
    st.sidebar.success(f"👤 {st.session_state.current_user}")
    if st.sidebar.button("Logout"):
        st.session_state.current_user = None
        st.rerun()

    st.title(f"Welcome back, {st.session_state.current_user}!")

    # Live Market Sidebar
    with st.sidebar:
        st.header("📊 Live Market")
        try:
            res = requests.get("https://api.coingecko.com/api/v3/simple/price?ids=bitcoin,ethereum,solana&vs_currencies=usd&include_24hr_change=true")
            prices = res.json()
            for coin in ["bitcoin", "ethereum", "solana"]:
                p = prices[coin]["usd"]
                ch = prices[coin].get("usd_24h_change", 0)
                st.metric(coin.capitalize(), f"${p:,.2f}", f"{ch:.2f}%")
        except:
            st.write("Live prices loading...")

        st.divider()
        st.header("💾 Files")
        filename = st.text_input("Save as", "strategy.py")
        if st.button("Save Script"):
            st.session_state.files[filename] = st.session_state.code
            st.success("Saved!")

        if st.session_state.files:
            load_file = st.selectbox("Load Script", options=list(st.session_state.files.keys()))
            if st.button("Load"):
                st.session_state.code = st.session_state.files[load_file]
                st.rerun()

    # Main Editor + Charts
    col1, col2 = st.columns([2, 1])

    with col1:
        st.subheader("✍️ Script Editor")
        code = st_ace(
            value=st.session_state.code,
            language="python",
            theme="monokai",
            height=520,
            font_size=15,
            show_gutter=True,
            wrap=True,
            auto_update=True
        )

    with col2:
        st.subheader("📈 7-Day Price Chart")
        coin = st.selectbox("Coin", ["bitcoin", "ethereum", "solana"])
        try:
            url = f"https://api.coingecko.com/api/v3/coins/{coin}/market_chart?vs_currency=usd&days=7"
            data = requests.get(url).json()['prices']
            df = pd.DataFrame(data, columns=['time', 'price'])
            df['time'] = pd.to_datetime(df['time'], unit='ms')
            st.line_chart(df.set_index('time')['price'])
        except:
            st.info("Chart loading...")

        st.subheader("▶ Execute Code")
        if st.button("Run Code", type="primary"):
            try:
                exec_output = st.empty()
                old_stdout = __import__('sys').stdout
                __import__('sys').stdout = mystdout = __import__('io').StringIO()
                exec(code)
                output = mystdout.getvalue()
                __import__('sys').stdout = old_stdout
                if output:
                    st.code(output)
                else:
                    st.success("Code executed successfully!")
            except Exception as e:
                st.error(f"Error: {str(e)}")

    st.session_state.code = code

    st.download_button("💾 Download Script", code, "my_script.py")
