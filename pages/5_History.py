import streamlit as st
import pandas as pd
import os

# CSS content (shared from main styles.css)
current_dir = os.path.dirname(os.path.abspath(__file__))
root_dir = os.path.dirname(current_dir)
styles_path = os.path.join(root_dir, 'styles.css')

def load_css():
    try:
        with open(styles_path, 'r', encoding='utf-8') as f:
            return f.read()
    except FileNotFoundError:
        return ""

st.markdown(f'<style>{load_css()}</style>', unsafe_allow_html=True)

# Session validation
from utils import is_current_session_valid

if not is_current_session_valid():
    st.warning("Your session has expired. Please login again.")
    if st.button("Go to Login"):
        st.switch_page("pages/2_Login.py")
    st.stop()

# History page content
st.markdown('<div class="history-container">', unsafe_allow_html=True)

st.title("Aahar AI – Calculation History")
st.markdown("---")

history_file = 'history.csv'

try:
    history_df = pd.read_csv(history_file)
    if history_df.empty:
        st.info("You have no calculation history yet. Go to the calculator to get started!")
    else:
        st.dataframe(history_df)
except FileNotFoundError:
    st.info("You have no calculation history yet. Go to the calculator to get started!")

st.markdown('</div>', unsafe_allow_html=True)

# Navigation buttons
st.markdown("---")
col1, col2, col3 = st.columns([1,2,1])
with col2:
    if st.button('🏠 Back to Home', type='secondary', use_container_width=True):
        st.switch_page("pages/1_Landing.py")
    
    if st.button('➕ Go to Calculator', type='secondary', use_container_width=True):
        st.switch_page("pages/4_Calculator.py")
