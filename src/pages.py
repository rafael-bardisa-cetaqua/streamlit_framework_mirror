from pathlib import Path
import streamlit as st
from streamlit.source_util import (
    page_icon_and_name, 
    calc_md5, 
    get_pages,
    _on_pages_changed
)


MAIN_PAGE_NAME = st.secrets.script_name
MAIN_PAGE_PATH = Path(MAIN_PAGE_NAME).absolute().resolve()

PAGES_DIR = MAIN_PAGE_PATH.parent / "pages"


def delete_page(page_name: str) -> None:

    current_pages = get_pages(MAIN_PAGE_NAME)

    for key, value in current_pages.items():
        if value['page_name'] == page_name:
            del current_pages[key]
            break
        else:
            pass
    _on_pages_changed.send()


def add_page(page_name: str) -> None:
    
    pages = get_pages(MAIN_PAGE_NAME)

    script_path = [f for f in PAGES_DIR.glob("*.py") if f.name.find(page_name) != -1][0]
    script_path_str = str(script_path.resolve())
    pi, pn = page_icon_and_name(script_path)
    psh = calc_md5(script_path_str)
    pages[psh] = {
        "page_script_hash": psh,
        "page_name": pn,
        "icon": pi,
        "script_path": script_path_str,
    }
    _on_pages_changed.send()


def delete_pages() -> None:
    for page in list(PAGES_DIR.glob("*.py")):
        delete_page(str(page.name)[:-3])


def add_pages() -> None:
    for page in list(PAGES_DIR.glob("*.py")):
        add_page(str(page.name)[:-3])