Small streamlit framework that provides utils to manage authentication status, pages and application state

---
# Installation

The framework can be installed from the gitlab repository and any mirrors, provided the user has access to them:
```bash
pip install git+ssh://git@gitlab.com/cetaquads/toolbox/streamlit_framework
```
---
# Usage

The framework provides five different modules:
- `auth.py`: encapsulates [streamlit_authenticator](https://github.com/mkhorasani/Streamlit-Authenticator) and provides functions to create login and logout buttons, and control flow depending on the user's authentication status.
- `pages.py`: provides functions for controlling which pages are shown in the sidebar.
- `state.py`: provides functions to manipulate application session state, variable inicialization, and control flow based on the application's session state
- `structure.py`: provides the `HTMLElement` and `HTMLTemplate` classes that allow lower level control of UI elements in the app.
- `style.py`: provides the `load_css` function, that injects a css file into the page, providing more low level control of the application's presentation.

In order to use the `auth` module, you need to specify the `auth_file` field in the `.streamlit/secrets.toml` file:

```secrets.toml
auth_file = ".streamlit/config.yaml"
```

For the `pages` module, you need to specify `script_name`:

```secrets.toml
script_name = <main page script name>
```
---
