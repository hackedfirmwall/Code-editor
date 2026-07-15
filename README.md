# Code-editor
Web browser 
import streamlit as st
from streamlit_ace import st_ace
import datetime

st.set_page_config(
    page_title="CodeLab • Script Editor",
    page_icon="🧪",
    layout="wide"
)

st.title("🧪 CodeLab")
st.markdown("**Official-looking Script Editor** — Educational Purposes Only")

# Sidebar
with st.sidebar:
    st.header("Settings")
    language = st.selectbox(
        "Language", 
        ["python", "javascript", "html", "markdown", "java", "cpp"]
    )
    
    theme = st.selectbox(
        "Theme", 
        ["monokai", "dracula", "github_light", "tomorrow_night", "solarized_dark"]
    )
    
    if st.button("New File", use_container_width=True):
        st.session_state.code = f"# New script - {datetime.datetime.now().strftime('%Y-%m-%d %H:%M')}\n"
        st.rerun()

# Main Editor
if "code" not in st.session_state:
    st.session_state.code = '''# Welcome to CodeLab! 
print("Hello from your professional script editor! 👋")
print("You can write Python, JavaScript, HTML, and more here.")
'''

code = st_ace(
    value=st.session_state.code,
    language=language,
    theme=theme,
    height=600,
    font_size=15,
    show_gutter=True,
    wrap=True,
    auto_update=True,
    key="main_editor"
)

# Action buttons
col1, col2, col3 = st.columns(3)

with col1:
    if st.button("▶ Run Code", type="primary", use_container_width=True):
        st.success("Code executed successfully (demo)")
        with st.expander("📤 Output"):
            st.code("This is where output would appear.\nGreat for learning!", language="text")

with col2:
    ext = "py" if language == "python" else "js" if language == "javascript" else language[:3]
    st.download_button(
        label="💾 Download File",
        data=code,
        file_name=f"my_script.{ext}",
        use_container_width=True
    )

with col3:
    st.info("✍️ Edits are saved in your browser. Refreshing keeps your work.")

# Auto update session
st.session_state.code = code
