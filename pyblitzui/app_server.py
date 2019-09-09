from flask import Flask, jsonify, request, render_template
from pyblitzui.script_loader import load_script, load_module


# DEFAULT_TEMPLATE_PATH = os.path.join(
#     os.path.dirname(os.path.dirname(__file__)),
#     "templates",
# )


class BlitzApp():
    def __init__(self, module, app=None):
        self._initialize_module(module)
        self._initialize_app(app)

    def _initialize_module(self, module):
        if isinstance(module, str):
            self._module = load_script(module)
        else:
            self._module = load_module(module)

        self._module_fns = {
            f['name']: f['function']
            for f in self._module['functions']
        }

        self._mod_fns_metadata = [
            {'name': f['name'], 'args': f['args']}
            for f in self._module['functions']
        ]

    def _initialize_app(self, app=None):
        self._app = app or Flask(__name__)

        self._app.route("/")(self.route_index)

        self._app.route("/function/list")(
            self.route_function_list
        )

        self._app.route("/function/call/<fn_name>", methods=['POST'])(
            self.route_function_call
        )

    def get_name(self):
        return self._module.__name__

    def route_index(self):
        return render_template("index.html")

    def get_function_list(self):
        return {'functions': self._mod_fns_metadata}

    def route_function_list(self):
        return jsonify(self.get_function_list())

    def execute_fn(self, fn_name, **kwargs):
        if fn_name not in self._module_fns:
            raise RuntimeError(f"Function {fn_name} not found.")
        return self._module_fns[fn_name](**kwargs)

    def route_function_call(self, fn_name):
        if fn_name not in self._module_fns:
            return jsonify({'output': f'ERROR: Function {fn_name} not found!'})

        try:
            kwargs = {
                k: eval(v)
                for k, v in request.json.items()
            }
            fn_output = self.execute_fn(fn_name, **kwargs)
        except Exception as e:
            return jsonify({'output': f'ERROR: {e}'})

        return jsonify({'output': fn_output})

    def run(self, **kwargs):
        self._app.run(**kwargs)
