import tkinter as tk
from . import usage_parser
from . import utils


class Application(tk.Tk):
    def __init__(self, path):
        super().__init__()

        self.path = path
        self.script = utils.load_module(self.path, 'script')
        self.commands = usage_parser.get_commands(self.script.__doc__)

        self.main_frame = MainFrame(self, self.commands, self.run_command)

        self.main_frame.pack()

    def run(self):
        self.mainloop()

    def run_command(self, args):
        self.script.main(args)


class MainFrame(tk.Frame):
    def __init__(self, parent, commands, on_run):
        super().__init__(parent)

        self.command = tk.StringVar(self)
        self.command.trace_variable('w', self.on_select_command)
        self.command_frames = {cmd.name: None for cmd in commands}
        self.on_run = on_run

        commands_container = tk.Frame(self)
        for cmd in commands:
            self.command_frames[cmd.name] = CommandFrame(commands_container, cmd)
            self.command_frames[cmd.name].pack()

        tk.OptionMenu(self, self.command, *self.command_frames.keys()).pack()
        commands_container.pack()
        tk.Button(self, text="Run", command=self.run).pack()

        self.command.set(commands[0].name)

    def run(self):
        frame = self.command_frames[self.command.get()]
        args = dict(frame.arguments)

        for cmd in self.command_frames:
            args[cmd] = False
        args[frame.command.name] = True

        self.on_run(args)


    def on_select_command(self, *_):
        for name, frame in self.command_frames.items():
            if name == self.command.get():
                frame.pack()
            else:
                frame.pack_forget()


class CommandFrame(tk.Frame):
    def __init__(self, parent, command):
        super().__init__(parent)

        self.command = command
        self.args = {}

        self.title_label.grid(row=0, column=0, columnspan=2)
        for i, arg in enumerate(command.args, 1):
            tk.Label(self, text=arg.name).grid(row=i, column=0)
            self.args[arg.name] = tk.StringVar(self)
            tk.Entry(self, textvariable=self.args[arg.name]).grid(row=i, column=1)

    @property
    def title_label(self):
        if self.command.name:
            title = "Command %s" % self.command.name
        else:
            title = "Script without command"

        return tk.Label(self, text=title)

    @property
    def arguments(self):
        return {arg: var.get() for arg, var in self.args.items()}
