import streamlit as st

def load_css(file_name):
    with open(file_name) as f:
        st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)

def iso_to_readable(iso_str):
    try:
        return iso_str.replace("T", " ").split(".")[0]
    except:
        return iso_str
