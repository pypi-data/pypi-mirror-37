import tkinter as tk
from saust import Constants


class DataTable(tk.Frame):

    def __init__(self, parent, controller, data=None):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        self.data = data
        self.configure(bg=Constants.dark_color)

        self.index_row = 1
        self.index_column = 2
        self.rowconfigure(0, minsize=40)

        for i in range(7):
            self.columnconfigure(i, weight=1)

    def set_data(self, data):
        self.data = data

    def update_all(self):
        self.create_title_row()
        self.create_row()

    def create_title_row(self):
        label_passed_steps = tk.Label(self,
                                      text="Passed Steps",
                                      font=Constants.text_font(),
                                      fg=Constants.text_color,
                                      bg=Constants.medium_color,
                                      bd=10)

        label_failed_steps = tk.Label(self,
                                      text="Failed steps",
                                      font=Constants.text_font(),
                                      fg=Constants.text_color,
                                      bg=Constants.medium_color,
                                      bd=10)

        label_total_steps = tk.Label(self,
                                     text="Total steps",
                                     font=Constants.text_font(),
                                     fg=Constants.text_color,
                                     bg=Constants.medium_color,
                                     bd=10)

        label_percentage_steps = tk.Label(self,
                                          text="% steps",
                                          font=Constants.text_font(),
                                          fg=Constants.text_color,
                                          bg=Constants.medium_color,
                                          bd=10)

        label_passed_steps.grid(row=self.index_row,
                                column=self.index_column,
                                sticky="nwes",
                                padx=1, pady=1)

        label_failed_steps.grid(row=self.index_row,
                                column=self.index_column + 1,
                                sticky="nwes",
                                padx=1, pady=1)

        label_total_steps.grid(row=self.index_row,
                               column=self.index_column + 2,
                               sticky="nwes",
                               padx=1, pady=1)

        label_percentage_steps.grid(row=self.index_row,
                                    column=self.index_column + 3,
                                    sticky="nwes",
                                    padx=1, pady=1)

    def create_row(self):
        for i in range(self.data.get_number_of_test_case()):
            test_d = self.data.get_test_case_by_order(i)

            for j in range(test_d.get_number_of_steps()):
                step = test_d.get_step_by_order(j + 1)

        for i in range(self.data.get_number_of_test_case()):
            test_d = self.data.get_test_case_by_order(i)
            status = test_d.get_status()
            if status == "pass":
                color = Constants.green_color
            else:
                color = Constants.red_color

            label = tk.Label(self,
                             text=str(test_d.get_name()),
                             font=Constants.text_font(),
                             fg=Constants.text_color,
                             bg=color,
                             bd=10
                             )

            label.grid(row=self.index_row + i + 1,
                       column=self.index_column - 1,
                       sticky="nwes",
                       padx=1, pady=1)

            label_passed = tk.Label(self,
                                    text=str(test_d.get_passed_steps()),
                                    font=Constants.text_font(),
                                    fg=Constants.text_color,
                                    bg=Constants.ultra_light_color,
                                    bd=10
                                    )

            label_passed.grid(row=self.index_row + i + 1,
                              column=self.index_column,
                              sticky="nwes",
                              padx=1, pady=1)

            label_failed = tk.Label(self,
                                    text=str(test_d.get_failed_steps()),
                                    font=Constants.text_font(),
                                    fg=Constants.text_color,
                                    bg=Constants.ultra_light_color,
                                    bd=10
                                    )

            label_failed.grid(row=self.index_row + i + 1,
                              column=self.index_column + 1,
                              sticky="nwes",
                              padx=1, pady=1)

            label_total = tk.Label(self,
                                   text=str(test_d.get_total_steps()),
                                   font=Constants.text_font(),
                                   fg=Constants.text_color,
                                   bg=Constants.ultra_light_color,
                                   bd=10
                                   )

            label_total.grid(row=self.index_row + i + 1,
                             column=self.index_column + 2,
                             sticky="nwes",
                             padx=1, pady=1)

            label_percentage = tk.Label(self,
                                        text=str(test_d.get_passed_percentage(1)) + "%",
                                        font=Constants.text_font(),
                                        fg=Constants.text_color,
                                        bg=Constants.ultra_light_color,
                                        bd=10
                                        )

            label_percentage.grid(row=self.index_row + i + 1,
                                  column=self.index_column + 3,
                                  sticky="nwes",
                                  padx=1, pady=1)
