from typing import Any
import streamlit as st
import types

from .logger import logger


def init_state(**kwargs: Any):
    """
    initialize the state of variables in streamlit session state when app is run for the first time
    """
    flag = "stutils_init_state"


    if flag not in st.session_state:
        logger.debug(f"{kwargs}")
        set(**kwargs)
    st.session_state[flag] = True
    

def set(**kwargs: Any):
    """
    set key, value in streamlit session state. If value is a function, it will be evaluated with the current key value and replace it
    """
    for key, value in kwargs.items():
        if isinstance(value, types.FunctionType):
            st.session_state[key] = value(st.session_state[key])
        else:
            st.session_state[key] = value


def get(*args: str) -> tuple:
    """
    get any number of keys from session state. a dict {key: value} is returned
    """
    return (st.session_state[key] for key in args)


def clear(*args: str):
    """
    clear any number of keys from session state
    """
    for key in args:
        del st.session_state[key]


def on_state(*, chain: bool = False, **kwargs: Any):
    """
    executes decorated function if the app state matches the one given in kwargs.
    For example:
    ```python
    init_state(retry_count=0)

    @on_state(retry_count=3)
    def retry_limit_reached():
        st.error("Retry limit reached")
        st.stop()
    ```
    In the above code, retry_limit_reached will only execute if the retry_count is 3.

    TODO add support for conditional expressions, similar to `@on_state(retry_count < 5)`
    """
    gateways = kwargs
    def decorator(func):
        def wrapper(*args, **kwargs):
            try:
                app_gateway_state = get(*gateways.keys())
                logger.debug(f"{app_gateway_state} | {gateways}")
            except KeyError:
                logger.warning(f"not all {gateways.keys()} were found in app state")
                return
            else:
                if app_gateway_state == gateways:
                    return func(*args, **kwargs)
        
        if chain:
            return wrapper      # do not execute the function, useful for chaining decorators or storing the function for later
        else:
            return wrapper()    # execute inner function, thus calling streamlit elements if any
    return decorator
