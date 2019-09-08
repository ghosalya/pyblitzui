#!/usr/bin/env python

import os
from flask import Flask, render_template, jsonify, request
from pyblitzui import script_loader

app = Flask(__name__)

loaded_module = script_loader.load_script("./blitz_ui.py")
module_fns = {
    f['name']: f['function']
    for f in loaded_module['functions']
}
functions_metadata = [
    {'name': f['name'], 'args': f['args']}
    for f in loaded_module['functions']
]
available_functions = [f['name'] for f in functions_metadata]


@app.route("/")
def index():
    return render_template('index.html')


# TODO: Make session-based?
@app.route("/function/list")
def get_function_list():
    return jsonify({
        'functions': functions_metadata
    })


@app.route("/function/call/<fn_name>", methods = ['POST'])
def function_call(fn_name):
    if fn_name not in available_functions:
        return jsonify({'output': f'Function {fn_name} not found!'})

    try:
        print(f'called {fn_name} with args: {request.json}')
        kwargs = {
            k: eval(v)
            for k, v in request.json.items()
        }
        fn_output = module_fns[fn_name](**kwargs)
    except Exception as e:
        print(e)

    return jsonify({'output': fn_output})

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=os.environ.get('PORT', 3000), debug=True)
