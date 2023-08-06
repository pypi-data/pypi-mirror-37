import tkinter as tk
from datetime import datetime
from saust.GUI import ColorizeFunctions
from natsort import natsorted
from saust import Constants
import sys
from io import StringIO
import numpy as np


def _parse_time(time):
    """Parse the given time to mm:ss
    :type time: (datetime.timedelta)

    :return: (string) the given time  parsed as mm:ss
     """
    string_time = " (%02d:%02d) " % (time.seconds % 3600 / 60.0, time.seconds % 60)
    return string_time


class Steps(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        # Frame arguments
        self.parent = parent
        self.controller = controller
        self.unbind_class('Text', '<Double-Button-1>')
        # Variables
        self.time_start = None
        self.text = None
        self.test_steps = 0
        self.test_status = True
        self.test_name_label = None
        self.test_passed = 0
        self.test_failed = 0
        self.test_name_index = 1.0
        self.test_steps_passed = 0
        self.test_steps_failed = 0
        self.search_indexes = []
        self.search_visited = None
        self.time_start = datetime.now()
        self.error_button_state = False
        self.passed_button_state = False
        self.collapsed = False
        self.console = None
        self.console_frame = None
        self.console_label = None
        self.error_line_ref = []

        sys.stdout = self.buffer = StringIO()

        # Frame creation methods
        self._create_option_bar()
        self._create_text_widget()
        self.create_console()
        self.colorize = ColorizeFunctions.ColorizePythonFunctions(self)

    def _create_option_bar(self):
        """
        Create the option bar of the window with it's elements, which contains the hide buttons, the search bar
        and the navigation of the search bar.
        """
        # Create option Bar
        self.option_bar = tk.Frame(self, bg=Constants.dark_color)
        self.option_bar.pack(fill=tk.X)

        # Create option bar elements
        self.passed_button = tk.Checkbutton(self.option_bar,
                                            image=Constants.image_hide_ok,
                                            selectimage=Constants.image_hide_ok_off,
                                            command=self.hide_passed,
                                            font=Constants.text_font(),
                                            indicatoron=False,
                                            bg=Constants.dark_color,
                                            fg="White",
                                            selectcolor=Constants.dark_color)

        self.error_button = tk.Checkbutton(self.option_bar,
                                           image=Constants.image_hide_error,
                                           selectimage=Constants.image_hide_error_off,
                                           command=self.hide_error_message,
                                           font=Constants.text_font(),
                                           indicatoron=False,
                                           bg=Constants.dark_color,
                                           fg="White",
                                           selectcolor=Constants.dark_color)

        self.collapse_button = tk.Checkbutton(self.option_bar,
                                              image=Constants.image_collapse,
                                              selectimage=Constants.image_collapse_off,
                                              command=self.collapse_all,
                                              font=Constants.text_font(),
                                              indicatoron=False,
                                              bg=Constants.dark_color,
                                              fg="White",
                                              selectcolor=Constants.dark_color)

        self.search_bar_frame = tk.Frame(self.option_bar, bg=Constants.dark_color)
        self.search_bar_frame.grid(row=0, column=4)

        self.validator = (self.register(self.search), '%P')

        self.search_bar_label = tk.Label(self.search_bar_frame,
                                         text="Search:",
                                         font=Constants.text_font(),
                                         bg=Constants.dark_color,
                                         fg=Constants.text_color)
        self.search_bar = tk.Entry(self.search_bar_frame,
                                   text="Search",
                                   fg="White",
                                   font=Constants.text_font(),
                                   width=28,
                                   bg=Constants.light_color,
                                   validate="key",
                                   validatecommand=self.validator)

        self.search_next_button = tk.Button(self.search_bar_frame,
                                            text=">",
                                            font=Constants.text_font(),
                                            bd=1,
                                            relief=tk.RIDGE,
                                            overrelief=tk.RIDGE,
                                            fg="White",
                                            bg=Constants.light_color,
                                            command=self.search_next)

        self.search_previous_button = tk.Button(self.search_bar_frame,
                                                text="<",
                                                font=Constants.text_font(),
                                                bd=1,
                                                relief=tk.RIDGE,
                                                overrelief=tk.RIDGE,
                                                fg="White",
                                                bg=Constants.light_color,
                                                command=self.search_previous)

        self.results_label = tk.Label(self.search_bar_frame,
                                      text="",
                                      bg=Constants.dark_color,
                                      fg="White")
        # Grid option bar elements
        self.passed_button.grid(row=0, column=0, pady=5, padx=10)
        self.error_button.grid(row=0, column=1, pady=5, padx=10)
        self.collapse_button.grid(row=0, column=2, pady=5, padx=10)
        # Grid search bar elements
        self.search_bar_label.grid(row=0, column=0, pady=10)
        self.search_bar.grid(row=0, column=1, pady=5)
        self.results_label.grid(row=0, column=2)
        self.search_previous_button.grid(row=0, column=3)
        self.search_next_button.grid(row=0, column=4)
        self.search_previous_button.grid_remove()
        self.search_next_button.grid_remove()

    def create_console(self):
        self.console_frame = tk.Frame(self.panned, bg=Constants.dark_color)

        self.console_label = tk.Label(self.console_frame,
                                      text="Console:",
                                      font=Constants.text_font(size=9),
                                      bg=Constants.dark_color,
                                      fg=Constants.text_color
                                      )

        self.console_label.pack(side="top", anchor="w")
        self.console = tk.Text(self.console_frame, cursor="arrow",
                               bd=0,
                               fg="white",
                               wrap="word",
                               state="disabled",
                               font=Constants.text_font(size=10, family="Courier"),
                               highlightbackground=Constants.dark_color,
                               highlightcolor=Constants.dark_color,
                               highlightthickness=10,
                               bg=Constants.medium_color)

        self.console.pack(expand=1, fill="both", side=tk.BOTTOM)

        self.panned.add(self.console_frame, height=100, minsize=150)

    def get_buffer_value(self):
        return self.buffer.getvalue()

    def write_console(self, text=None):

        self.console.configure(state="normal")
        self.console.delete("1.0", "end")
        if text is not None:
            self.console.insert("end", text)
        else:
            self.console.insert("end", self.buffer.getvalue())
        self.console.configure(state="disabled")
        self.console.see("end")

    def _create_text_widget(self):
        """Creates and configure the text widget in which the data will be writen"""
        # Create Text Widget
        self.panned = tk.PanedWindow(self, bd=0, orient=tk.VERTICAL, bg=Constants.ultra_light_color, handlepad=300)
        self.panned.pack(expand=1, fill="both")

        self.text = tk.Text(self.panned,
                            cursor="arrow",
                            bd=0,
                            fg="white",
                            wrap="word",
                            state="disabled",
                            font=Constants.text_font(),
                            highlightbackground=Constants.dark_color,
                            highlightcolor=Constants.dark_color,
                            highlightthickness=10,
                            bg=Constants.light_color)

        self.panned.add(self.text, sticky="nwes", minsize=400, height=2000)
        self.text.tag_bind("header", "<Double-1>", self._toggle_visibility)

        # Create text widget Scrollbar
        scroll = tk.Scrollbar(self.text, command=self.text.yview)
        scroll.pack(expand=1, anchor="e", fill=tk.Y)
        self.text['yscrollcommand'] = scroll.set

        # Create Tags of the text widget
        self.text.tag_configure("header",
                                font=Constants.text_font(16),
                                background=Constants.medium_color,
                                foreground="white",
                                borderwidth=2,
                                spacing1=8,
                                spacing3=8,
                                relief=tk.RAISED)

        self.text.tag_configure("hidden",
                                elide=True)
        self.text.tag_configure("selected",
                                background="Blue")

        self.text.tag_configure("passed")

        self.text.tag_configure("failed",
                                borderwidth=2,
                                relief=tk.RAISED)
        self.text.tag_configure("collapsed_failed")

        self.text.tag_configure("function",
                                spacing1=5,
                                spacing3=5,
                                font=Constants.text_font(size=10),
                                background=Constants.dark_color)

        self.text.tag_configure("hidden_failed_message",
                                elide=True)

        self.text.tag_configure("failed_message_hover",
                                background=Constants.medium_color)

        self.text.tag_configure("failed_line",
                                background=Constants.error_line,
                                borderwidth=1,
                                relief=tk.RAISED
                                )

        self.text.tag_configure("failed_message",
                                lmargin1=5,
                                lmargin2=5,
                                spacing1=5,
                                spacing3=10,
                                background=Constants.medium_color,
                                font=Constants.text_font(11),
                                relief=tk.GROOVE,
                                borderwidth=3)

        self.text.tag_configure("failed_line",
                                background=Constants.error_line,
                                )

        self.text.tag_configure("passed_header",
                                background=Constants.green_color)
        self.text.tag_configure("failed_header",
                                background=Constants.red_color)

        self.text.tag_configure("step_hover",
                                background=Constants.ultra_light_color)
        self.text.tag_configure("failed_hover",
                                background=Constants.light_red_color)
        self.text.tag_configure("passed_hover",
                                background=Constants.light_green_color)

        self.text.bind("<Leave>", self.remove_hover)

        self.text.tag_bind("passed", "<Motion>", self.step_hover)
        self.text.tag_bind("failed", "<Motion>", self.step_hover)
        self.text.tag_bind("failed_header", "<Motion>", self.failed_header_hover)
        self.text.tag_bind("passed_header", "<Motion>", self.passed_header_hover)
        self.text.tag_bind("failed_message", "<Enter>", self.remove_hover)
        self.text.tag_bind("function", "<Enter>", self.remove_hover)
        self.text.tag_bind("failed", "<Double-1>", self._toggle_visibility)
        self.text.tag_bind("failed_line", "<Double-1>", self.goto_editor_line)

        self.text.tag_lower("passed", "hidden")
        self.text.tag_lower("failed_message", "hidden")
        self.text.tag_raise("step_hover", "passed")
        self.text.tag_raise("failed_hover", "failed_header")
        self.text.tag_raise("step_hover", "failed")
        self.text.tag_raise("selected", "failed_hover")
        self.text.tag_raise("selected", "passed_hover")
        self.text.tag_raise("selected", "failed_header")
        self.text.tag_raise("selected", "passed_header")
        self.text.tag_raise("failed_line", "function")

    #
    # WRITE FUNCTIONS
    #
    def check_time(self, time):
        if time is None:
            # Calculate the elapsed time since the start of the test case
            now = datetime.now() - self.time_start
            time = _parse_time(now)
            return time
        else:
            # Format the given time
            time = " (" + time + ") "
            return time

    def remove_hover(self, event=None):
        self.text.tag_remove("step_hover", "1.0", "end")
        self.text.tag_remove("failed_hover", "1.0", "end")
        self.text.tag_remove("passed_hover", "1.0", "end")
        self.text.tag_remove("failed_message_hover", "1.0", "end")

    def step_hover(self, event=None):
        """Change the color of the line where the mouse is"""

        self.remove_hover()
        index = self.text.index("current")
        self.text.tag_add("step_hover", str(index) + " linestart", str(index) + " lineend + 1 char")

    def failed_header_hover(self, event=None):
        """Change the color of the line where the mouse is"""

        self.remove_hover()
        index = self.text.index("current")
        self.text.tag_add("failed_hover", str(index) + " linestart", str(index) + " lineend + 1 char")

    def passed_header_hover(self, event=None):
        """Change the color of the line where the mouse is"""

        self.remove_hover()
        index = self.text.index("current")
        self.text.tag_add("passed_hover", str(index) + " linestart", str(index) + " lineend + 1 char")

    def failed_message_hover(self, event=None):

        self.remove_hover()
        index = self.text.index("current")
        self.text.tag_add("failed_message_hover", str(index) + " linestart", str(index) + " lineend + 1 char")

    def add_test_case(self, name):
        """Print to the text widget a header and start a new test case

        :type name: (str) the name of the test case
        """
        # Set variables
        self.test_steps = 0
        self.test_status = True
        self.time_start = datetime.now()
        self.test_name_label = name
        self.test_name_index = self.text.index("end") + "-1 lines"

        # Add new test case info
        self.text.image_create(str(self.test_name_index) + "+ 1 char", image=Constants.image_run_test, pady=0)
        self.text.tag_add("header", str(self.test_name_index), str(self.test_name_index) + " lineend")
        self.text.configure(state="normal")
        self.text.insert("end", " " + self.test_name_label + "\n", "header")
        self.text.configure(state="disabled")

        # update run tests button
        self.controller.update_run_button()

        # set the new line visible if it isn't
        self.text.see("end")

    def step_pass(self, message, time=None):
        """Add a successfully executed step of a test case. it displays the time on completion of the step since
        the start of the test case and the description of the step

        :type message: (str) the description of the step
        :type time: (str) the elapsed time since the start of the test case until the execution of the step
        """
        # Check if variable time is assigned else assign it
        time = self.check_time(time)
        # add step info
        self.text.config(state="normal")
        image_index = self.text.index("end") + "-1 lines"
        self.text.image_create("end", image=Constants.image_ok)
        self.text.tag_add("passed", image_index, image_index + "+1 char")
        self.text.insert("end", "%s %s \n" % (time, message), "passed")
        self.text.config(state="disabled")
        # if new line is not visible scroll down until it's visible
        self.text.see("end")
        self.update_all()
        # Increase variables
        self.controller.total_steps += 1
        self.test_steps += 1
        self.test_steps_passed += 1

    def step_fail(self, message, error_message=None, lines=None, error_line=None, time=None, error_line_module=None):
        """Add a failed executed step of a test case. it displays the time on completion of the step since
        the start of the test case, the description of the step and the error message of the step.

        :type message: (str) the description of the step
        :type error_message: (str) the error message of the step
        :type lines: (str) the source code of the function
        :type error_line: (str) the index of line where the error had happened
        :type time: (str) the elapsed time since the start of the test case until the execution of the step
        """
        # set the test case status as failed
        self.test_status = False
        time = self.check_time(time)
        # add step info
        self.text.config(state="normal")
        image_index = self.text.index("end") + "-1 lines"
        self.text.image_create("end", image=Constants.image_fail)

        self.text.tag_add("failed", image_index, image_index + "+1 char")
        current_index = self.text.index("end")
        self.text.insert("end", "%s  %s \n" % (time, message), "failed")
        # if there is no error message print consequently
        if error_message is "":
            error_message = "Without error message"
        if lines is not None:
            self.text.insert("end", lines, "function")
        if error_line is not None:
            error_line_index = float(current_index) + float(error_line) - 1.0
            self.text.tag_add("failed_line",
                              str(error_line_index) + " linestart",
                              str(error_line_index) + " lineend + 1 char")
            ref_index = len(self.error_line_ref)
            self.text.tag_add("error_ref" + str(ref_index),
                              str(error_line_index) + " linestart",
                              str(error_line_index) + " lineend + 1 char")
            self.error_line_ref.append(("error_ref" + str(ref_index), error_line_module))
            self.text.tag_raise("failed_line", "failed_message")
            self.text.tag_raise("failed_line", "function")
        self.text.insert("end ", " Error Message: \n" + error_message + "\n", "failed_message")

        self.text.config(state="disabled")
        # if new line is not visible scroll down until it's visible
        self.text.see("end")
        if self.error_button_state:
            self.hide_error_message(True)

        # Update function colors
        self.update_all()
        # Increase variables
        self.controller.total_steps += 1
        self.test_steps_failed += 1
        self.test_steps += 1

    def test_finish(self):
        """Finish a test case. If any of the test case steps had failed then tags the test case as failed. Otherwise
        tag the test case as passed."""
        if self.test_status:
            # Change the header of the test case
            self.text.configure(state="normal")

            self.text.delete(str(self.test_name_index),
                             str(self.test_name_index) + "+1 chars")

            self.text.insert(self.test_name_index,
                             " ", "header")
            self.text.image_create(str(self.test_name_index) + "+ 1 char",
                                   image=Constants.image_ok,
                                   pady=0)
            self.text.tag_add("passed",
                              str(self.test_name_index),
                              str(self.test_name_index) + " lineend + 1 char")

            self.text.tag_add("passed_header",
                              str(self.test_name_index),
                              str(self.test_name_index) + " lineend + 1 char")

            self.text.configure(state="disabled")
            # increase the variable
            self.controller.test_passed += 1
        else:
            # Change the header of the test case
            self.text.configure(state="normal")

            self.text.delete(str(self.test_name_index),
                             str(self.test_name_index) + "+1 chars")

            self.text.insert(str(self.test_name_index),
                             " ", "header")

            self.text.image_create(str(self.test_name_index) + "+ 1 char",
                                   image=Constants.image_fail,
                                   pady=0)

            self.text.tag_add("failed_header",
                              str(self.test_name_index),
                              str(self.test_name_index) + " lineend + 1 char")

            self.text.configure(state="disabled")
            # increase the variable
            self.controller.test_failed += 1

        # store the test case results
        self.controller.data_tests.append([self.test_steps_passed, self.test_steps_failed])
        # reset the steps variables
        self.test_steps_passed = 0
        self.test_steps_failed = 0

    #
    # UTILITY FUNCTIONS
    #

    def update_all(self):
        self.colorize.update_color()
        if self.controller.loaded_xml is False:
            self.write_console()

    def clear_text(self):
        self.text.configure(state="normal")
        self.text.delete("1.0", "end")
        self.text.configure(state="disabled")

    def search(self, search_value=None):
        """Search in the text widget if there are any coincidences to the given value. If they are then select
        the coincidences.

        :type search_value: (str) the value to be searched"""
        # init variables
        if search_value is None:
            search_value = self.search_bar.get()
        self.search_indexes = []
        search_index = "1.0"
        # remove all previous searched coincidence
        self.text.tag_remove("selected", "1.0", "end")
        # raise selected tag in order to be shown
        self.text.tag_raise("selected", "failed_message")
        self.text.tag_raise("selected", "failed_hover")
        self.text.tag_raise("selected", "passed_hover")
        self.text.tag_raise("selected", "failed_header")
        self.text.tag_raise("selected", "passed_header")
        self.text.tag_raise("selected", "step_hover")
        self.text.tag_raise("selected", "function")
        self.text.tag_raise("selected", "failed_line")
        # if none value is searched don't search
        if search_value == "":
            self.results_label.configure(text="")
            # hide navigation search bar buttons
            self.search_next_button.grid_remove()
            self.search_previous_button.grid_remove()
            return True
        # while the search hasn't get to the end of the text, search for the value and store the coincidences index
        while search_index != "+ 1 char":
            # search the value starting at 'search index' and returns the index if there is a coincidence
            search_index = self.text.search(search_value, search_index, "end", nocase=1)
            if search_index != "":
                # if the index is not empty store it
                self.search_indexes.append(search_index)

            # set the search_index to the current coincidence plus 1 character
            search_index = search_index + "+ 1 char"
        # tag the coincidences of the search as selected
        for elem in self.search_indexes:
            self.text.tag_add("selected", str(elem), str(elem) + " +" + str(len(search_value)) + "char")
        # show the navigation bar if necessary
        self.show_navigation_search_bar()
        return True

    def show_navigation_search_bar(self):
        """If there is any coincidence in a search then show the navigation of the search bar"""
        # make the first coincidences as the current
        self.search_visited = 1
        # if there is any coincidence show the results and show the navigation search bar buttons
        if len(self.search_indexes) > 0:
            self.results_label.configure(text="%s of %s results" % (str(self.search_visited), len(self.search_indexes)))
            self.text.see(self.search_indexes[0])
            self.search_next_button.grid()
            self.search_previous_button.grid()
        # else hide the navigation search bar buttons if they were shown
        else:
            self.search_next_button.grid_remove()
            self.search_previous_button.grid_remove()
            self.results_label.configure(text=" No results")

    def search_next(self):
        """Scroll to the next searched coincidence of the text widget"""
        self.text.tag_raise("selected", "function")
        next_index = self.search_visited
        # check that the next index is inside the list
        if next_index < len(self.search_indexes):
            self.text.see(self.search_indexes[next_index])
            self.search_visited += 1
            self.results_label.configure(text="%s of %s results" % (str(self.search_visited), len(self.search_indexes)))

    def search_previous(self):
        """Scroll to the previous searched coincidence of the text widget"""
        previous_index = self.search_visited - 2
        # check that the previous_index is in range
        if previous_index >= 0:
            # scroll to the previous index
            self.text.see(self.search_indexes[previous_index])
            self.search_visited -= 1
            # change the text to display the right index
            self.results_label.configure(text="%s of %s results" % (str(self.search_visited), len(self.search_indexes)))

    def collapse_all(self):
        """ If steps are collapsed then show all collapsed text, Otherwise collapse all steps"""
        # Show all collapsed steps
        self.text.tag_remove("hidden", "1.0", "end")
        # If was collapsed then do nothing more
        if self.collapsed:
            self.collapsed = False
        # if wasn't collapsed then collapse all
        else:
            index = 1.0
            # for the number of test case there are
            for _ in self.controller.data_tests:
                # collapse the given test case
                self._toggle_visibility(position=str(index))
                # get the start index of the next test case that is the end index of the current test case
                next_range = self._get_block(str(index))
                index = float(next_range[1])
            # Set the variable
            self.collapsed = True
        self.search()

    def hide_error_message(self, override=False):
        self.text.tag_remove("hidden_failed_message", "1.0", "end")
        # If was collapsed then do nothing more
        if self.error_button_state and override is False:
            self.error_button_state = False
            self.search()
            self.colorize.update_color()
            return
        # if wasn't collapsed then collapse all
        else:
            try:
                index, end = self.text.tag_nextrange("failed", "1.0", "end")
            except Exception:
                self.error_button_state = True
                self.search()
                self.colorize.update_color()
                return
            # for the number of steps there are
            for _ in range(self.controller.total_steps):
                # collapse the given test case

                next_range = self.text.tag_nextrange("failed", index, "end")

                if next_range is not ():
                    self._toggle_visibility(position=str(next_range[0]),
                                            tag="hidden_failed_message",
                                            current_tag="failed")
                    # get the start index of the next test case that is the end index of the current test case
                    end = self._get_block(str(next_range[0]), tag="failed")
                    index = end[1]
            # Set the variable
            if not override:
                self.error_button_state = True
        self.search()
        self.update_all()

    def hide_passed(self):
        """Hide all the passed steps of the text widget if they are visible.
         If they are not visible then set all the passed steps visible
         """
        if self.passed_button_state is False:
            self.passed_button_state = True
            self.text.tag_configure("passed", elide=True)
        else:
            self.passed_button_state = False
            self.text.tag_configure("passed", elide=False)

    def _toggle_visibility(self, event=None, position="insert", tag="hidden", current_tag="header"):
        """ hide or show the steps of the 'selected' test case """
        if event is not None:
            tags = self.text.tag_names(position)
            for elem_tag in tags:
                if elem_tag == "failed":
                    current_tag = "failed"
                    tag = "hidden_failed_message"

        # get the block start and end of the 'elected' test case
        block_start, block_end = self._get_block(position, current_tag)
        # get if the block is hidden or not
        next_hidden = self.text.tag_nextrange(tag, block_start, block_end)
        if next_hidden:
            # make the block visible again
            self.text.tag_remove(tag, block_start, block_end)
        else:
            # hide the block
            self.text.tag_add(tag, block_start, block_end)
        self.search(self.search_bar.get())
        self.colorize.update_color()

    def _get_block(self, index, tag="header"):
        """return indices after header, to next header or EOF

        :type index: (str) the index of start of the block

        :returns: (str) the index of start of the block
                  (str) the index of end of the block
        """

        start = self.text.index("%s lineend+1c" % index)
        if tag == "failed":
            next_passed = self.text.tag_nextrange("passed", start)
            next_failed = self.text.tag_nextrange("failed", start)
            next_header = self.text.tag_nextrange("header", start)
            end = (self.text.index("end"), self.text.index("end"))

            next_tags = [next_passed, next_failed, next_header, end]
            next_tags = [x for x in next_tags if x is not ()]
            next_tags = natsorted(next_tags, key=lambda x: x[0])
            if next_tags[0][0] == end[0]:
                return start, next_tags[0][0] + "-1 char"
            return start, next_tags[0][0]

        next_header = self.text.tag_nextrange(tag, start)

        if next_header:
            end = next_header[0]
        else:
            end = self.text.index("end")
        return start, end

    def goto_editor_line(self, event=None):

        self.controller.show_frame("Editor")
        editor = self.controller.get_frame("Editor")
        error_ref = [elem for elem in self.text.tag_names("insert") if "error_ref" in elem]
        for element in self.error_line_ref:
            if element[0] == error_ref[0]:
                index = element[1] + ".0"
                editor.text.tag_remove("selected", "1.0", "end")
                lines = np.round(self.parent.winfo_height()/100, 0)
                index_centered = float(index) + float(lines)
                editor.text.see(index_centered)
                editor.text.tag_add("selected", index + " linestart", index + " lineend + 1 char")
                editor.text.tag_raise("selected", "function")
        self.write_console()
