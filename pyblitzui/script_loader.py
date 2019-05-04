import os.path
import importlib.util

def load_script(script_path):
    # loading the file
    module_name = os.path.basename(script_path).strip(".py")
    spec = importlib.util.spec_from_file_location(module_name, script_path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)

    # listing functions
    valid_functions = [
        fn_name for fn_name in dir(module)
        if not fn_name.startswith("_")
        and hasattr(getattr(module, fn_name), '__call__')
    ]

    result = []

    for fn_name in valid_functions:
        func = getattr(module, fn_name)
        args = {}
        for i in range(func.__code__.co_argcount):
            if func.__defaults__ is not None:
                required = i < (func.__code__.co_argcount - len(func.__defaults__))
            else:
                required = True
            arg = func.__code__.co_varnames[i]
            if required:
                args[arg] = "REQUIRED"
            else:
                args[arg] = func.__defaults__[i-func.__code__.co_argcount]
        result.append({
            "name": fn_name,
            "function": func,
            "args": args
        })

    return result
