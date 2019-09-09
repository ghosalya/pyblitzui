from flask import Flask, jsonify, request, render_template
from pyblitzui.script_loader import load_script, load_module
from pyblitzui.utils import FunctionCallHandler


class BlitzApp():
    def __init__(self, module, app=None):
        self._initialize_module(module)
        self._initialize_app(app)
        self.call_handlers = {}

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

        self._app.route("/function/logs/<call_id>")(
            self.route_get_call_log
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
        # return self._module_fns[fn_name](**kwargs)

        call_handler = FunctionCallHandler(self._module_fns[fn_name])
        cid = call_handler.get_call_id()
        self.call_handlers[cid] = call_handler
        call_handler.execute_async(**kwargs)
        return cid

    def route_function_call(self, fn_name):
        if fn_name not in self._module_fns:
            return jsonify({'error': f'ERROR: Function {fn_name} not found!'})

        eval_kwargs = {}
        for k, v in request.json.items():
            try:
                eval_v = eval(v)
                eval_kwargs[k] = eval_v
            except Exception as e:
                return jsonify({'error': f'ERROR while parsing {k}: {e}'})

        try:
            call_id = self.execute_fn(fn_name, **eval_kwargs)
        except Exception as e:
            return jsonify({'error': f'ERROR: {e}'})

        return jsonify({'call_id': call_id})

    def route_get_call_log(self, call_id):
        call_handler = self.call_handlers[call_id]
        result = {
            'logs': call_handler.get_current_log(),
            'output': call_handler.result
        }
        return jsonify(result)

    def run(self, **kwargs):
        self._app.run(**kwargs)
