import io
import uuid
from threading import Thread
from contextlib import redirect_stdout
from tkinter.constants import END


class TextWidgetOutput:
    def __init__(self, widget):
        self.output_widget = widget

    def write(self, text):
        self.output_widget.configure(state="normal")
        self.output_widget.insert(END, text)
        self.output_widget.configure(state="disabled")

    def flush(self):
        self.output_widget.configure(state="normal")
        self.output_widget.delete(1.0, END)
        self.output_widget.configure(state="disabled")


class FunctionCallHandler:
    def __init__(self, function):
        self.call_uuid = uuid.uuid4()
        self.function = function
        self.stdout = io.StringIO()
        self.result = None
        self.finished = False

    def get_call_id(self):
        return str(self.call_uuid)

    def execute(self, **kwargs):
        with redirect_stdout(self.stdout):
            self.result = self.function(**kwargs)
            self.finished = True
            return self.result

    def execute_async(self, **kwargs):
        fn_thread = Thread(
            target=self.execute,
            kwargs=kwargs
        )
        fn_thread.start()

    def get_current_log(self):
        return self.stdout.getvalue()
