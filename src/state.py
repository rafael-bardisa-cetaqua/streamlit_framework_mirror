import streamlit as st
import types


def set(**kwargs):
    """
    set key, value in streamlit session state. If value is a function, it will be evaluated with the current key value and replace it
    """
    for key, value in kwargs.items():
        if isinstance(value, types.FunctionType):
            st.session_state[key] = value(st.session_state[key])
        else:
            st.session_state[key] = value


def get(*args):
    """
    get any number of keys from session state. a dict {key: value} is returned
    """
    return {key: st.session_state[key] for key in args}


def init_state(**kwargs):
    """
    initialize the state of variables in streamlit session state when app is run for the first time
    """
    flag = "stutils_init_state"

    if flag not in st.session_state:
        set(**kwargs)
    st.session_state[flag] = True
    