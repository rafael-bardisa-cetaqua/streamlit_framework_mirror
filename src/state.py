from typing import Any
import streamlit as st
import types

from .logger import logger


def set(**kwargs: Any):
    """
    set key, value in streamlit session state. If value is a function, it will be evaluated with the current key value and replace it
    """
    for key, value in kwargs.items():
        if isinstance(value, types.FunctionType):
            st.session_state[key] = value(st.session_state[key])
        else:
            st.session_state[key] = value


def get(*args: str):
    """
    get any number of keys from session state. a dict {key: value} is returned
    """
    return {key: st.session_state[key] for key in args}


def init_state(**kwargs: Any):
    """
    initialize the state of variables in streamlit session state when app is run for the first time
    """
    flag = "stutils_init_state"


    if flag not in st.session_state:
        logger.debug(f"{kwargs}")
        set(**kwargs)
    st.session_state[flag] = True
    