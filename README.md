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