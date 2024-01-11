from typing import Literal

import yaml
from pathlib import Path

import streamlit as st
import streamlit_authenticator as stauth

from .logger import logger


USERS_AUTH_FILE = Path(st.secrets.auth_file).absolute().resolve()

@st.cache_data
def _load_config(users_auth_file: Path):
    with open(users_auth_file, 'r') as file:
        logger.debug(f'Loading config from {USERS_AUTH_FILE}')
        config = yaml.load(file, Loader=yaml.SafeLoader)
    return config

config = _load_config(USERS_AUTH_FILE)

def _sync_config():
    with open(USERS_AUTH_FILE, 'w') as file:
        logger.debug(f'Syncing config changes to {USERS_AUTH_FILE}')
        yaml.dump(config, file, default_flow_style=False)

authenticator = stauth.Authenticate(
    config['credentials']
    , config['cookie']['name']
    , config['cookie']['key']
    , config['cookie']['expiry_days']
    , config['preauthorized']
)


def on_auth(*args: Literal[True, False, None], chain: bool = False):
    """
    execute function if user's auth state is one of *args. Possible state values are:
    * True: user is authenticated
    * False: user failed to authenticate
    * None: user is not authenticated, nor has it tried to do so
    """
    gateways = args
    def decorator(func):
        def wrapper(*args, **kwargs):
            if st.session_state.authentication_status in gateways:
                return func(*args, **kwargs)
            
        if chain:
            return wrapper      # do not execute the function, useful for chaining decorators or storing the function for later
        else:
            return wrapper()    # execute inner function, thus calling streamlit elements if any
    return decorator


def login_button(ask_prompt: str = 'Please enter your username and password'):
    # login user
    st.warning(ask_prompt)
    authenticator.login('Login')


def logout_button(logout_prompt: str = 'Logout', location: Literal['main', 'sidebar'] = 'main'):
    # logout user
    authenticator.logout(logout_prompt, location)


def register_button(register_prompt: str = 'Register user', success_prompt: str = 'User registered successfully'):
    # register new user
    try:
        if authenticator.register_user(register_prompt, preauthorization=True):
            st.success(success_prompt)

            _sync_config()
            
    except Exception as e:
        st.error(e)
