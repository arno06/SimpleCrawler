from tkinter import *
from tkinter import ttk


class Main():
    def __init__(self):
        self.running = False
        self.toggle_handler = None
        self.window = Tk()
        self.window.columnconfigure(0, weight=1)
        self.window.rowconfigure(0, weight=1)

        self.main_panel = ttk.Frame(self.window, padding=(5, 5, 5, 5))
        self.main_panel.grid(column=0, row=0, sticky=(N, S, E, W))
        self.main_panel.columnconfigure(0, weight=1)
        self.main_panel.rowconfigure(1, weight=1)

        self.nav_panel = ttk.Frame(self.main_panel)
        self.nav_panel.grid(column=0, row=0, sticky=(N, E, W))
        self.nav_panel.columnconfigure(0, weight=1)

        self.base_url = StringVar()
        self.base_url.set("http://")
        self.entry = ttk.Entry(self.nav_panel, textvariable=self.base_url, width=100)
        self.toggle_button = ttk.Button(self.nav_panel, text="Go", command=self.click_handler)
        self.entry.grid(column=0, row=0, sticky=(N, W, E, S))
        self.toggle_button.grid(column=1, row=0, sticky=(N, W, E, S))

        self.content = ttk.Frame(self.main_panel, padding=(0, 5, 0, 0))
        self.content.grid(column=0, row=1, sticky=(N, W, E, S))
        self.content.columnconfigure(0, weight=1)
        self.content.rowconfigure(0, weight=1)

        self.left_content = ttk.Frame(self.content)
        self.left_content.grid(column=0, row=0, sticky=(N, W, E, S))
        self.left_content.columnconfigure(0, weight=1)
        self.left_content.rowconfigure(1, weight=1)
        self.content.columnconfigure(0, weight=1)

        self.todo_count = ttk.Label(self.left_content, text=" ")
        self.todo_count.grid(column=0, row=0, sticky=(N, W, E, S))

        scrollbar = ttk.Scrollbar(self.left_content)
        self.todo_label = Text(self.left_content, yscrollcommand=scrollbar.set)
        scrollbar.config(command=self.todo_label.yview)

        self.todo_label.grid(column=0, row=1, sticky=(N, W, E, S))
        scrollbar.grid(column=1, row=1, sticky=(N, W, E, S))

        self.right_content = ttk.Frame(self.content)
        self.right_content.grid(column=1, row=0, sticky=(N, W, E, S))
        self.content.columnconfigure(1, weight=1)
        self.content.rowconfigure(0, weight=1)
        self.right_content.columnconfigure(0, weight=1)
        self.right_content.rowconfigure(1, weight=1)

        scrollbar = ttk.Scrollbar(self.right_content)
        self.main_label = Text(self.right_content, yscrollcommand=scrollbar.set)
        scrollbar.config(command=self.main_label.yview)

        self.main_label.grid(column=0, row=1, sticky=(N, W, E, S))
        scrollbar.grid(column=1, row=1, sticky=(N, W, E, S))

        self.done_count = ttk.Label(self.right_content, text=" ")
        self.done_count.grid(column=0, row=0, sticky=(N, W, E, S))

    def mainloop(self):
        self.window.mainloop()

    def update(self, _tbd, _crawled, _global_time, _remaining):
        self.todo_count['text'] = str(len(_tbd))+" urls restantes ("+self.format_time(_remaining)+")"
        self.todo_label.delete(1.0, END)
        self.todo_label.insert(END, "\n".join(_tbd))
        self.done_count['text'] = str(len(_crawled))+" urls parcourues ("+self.format_time(_global_time)+")"
        self.main_label.delete(1.0, END)
        self.main_label.insert(END, "\n".join(_crawled))

    def click_handler(self):
        if self.toggle_handler is None or callable(self.toggle_handler) is False or self.base_url.get() == "http://":
            return

        self.running = False if self.running is True else True

        if self.running is True:
            self.entry.config(state="disable")
            self.toggle_button.config(text='Stop')
        else:
            self.entry.config(state="normal")
            self.toggle_button.config(text='Go')

        self.toggle_handler(self.running, self.base_url.get())

    def reset(self):
        if self.running is True:
            self.click_handler()

    @staticmethod
    def format_time(_time):
        if _time < 60:
            return str(round(_time, 2))+" sec"
        _time /= 60
        if _time < 60:
            return str(round(_time, 2))+" min"
        _time /= 60
        if _time < 24:
            return str(round(_time, 2))+" h"
        _time /= 24
        return str(round(_time, 2))+" j"