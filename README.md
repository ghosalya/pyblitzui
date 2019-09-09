# pyblitzui

A fast &amp; simple GUI launcher for Python 3 scripts.



# Installation

```
pip install git+https://github.com/ghosalya/pyblitzui.git@master
```

Note: Requires Python 3.4+

# Usage

You can run this command to start the BlitzUI interface.

```
pyblitzui
```

# Caveats

1. `pyblitzui` expects an "importable" python scripts, meaning that lines that runs on script execution should be under the following condition:
    ```
    if __name__ == "__main__":
    ```
    Other lines e.g. function definition and import statements should be per usual.
2. `pyblitzui` does not manage environments. This means that the dependency of the selected python scripts should be installed in the same environment as `pyblitzui` for it to run properly.
3. Inputs in `pyblitzui` are considered a line of python code; hence a string must be quoted, for example. This is a design decision so that one can differentiate e.g. a `4` from a `"4"`


# NEW: React Mode

1. npm install && pip install -e .
2. npm run start && python server.py
3. visit localhost:3000


# Example

Run
```
python examples/simple_ui/server.py
```

# Routes

* `/`: Go to main panel that list all the functions
* `/function/list`: Module metadata, which is a list of name & args in JSON format
* `/function/call/<fn_name>` (POST): given a JSON of args, call the function with those args
    Returns a call_id that can be used for fetching logs.
* `/function/logs/<call_id>`: Fetch the current state of logs at the current time.
