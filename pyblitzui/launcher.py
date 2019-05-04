from .frame import ModuleFrame


def run():
    main_frame = ModuleFrame().build()
    main_frame.mainloop()


if __name__ == "__main__":
    run()
