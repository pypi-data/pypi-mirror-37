import tkinter as tk
from saust import Constants
from saust.GUI import ColorizeFunctions


class Editor(tk.Frame):

    def __init__(self, parent, controller):

        tk.Frame.__init__(self, parent)
        self.configure(bg=Constants.dark_color)
        self.controller = controller
        self.save_changes_label = tk.Label(self, text="hola",
                                           font=Constants.text_font(),
                                           fg=Constants.text_color,
                                           bg=Constants.dark_color)
        self.save_changes_label.pack(anchor="w")
        self.text = tk.Text(self,
                            cursor="arrow",
                            bd=0,
                            fg="white",
                            wrap="word",
                            font=Constants.text_font(),
                            highlightbackground=Constants.dark_color,
                            highlightcolor=Constants.dark_color,
                            highlightthickness=10,
                            bg=Constants.medium_color)

        self.text.tag_configure("selected", background=Constants.red_color)
        self.text.tag_configure("function")
        self.text.tag_raise("selected", "function")
        self.text.pack(expand=1, fill="both")
        self.text.bind("<Key>", self.update_all)
        self.text.bind("<KeyRelease>", self.update_all)
        self.colorize = ColorizeFunctions.ColorizePythonFunctions(self)

    def update_all(self, event=None):
        self.text.tag_add("function", "1.0", "end")
        self.colorize.update_color()
        try:
            with open(self.controller.run_module_path, "w") as f:
                code_to_write = self.text.get("1.0", "end")
                f.write(code_to_write)
                f.close()
                self.save_changes_label.configure(text="changes saved")
        except Exception:
            self.save_changes_label.configure(text="error")


    def update_text(self, text):
        self.text.delete("1.0", "end")
        self.text.insert("end", text, "function")
        self.update_all()