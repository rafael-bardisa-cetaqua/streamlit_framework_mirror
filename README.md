Small streamlit framework that provides utils to manage authentication status, pages and application state

---
# Installation

The framework can be installed from the gitlab repository and any mirrors, provided the user has access to them:
```bash
pip install git+ssh://git@gitlab.com/cetaquads/toolbox/streamlit_framework
```
---
# Usage

## Overview
The framework provides five different modules:

- [auth.py](#auth): encapsulates [streamlit_authenticator](https://github.com/mkhorasani/Streamlit-Authenticator) and provides functions to create login and logout buttons, and control flow depending on the user's authentication status.
- [pages.py](#pages): provides functions for controlling which pages are shown in the sidebar.
- [state.py](#state): provides functions to manipulate application session state, variable inicialization, and control flow based on the application's session state
- [structure.py](#structure): provides the `HTMLElement` and `HTMLTemplate` classes that allow lower level control of UI elements in the app.
- [style.py](#style): provides the `load_css` function, that injects a css file into the page, providing more low level control of the application's presentation.

In order to use the `auth` module, you need to specify the `auth_file` field in the `.streamlit/secrets.toml` file:

```secrets.toml
auth_file = ".streamlit/config.yaml"
```

For the `pages` module, you need to specify `script_name`:

```secrets.toml
script_name = <main page script name>
```

## Auth
The `auth` module provides the following functions for controlling access to the application:
```python
def login_button(ask_prompt: str = 'Please enter your username and password'
				) -> None

def logout_button(logout_prompt: str = 'Logout'
				  , location: Literal['main', 'sidebar'] = 'main'
				  ) -> None

def register_button(register_prompt: str = 'Register user'
					, success_prompt: str = 'User registered successfully'
					) -> None
```
Each of these create a [streamlit_authenticator](https://github.com/mkhorasani/Streamlit-Authenticator) prompt and change the user's authentication status accordingly. `register_button` also synchronizes the received information with the authentication file.

Furthermore, the `on_auth` decorator is available:
```python
def on_auth(*args: Literal[True, False, None]
			, chain: bool = False
			) -> Union[Callable, None]:
```
This decorator allows blocks of code to only be executed if the application's authentication state matches the one given to the decorator:

```python
@on_auth(True)
def will_run_when_logged_in():
	st.write("Logged in!")

@on_auth(False)
def will_run_when_failed_login():
	st.write("Invalid login!")

@on_auth(None)
def will_run_when_no_attempted_login():
	st.write("Please log in to continue to the app")

@on_auth(None, False)
def will_run_when_not_logged_in():
	st.write("login")
	login_button()
```

In the above example, if the user has logged in, `"Logged in!"` will be shown on the app. If the user failed to log in, `"Invalid login!"`, `"login"` and a login button will be shown in the app. If no login attempts have been made, `"Please log in to continue to the app"`, `"login"` and a login button will be shown in the app.

The application log in state can be one of:

- `True`: The user has successfully logged in
- `False`: The user tried to log in but failed
- `None`: The user has not tried to log in

By default, the decorated function will be executed immediately as the decorator is called. Its intended use is to conditionally run the blocks of code wrapped in the decorated functions. However, there are some cases in which you would want the standard decorator behaviour. This can be toggled with the chain keyword argument:

```python
@on_auth(True)
def no_chain():
	# some streamlit code
# streamlit code is run if auth status is True

no_chain() # TypeError: 'NoneType' object is not callable

@on_auth(True, chain=True)
def chain():
	# some streamlit code

chain() # streamlit code is run if auth status is True
```

The two main cases where the chain parameter is useful are:
- You want to reuse the code in a function
- You want to stack multiple decorators for the same function
```python
# enable the chain parameter to define the function and call it later
@on_auth(True, chain=True)
def will_run_when_called_and_logged_in(name: str):
	st.write(f"{name} Logged in and function called!")

# prints "Logged in and function called!" 3 times
will_run_when_called_and_logged_in("Marcos")
will_run_when_called_and_logged_in("Roberto")
will_run_when_called_and_logged_in("Paula")
```

```python
@st.cache_data
@on_auth(True)
def will_raise_error():
	# some code

@st.cache_data
@on_auth(True, chain=True)
def will_work():
	# some code

# The following are functionally equivalent:
@on_auth(False)
@on_auth(True, chain=True)
def foo():
	# some code

@on_auth(False, True)
def foo():
	# some code
```
## Pages
The `pages` module provides the following functions to control which pages the user can navicate to:
```python
def delete_page(page_name: str
			   ) -> None

def add_page(page_name: str
			) -> None

def delete_pages() -> None

def add_pages() -> None
```

You can use these functions to add or remove navigation to any page in the `pages` subdirectory.

## State
The `state` module provides the following functions to control application state:
```python
def init_state(page_name: Union[str, None]=None
			   , /
			   , **kwargs: Any
			   ) -> None

def set(**kwargs: Any
	   ) -> None

def get(*args: str
	   ) -> Union[Any, Tuple[Any, ...]]

def clear(*args: str
		 ) -> None
```

## Structure
This module contains the 
## Style
This module contains one function to load a css file

---
