from pathlib import Path
from typing import Union
import streamlit as st

@st.cache_data
def fetch_css(path: Union[str, Path]) -> str:
    """
    loads a css file and returns an html style element as a string
    """
    with open(path, "r") as file:
        css = file.read()
    
    return f"<style>{css}</style>"


def load_css(path: Union[str, Path]) -> None:
    """
    loads a css file into the cache and renders it on the page
    """
    css = fetch_css(path)
    st.markdown(css, unsafe_allow_html=True)