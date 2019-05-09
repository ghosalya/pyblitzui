import sys
import traceback
from datetime import datetime
from tkinter import filedialog
from tkinter import Tk, Frame, Label, Button, Entry, Menu
from tkinter.scrolledtext import ScrolledText
from tkinter.ttk import Notebook, Separator
from tkinter.constants import END

from .script_loader import load_script
from .utils import TextWidgetOutput


def get_log_time():
    return datetime.now().strftime("%y-%m-%d %H:%M:%S")


class ModuleFrame():
    def __init__(self, filepath=None):
        self.filepath = filepath
        self.frame = Tk()
    
    def build(self):
        self._load_script()
        if self.frame is not None:
            self.frame.destroy()

        self.frame = Tk()
        self.frame.title("PyBlitzUI - {}".format(self.filepath))
        self._build_menu()
        self._build_globalvar_domain()
        self._build_function_frames()
        self._pack_to_grid()
        return self.frame

    def _load_script(self):
        if self.filepath is None:
            self.filepath = filedialog.askopenfilename(
                title="Load python script"
            )
        self.script_meta = load_script(self.filepath)
        self.module = self.script_meta.get("module")
        self.function_list = self.script_meta.get("functions", [])
        self.global_vars = self.script_meta.get("globalvars", [])

    def _build_menu(self):
        self.menu = Menu(self.frame)
        self._file_menu = Menu(self.menu, tearoff=0)
        self._file_menu.add_command(label='Open..', command=self._open_command)
        self._file_menu.add_separator()
        self._file_menu.add_command(label='Exit', command=self.frame.quit)
        self.menu.add_cascade(label="File", menu=self._file_menu)
        self.frame.config(menu=self.menu)

    def _open_command(self):
        self.filepath = None
        self.build()

    def _build_globalvar_domain(self):
        self.globalvar_domain = Frame(self.frame)
        self.globalvar_frames = []
        for i in range(len(self.global_vars)):
            globalvar_spec = self.global_vars[i]
            globalvar_frame = GlobalvarFrame(
                self.module, globalvar_spec['name'], globalvar_spec['init_value']
            )
            globalvar_frame.build(self.globalvar_domain, index=i)
            self.globalvar_frames.append(globalvar_frame)
        self.domain_separator = Separator(self.frame, orient='horizontal')

    def _build_function_frames(self):
        self.tab_control = Notebook(self.frame)
        self.function_frames = []
        for function_spec in self.function_list:
            func_frame = FunctionFrame(
                func=function_spec["function"],
                name=function_spec.get("name", "<UNKFUNC>"),
                args=function_spec.get("args", {}),
            )
            func_frame.build(self.tab_control)
            self.tab_control.add(
                func_frame.frame, text=function_spec["name"]
            )
            self.function_frames.append(func_frame)

    def _pack_to_grid(self):
        self.globalvar_domain.grid(row=0, sticky='nsew')
        self.domain_separator.grid(row=1, sticky='ew')
        self.tab_control.grid(row=2, sticky='nsew')


class GlobalvarFrame():
    def __init__(self, module, name, init_value):
        self.name = name
        self.module = module
        if isinstance(init_value, str):
            self.init_value = '"{}"'.format(init_value)
        else:
            self.init_value = init_value
        self.current_value = init_value

    def build(self, root, index=0):
        self.frame = Frame(root)
        self.frame.grid(row=int(index/2), column=int(index%2), sticky='nsew')
        self.name_label = Label(self.frame, text=self.name)
        self.name_label.grid(row=0, column=0, sticky='nsew')
        self.entry = Entry(self.frame)
        self.entry.insert(0, str(self.init_value))
        self.entry.configure(state='disabled')
        self.entry.grid(row=0, column=1, sticky='nsew')
        self.button = Button(self.frame, text='Edit', command=self._edit)
        self.button.grid(row=0, column=2, sticky='nsew')
        return self.frame

    def _edit(self):
        self.entry.configure(state='normal')
        self.button.configure(text='Apply', command=self._apply)

    def _apply(self):
        if self._change_value():
            self.entry.configure(state='disabled')
            self.button.configure(text='Edit', command=self._edit)

    def _change_value(self):
        try:
            new_value = eval(self.entry.get())
            self.current_value = new_value
            setattr(self.module, self.name, new_value)
            return True
        except Exception:
            traceback.print_exc(file=sys.stdout)
            return False



class FunctionFrame():
    def __init__(self, func, name, args={}):
        self.name = name
        self.func = func
        self.args = args
    
    def build(self, root):
        self.frame = Frame(root)
        self._build_runner()
        self._build_args()
        self._build_output()
        self._bind_execution()
        return self.frame
        
    def _build_runner(self):
        self.name_label = Label(self.frame, text=self.name)
        self.name_label.grid(row=0, column=0, sticky='nsew')

        self.run_button = Button(self.frame, text="Run")
        self.run_button.grid(row=0, column=1, columnspan=2, sticky='nsew')

    def _build_args(self):
        self.arg_frames = []
        arg_items = list(self.args.items())
        for i in range(len(arg_items)):
            arg_name, arg_type = arg_items[i]
            arg_frame = self._build_arg_frame(arg_name, arg_type, i + 1)
            self.arg_frames.append(arg_frame)

    def _build_arg_frame(self, arg_name, arg_type, index):
        arg_label = Label(self.frame, text=arg_name)
        arg_label.grid(row=index, column=0, sticky='nsew')
        arg_entry = Entry(self.frame)
        arg_entry.grid(row=index, column=1, columnspan=3, sticky='nsew')
        if arg_type != "REQUIRED":
            arg_entry.insert(0, str(arg_type))
        return arg_entry

    def _build_output(self):
        index = len(self.args) + 1
        self.output_separator = Separator(self.frame, orient='horizontal')
        self.output_separator.grid(row=index, columnspan=3, sticky='ew')
        index += 1
        self.output_label = Label(self.frame, text="Output:")
        self.output_label.grid(row=index, column=0, sticky='w')
        self.output_clear = Button(self.frame, text="clear")
        self.output_clear.grid(row=index, column=2, sticky='nsew')
        self.output_label.grid(row=index, column=0, sticky='w')
        index += 1
        self.output_text = ScrolledText(self.frame, height=5, width=60)
        self.output_text.configure(state="disabled")
        self.output_text.grid(row=index, columnspan=3, sticky='nsew')
        self.stdout = TextWidgetOutput(self.output_text)
        self.output_clear.configure(command=self.stdout.flush)

    def _bind_execution(self):
        def execute():
            self.output_text.configure(state="normal")
            argstring = ", ".join([
                list(self.args.keys())[i] + "=" + str(self.arg_frames[i].get())
                for i in range(len(self.arg_frames))
            ])
            self.output_text.insert(
                END,
                "<{}> [in]: {}({}) \n".format(
                    get_log_time(), self.name, argstring
                )
            )
            self.output_text.configure(state="disabled")

            try:
                sys.stdout = self.stdout
                result = self.func(
                    *[eval(arg.get()) for arg in self.arg_frames]
                )
            except Exception as e:
                traceback.print_exc(file=self.stdout)
                result = "ERROR: " + str(e)

            self.output_text.configure(state="normal")
            self.output_text.insert(
                END,
                "<{}> [out]: {} \n".format(get_log_time(), result)
            )
            self.output_text.configure(state="disabled")

        self.__execute = execute

        self.run_button.configure(
            command=self.__execute
        )