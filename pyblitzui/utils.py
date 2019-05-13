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


def displayed_string(value):
    if isinstance(value, str):
        return '"{}"'.format(value)
    else:
        return str(value)