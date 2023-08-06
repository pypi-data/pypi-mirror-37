import inspect
import threading
from datetime import datetime
from defusedxml.lxml import _etree as et
from saust import TestCase
from saust.Tools import TestData
import sys
import traceback


def _get_class_methods(cls):
    """Get a class as an argument and return a list of it's methods that the method name start with the word 'test'.
     The list is sorted by its line position in the module file
     :type cls: (class)

     :return: (list) of 2 dimension elements:   first element is the method name,
                                                second element is line position of the element
     """
    # Initialize a array to store methods
    methods = []
    # Get all the methods of 'cls' (class)
    cls_methods = dir(cls)
    # start a loop to check if a method is a 'test_method'
    for method in cls_methods:
        # check if the method name starts with 'test'
        if method[0:4] == "test":
            # get a reference to the method
            func = getattr(cls, method)
            # get the line position of the method in it's module file
            position = inspect.findsource(func)[1]
            # add the method and its line position to the list 'methods
            methods.append([method, position])
    # sort the methods by the line position
    methods.sort(key=lambda x: x[1])
    return methods


def _add_step_xml(parent, step_order):
    """Add a step sub element with an attribute order to the given parent
    :type parent: (ElementTree)
    :type step_order: (int)

    :return: (ElementTree) the element which has been added
    """
    element = et.SubElement(parent, "step", {"order": str(step_order)})
    return element


def _add_step_time_xml(step, time):
    """Add a time sub element with it's value to the given step
    :type step: (ElementTree)
    :type time: (String)

    :return: (ElementTree) the element which has been added
    """
    element = et.SubElement(step, "time")
    element.text = time
    return element


def _add_step_description(step, description):
    """Add a description sub element with it's value to the given step
    :type step: (ElementTree)
    :type description: (String)

    :return: (ElementTree) the element which has been added
    """
    element = et.SubElement(step, "description")
    element.text = description
    return element


def _add_step_status(step, status):
    """Add a status sub element with it's value to the given step
    :type step: (ElementTree)
    :type status: (String)

    :return: (ElementTree) the element which has been added
    """
    element = et.SubElement(step, "status")
    element.text = status
    return element


def _add_step_error(error):
    """Add a error sub element with it's value to the given step
    :type error: (ElementTree)

    :return: (ElementTree) the element which has been added
    """
    element = et.SubElement(error, "error")
    return element


def _add_error_function(error, func):
    """Add a error sub element with it's value to the given step
       :type error: (ElementTree)
       :type func: (String)

       :return: (ElementTree) the element which has been added
       """
    element = et.SubElement(error, "function")
    element.text = func
    return element


def _add_error_line(error, line):
    """Add a error sub element with it's value to the given step
       :type error: (ElementTree)
       :type line: (String)

       :return: (ElementTree) the element which has been added
       """
    element = et.SubElement(error, "line")
    element.text = line
    return element


def _add_error_message(error, message):
    """Add a error sub element with it's value to the given step
       :type error: (ElementTree)
       :type message: (String)

       :return: (ElementTree) the element which has been added
       """
    element = et.SubElement(error, "message")
    element.text = message
    return element


def _get_datetime():
    """Get the current date time and parse it to YYYY-MM-DD_hh-mm

    :return: (string) the current time parsed as YYYY-MM-DD_hh-mm"""
    time = str(datetime.now())
    return time[:10] + "_" + time[11:13] + "-" + time[14:16]


def _parse_time(time):
    """Parse the given time to mm:ss
    :type time: (datetime.timedelta)

    :return: (string) the given time  parsed as mm:ss
    """
    string_time = "%02d:%02d" % (time.seconds % 3600 / 60.0, time.seconds % 60)
    return string_time


class Process(threading.Thread):
    """Read and execute the TestCase and and the results in a Queue in order to transfer the data to the main Thread and
    save the data to a XML file"""
    def __init__(self, steps, queue, module):
        threading.Thread.__init__(self, None, self.do)
        # assign the arguments
        self.queue = queue
        self._test = steps
        self._module = module
        # create empty data
        self._run_methods = []
        self._modules_classes = []
        self.cls = None
        self.time_start = datetime.now()
        self.data = TestData.TestRunData()
        # create a XML element that will serve as a root
        self.xml = et.Element("test_run")

    def do(self):
        """Execute all functions of this class to perform is task"""
        # clear the list if they aren't empty
        self._run_methods = []
        self._modules_classes = []
        # get the classes of the module that are subclasses of TestCase
        self._process_module_classes(self._module)
        # execute the methods, evaluate its execution and store its result in a Queue
        self.new_execute_methods()
        # Send the signal that the task has finished
        self.queue.put(["finish_thread", self.xml, self.data])
        # delete the object
        del self

    def _process_module_classes(self, module):
        """Get all the the classes that are subclasses of 'TestCase' of a given module
        and store them in a list named'_module_classes'

        :type module: (module) the module which will be run"""
        for element in inspect.getmembers(module):
            # check the object is a class
            obj = element[1]
            if inspect.isclass(obj):
                # check the class is a subclass of 'TestCase'
                if issubclass(obj, TestCase.TestCase):
                    position = inspect.findsource(obj)[1]
                    self._modules_classes.append([obj, position])
        self._modules_classes.sort(key=lambda x: x[1])

    # noinspection PyBroadException

    def new_execute_methods(self):
        """Execute all the test case methods, send the results data to the Queue and save the data to a XML file"""

        # Get the total number of test case to run
        n_test_case = len(self._modules_classes)
        # Send the number of test case to the Queue
        self.queue.put(["n_test_case", n_test_case])
        # do a loop with one iteration per test case
        for i in range(n_test_case):
            # initialize the class of the test case
            try:
                cls = self._modules_classes[i][0]()
            except Exception:
                # If and error during loading the class of test case, then jump to the next test case
                self.error_message()
                continue
            # get the Start Time of the test case
            self.time_start = datetime.now()
            # Reset the step order variable
            step_order = 1
            # get the name of the test case
            cls_name = cls.get_name()
            # if there is no name of test case assign a name of 'Test' plus the test case order number
            if cls_name is None:
                cls_name = "Test " + str(i+1)
            # Send the signal of a start of a test case to the Queue
            self.queue.put(["start", cls_name])
            # Add a test case element to the XML file
            parent_xml = self._add_test_xml(cls_name)
            # call a function that returns a list of all test_methods of the class and it's line position
            class_methods = _get_class_methods(cls)

            test_case_data = self.data.add_test_case(cls_name, i)
            # do a loop with one iteration per test method of the test case
            for method in class_methods:
                # get the reference to the method
                func = cls.__getattribute__(method[0])
                # get the __doc__ description of the method
                description = inspect.getdoc(func)
                # get the source lines of the method
                lines = inspect.getsource(func)
                # set the variable that stores the line where a function fails to None
                function_error_line = None
                # If there is no description of the test assign a default description
                if description is None:
                    description = "There is no description of this step"

                # try execute the method
                try:
                    func()
                # If fail get the exception info, send the info and save it to XML

                except Exception as e:
                    # get the end time of the step
                    now = datetime.now() - self.time_start
                    elapsed_time = _parse_time(now)

                    # Create a list to store the exception info
                    trace = []
                    # get the exception info
                    exc_type, exc_value, exc_traceback = sys.exc_info()
                    # try extract the exception info and get the line where the exception happened
                    try:
                        # Create a TracebackException object and store all the data to the list
                        for line in traceback.TracebackException(
                                type(exc_value), exc_value, exc_traceback, limit=None).format(chain=True):
                                trace.append(line)
                        # get the string that contains the data of where the exception happened
                        error_string = trace[2]
                        # get the index start and end position of the line number on the string
                        error_string_index = error_string.find(", line")
                        error_string_index_end = error_string.find(",", error_string_index + 1)
                        # get the line number
                        error_line = error_string[error_string_index + 7:error_string_index_end]
                        # get the line number of the error within the function
                        function_error_line = float(error_line) - float(method[1])
                    except Exception:
                        self.error_message()
                    # for safety reasons delete the objects of the exception
                    del exc_type, exc_value, exc_traceback, trace

                    # Send all the data to the Queue
                    test_case_data.add_step(step_order,
                                            description=description,
                                            status="fail",
                                            time=elapsed_time,
                                            method=lines,
                                            error_message=str(e),
                                            error_line=str(function_error_line),
                                            error_line_module=str(error_line),
                                            )
                    self.queue.put(["fail", description, str(e), function_error_line, str(lines), str(error_line)])

                    # Create a step element of XML
                    step = _add_step_xml(parent_xml, step_order)
                    # Add all info to the step element
                    _add_step_status(step, "failed")
                    _add_step_time_xml(step, elapsed_time)
                    _add_step_description(step, description)
                    error = _add_step_error(step)
                    _add_error_function(error, lines)
                    _add_error_line(error, str(function_error_line))
                    if str(e) == "":
                        _add_error_message(error, "There is no error message")
                    else:
                        _add_error_message(error, str(e))
                    # Increase the step order variable
                    step_order += 1

                else:
                    # Get the end time of the step
                    now = datetime.now() - self.time_start
                    elapsed_time = _parse_time(now)
                    # Send the info to the Queue
                    test_case_data.add_step(step_order, description=description, status="pass",time=elapsed_time,method=lines)
                    self.queue.put(["pass", description])
                    # Create a step element of XML
                    step = _add_step_xml(parent_xml, step_order)
                    # Add all info to the step element
                    _add_step_status(step, "passed")
                    _add_step_time_xml(step, elapsed_time)
                    _add_step_description(step, description)
                    _add_step_error(step)
                    # Increase the step order variable
                    step_order += 1
            # Send the signal to the Queue that the test case has finished
            self.queue.put(["end", cls.get_name()])

    def _add_test_xml(self, name):
        """Create a XML sub element of 'test_run' with the tag'testcase' and with the attribute 'name' which contains
        the test case name

        :return: (ElementTree) the element which has been created"""
        parent = et.SubElement(self.xml, "testcase", {"name": name})
        return parent

    def _save_xml(self):
        """Create a string of the XML element 'test_run' with a pretty format (indented and with end lines)
        that later is writen in a XML file

        :return: None"""
        # Converts to string the 'xml' Element to string
        xml_string = et.tostring(self.xml, encoding='UTF-8', xml_declaration=True, pretty_print=True)
        # Replace the end of line with end of line that some programs can understand
        xml_string.replace(b'\n', b'\r\n')
        # Create a string with the name of the file
        xml_name = "test_history/" + _get_datetime() + ".xml"
        # Create and write the XML data to the file
        with open(xml_name, "wb") as f:
            f.write(xml_string)
            f.close()
        # Add the filename to the Queue in order to be read by the main thread
        self.queue.put(["xml_name", xml_name])

    def get_modules_classes(self):
        """:return: the 'modules_classes'"""
        return self._modules_classes

    def get_run_methods(self):
        """:return: the 'run_methods'"""
        return self._run_methods

    def error_message(self):
        pass