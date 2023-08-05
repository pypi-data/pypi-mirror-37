import sys
import os
import pkgutil
import textwrap
import traceback
from collections import OrderedDict
from os import path
from queue import Empty
from queue import Queue
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import QObject, QThread, pyqtSignal
from pubsub import pub
import fixate.config
from fixate.config import RESOURCES
from fixate.core.exceptions import UserInputError, SequenceAbort
from . import layout

wrapper = textwrap.TextWrapper(width=75)
wrapper.break_long_words = False

wrapper.drop_whitespace = True

QT_GUI_WORKING_INDICATOR = path.join(path.dirname(__file__), 'working_indicator.gif')

ERROR_STYLE = """
QProgressBar{
    padding: 1px;
    margin-right: 32px;
}
QProgressBar::chunk{
    background-color: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1,
                                      stop: 0 #f3baba, stop: 0.6 #d30505);
    margin: 0px;
    width: 1px;
}"""

STATUS_PRIORITY = OrderedDict(
    [("In Progress", (QtGui.QBrush(QtGui.QColor(255, 255, 128)), QtGui.QBrush(QtGui.QColor(0, 0, 0)))),
     ("Error", (QtGui.QBrush(QtGui.QColor(255, 0, 0)), QtGui.QBrush(QtGui.QColor(255, 255, 255)))),
     ("Failed", (QtGui.QBrush(QtGui.QColor(255, 0, 0)), QtGui.QBrush(QtGui.QColor(255, 255, 255)))),
     ("Aborted", (QtGui.QBrush(QtGui.QColor(128, 128, 128)), QtGui.QBrush(QtGui.QColor(255, 255, 255)))),
     ("Passed", (QtGui.QBrush(QtGui.QColor(0, 255, 0)), QtGui.QBrush(QtGui.QColor(0, 0, 0)))),
     ("Skipped", (QtGui.QBrush(QtGui.QColor(90, 255, 255)), QtGui.QBrush(QtGui.QColor(0, 0, 0))))])


def get_status_colours(status):
    return STATUS_PRIORITY[status]


def exception_hook(exctype, value, traceback):  # TODO DEBUG REMOVE
    # logger.error("{}:{}:{}".format(exctype, value, traceback))
    sys.__excepthook__(exctype, value, traceback)
    sys.exit(1)


class SequencerThread(QObject):
    def __init__(self, worker):
        super(QObject, self).__init__()
        self.worker = worker

    def run_thread(self):
        pub.sendMessage('Finish', code=self.worker.ui_run())


class FixateGUI(QtWidgets.QMainWindow, layout.Ui_FixateUI):
    input_signal = pyqtSignal(str, tuple)
    output_signal = pyqtSignal(str, str)
    label_update = pyqtSignal(str, str)
    update_image = pyqtSignal(str, bool)
    text_signal = pyqtSignal(str)
    timer_signal = pyqtSignal()
    tree_init = pyqtSignal(list)
    tree_update = pyqtSignal(str, str)

    working = pyqtSignal()
    progress = pyqtSignal()
    finish = pyqtSignal()

    """Class Constructor and destructor"""

    def __init__(self, worker, application):
        super(FixateGUI, self).__init__(None)
        self.application = application
        self.register_events()
        self.setupUi(self)
        self.treeSet = False
        self.blocked = False
        self.closing = False

        # Extra GUI setup not supported in the designer
        self.TestTree.setColumnWidth(1, 90)
        self.TestTree.header().setSectionResizeMode(0, QtWidgets.QHeaderView.Stretch)
        self.TestTree.header().setSectionResizeMode(1, QtWidgets.QHeaderView.Fixed)

        self.base_image = ""
        self.dialog = None
        self.image_scene = QtWidgets.QGraphicsScene()
        self.ImageView.set_scene(self.image_scene)
        self.ImageView.setScene(self.image_scene)

        self.working_indicator = QtGui.QMovie(QT_GUI_WORKING_INDICATOR)
        self.WorkingIndicator.setMovie(self.working_indicator)
        self.start_indicator()

        self.status_code = -1  # Default status code used to check for unusual exit
        self.input_queue = Queue()
        self.abort_timer = QtCore.QTimer(self)
        self.fail_queue = None
        self.abort_queue = None
        self.worker = SequencerThread(worker)
        self.worker_thread = QThread()
        self.worker.moveToThread(self.worker_thread)

        self.worker_thread.started.connect(self.worker.run_thread)

        self.finish.connect(self.clean_up)  # Normal termination

        self.Button_1.clicked.connect(self.button_1_click)
        self.Button_2.clicked.connect(self.button_2_click)
        self.Button_3.clicked.connect(self.button_3_click)
        self.UserInputBox.submit.connect(self.text_input_submit)

        self.abort_timer.timeout.connect(self.abort_check)
        self.input_signal.connect(self.get_input)
        self.output_signal.connect(self.display_output)
        self.label_update.connect(self.display_test)
        self.update_image.connect(self.display_image)
        self.text_signal.connect(self.open_text_input)
        self.timer_signal.connect(self.start_timer)
        self.tree_init.connect(self.display_tree)
        self.tree_update.connect(self.update_tree)
        self.progress.connect(self.progress_update)
        self.working.connect(self.start_indicator)

        sys.excepthook = exception_hook  # TODO DEBUG REMOVE

    def run_sequencer(self):
        self.worker_thread.start()

    def closeEvent(self, event):
        """ This function overrides closeEvent from the MainWindow class, called in case of unusual termination"""

        event.ignore()
        self.hide()
        self.clean_up()

    """Pubsub handlers for setup and teardown
       These are run in the main thread"""

    def register_events(self):
        pub.subscribe(self._print_test_start, 'Test_Start')
        pub.subscribe(self._print_test_seq_start, 'TestList_Start')
        pub.subscribe(self._print_test_complete, 'Test_Complete')
        pub.subscribe(self._print_comparisons, 'Check')
        pub.subscribe(self._print_errors, "Test_Exception")
        pub.subscribe(self._print_sequence_end, "Sequence_Complete")
        pub.subscribe(self._seq_abort, "Sequence_Abort")
        pub.subscribe(self._image, 'UI_image')
        pub.subscribe(self._user_ok, 'UI_req')
        pub.subscribe(self._user_choices, "UI_req_choices")
        pub.subscribe(self._user_input, 'UI_req_input')
        pub.subscribe(self._user_display, 'UI_display')
        pub.subscribe(self._user_display_important, "UI_display_important")
        pub.subscribe(self._print_test_skip, 'Test_Skip')
        pub.subscribe(self._print_test_retry, 'Test_Retry')
        pub.subscribe(self._user_action, 'UI_action')
        pub.subscribe(self._completion_code, 'Finish')
        return

    def unregister_events(self):
        pub.unsubAll()
        return

    """Slot handlers for thread-gui interaction
       These are run in the main thread"""

    def start_timer(self):
        self.abort_timer.start(100)

    def abort_check(self):
        if self.abort_queue is None:
            return
        try:
            self.abort_queue.get_nowait()
            self.abort_queue = None
            self.button_reset(True)
            self.abort_timer.stop()
        except Empty:
            return

    def open_text_input(self, message):
        self.ActiveEvent.append(message)
        self.ActiveEvent.verticalScrollBar().setValue(self.ActiveEvent.verticalScrollBar().maximum())
        self.Events.append(message)
        self.Events.verticalScrollBar().setValue(self.Events.verticalScrollBar().maximum())
        self.working_indicator.stop()
        self.WorkingIndicator.hide()
        self.UserInputBox.setPlaceholderText("Input:")
        self.UserInputBox.setEnabled(True)
        self.UserInputBox.setFocus()

    def start_indicator(self):
        self.WorkingIndicator.show()
        self.working_indicator.start()

    def retrieve_packaged_data(self, path):
        try:
            return pkgutil.get_data("module.loaded_tests", path)
        except FileNotFoundError:
            return b""

    def display_image(self, path="", overlay=False):
        if path == "" or not overlay:
            self.image_scene.clear()
            if overlay:
                image = QtGui.QPixmap()
                image.loadFromData(self.base_image)
                if image.isNull():
                    self.file_not_found(self.base_image)
            elif path == "":
                self.base_image = path
                return
            else:
                self.base_image = self.retrieve_packaged_data(path)
                image = QtGui.QPixmap()
                image.loadFromData(self.base_image)
                if image.isNull():
                    self.file_not_found(path)
            self.image_scene.addPixmap(image)
            self.ImageView.fitInView(0, 0, self.image_scene.width(), self.image_scene.height(),
                                     QtCore.Qt.KeepAspectRatio)
            return
        image = QtGui.QPixmap()
        image.loadFromData(self.retrieve_packaged_data(path))
        if image.isNull():
            self.file_not_found(path)
        self.image_scene.addPixmap(image)
        self.ImageView.fitInView(0, 0, self.image_scene.width(), self.image_scene.height(), QtCore.Qt.KeepAspectRatio)
        return

    def file_not_found(self, path):
        """
        Display warning box for an invalid image path
        :param path:
        :return:
        """

        self.dialog = QtWidgets.QMessageBox()
        self.dialog.setText("Warning: Image not Found")
        self.dialog.setInformativeText("Filename: {}".format(path))
        self.dialog.setStandardButtons(QtWidgets.QMessageBox.Ok)
        self.dialog.setDefaultButton(QtWidgets.QMessageBox.Ok)
        self.dialog.setIcon(QtWidgets.QMessageBox.Warning)
        self.dialog.exec()

    def display_tree(self, tree):

        # Make sure this function is only run once
        if self.treeSet:
            return
        self.treeSet = True

        level_stack = []
        for item in tree:
            # Check Level
            if item[0].count('.') + 1 <= len(level_stack):  # Case 1: Going out one or more levels or same level
                for _ in range(len(level_stack) - item[0].count('.')):
                    level_stack.pop()
            elif item[0].count('.') + 1 > len(level_stack):  # Case 2: Going in one or more levels
                for index in range(item[0].count('.') + 1 - len(level_stack), 0, -1):
                    split_index = item[0].split('.')
                    if index > 1:  # More than one level, append dummy items as required
                        dummy = QtWidgets.QTreeWidgetItem()
                        dummy.setText(0, '.'.join(split_index[:-(index - 1)]))
                        dummy.setText(1, 'Queued')
                        dummy.setTextAlignment(1, QtCore.Qt.AlignRight)
                        level_stack.append(dummy.clone())

            tree_item = QtWidgets.QTreeWidgetItem()
            tree_item.setText(0, item[0] + '. ' + item[1])
            tree_item.setTextAlignment(1, QtCore.Qt.AlignRight)
            tree_item.setText(1, 'Queued')

            level_stack.append(tree_item.clone())
            if len(level_stack) > 1:  # Child Add
                level_stack[-2].addChild(level_stack[-1])
            else:  # Top Level
                self.TestTree.addTopLevelItem(level_stack[-1])

    def update_tree(self, test_index, status):

        if len(test_index) == 0:
            return

        colours = get_status_colours(status)
        test_index = test_index.split('.')

        #   Find the test in the tree
        current_test = self.TestTree.findItems(test_index[0], QtCore.Qt.MatchStartsWith, 0)[0]
        while len(test_index) > 1:
            test_index[0:2] = [''.join(test_index[0] + '.' + test_index[1])]
            for child_index in range(current_test.childCount()):
                if current_test.child(child_index).text(0).startswith(test_index[0]):
                    current_test = current_test.child(child_index)
                    break

        # Update the test
        if status not in ["Aborted"]:
            for i in range(2):
                current_test.setBackground(i, colours[0])
                current_test.setForeground(i, colours[1])
            current_test.setText(1, status)
            current_test.setExpanded(True)

        # In case of an abort, update all remaining tests
        else:
            self.display_output(message="Aborting, please wait...", status="Active")
            sub_finish = False
            original_test = current_test
            while current_test is not None:
                if current_test.text(1) in ["Queued"]:
                    for i in range(2):
                        current_test.setBackground(i, colours[0])
                        current_test.setForeground(i, colours[1])
                    current_test.setText(1, status)
                    current_test.setExpanded(False)
                if current_test.childCount() > 0 and not sub_finish:  # Go in a level
                    current_test = current_test.child(0)
                    sub_finish = False
                elif current_test.parent() is not None:
                    if current_test.parent().indexOfChild(
                            current_test) >= current_test.parent().childCount() - 1:  # Come out a level
                        sub_finish = True
                        current_test = current_test.parent()
                    else:
                        current_test = current_test.parent().child(
                            current_test.parent().indexOfChild(current_test) + 1)  # Same level
                        sub_finish = False
                else:  # Top level test, go to next test
                    current_test = self.TestTree.topLevelItem(self.TestTree.indexOfTopLevelItem(current_test) + 1)
                    sub_finish = False
            current_test = original_test

        # Check for last test in group
        while current_test.parent() is not None and (current_test.parent().indexOfChild(
                current_test) >= current_test.parent().childCount() - 1 or status in ["Aborted"]):
            parent_status = current_test.text(1)
            current_test = current_test.parent()
            for child_index in range(current_test.childCount()):  # Check status of all child tests
                check_status = current_test.child(child_index).text(1)
                if list(STATUS_PRIORITY.keys()).index(check_status) < list(STATUS_PRIORITY.keys()).index(parent_status):
                    parent_status = check_status
            colours = get_status_colours(parent_status)
            for i in range(2):
                current_test.setBackground(i, colours[0])
                current_test.setForeground(i, colours[1])
            current_test.setText(1, parent_status)
            if parent_status not in ["In Progress"]:
                current_test.setExpanded(False)

    def display_test(self, test_index, description):
        self.ActiveTest.setText("Test {}:".format(test_index))
        self.TestDescription.setText("{}".format(description))

    def display_output(self, message, status):
        self.Events.append(message)
        self.Events.verticalScrollBar().setValue(self.Events.verticalScrollBar().maximum())

        if status == "False":  # Print errors
            self.Errors.append(self.ActiveTest.text() + ' - ' + message[1:])
            self.Errors.verticalScrollBar().setValue(self.Errors.verticalScrollBar().maximum())

        if status in ["Active", "False"]:
            self.ActiveEvent.append(message)
            self.ActiveEvent.verticalScrollBar().setValue(self.ActiveEvent.verticalScrollBar().maximum())

    def progress_update(self):
        self.ActiveEvent.clear()
        self.ProgressBar.setValue(self.worker.worker.get_current_task())
        if self.worker.worker.sequencer.tests_failed > 0 or self.worker.worker.sequencer.tests_errored > 0:
            self.ProgressBar.setStyleSheet(ERROR_STYLE)

    def get_input(self, message, choices):
        self.Events.append(message)
        self.ActiveEvent.append(message)
        self.Events.verticalScrollBar().setValue(self.Events.verticalScrollBar().maximum())
        self.ActiveEvent.verticalScrollBar().setValue(self.ActiveEvent.verticalScrollBar().maximum())
        if isinstance(choices, bool):
            pass
        elif len(choices) == 1:
            self.Button_2.setText(choices[0])
            self.Button_2.setShortcut(QtGui.QKeySequence(choices[0][0:1]))
            self.Button_2.setEnabled(True)
            self.Button_2.setDefault(True)
            self.Button_2.setFocus()
        elif len(choices) == 2:
            self.Button_1.setText(choices[0])
            self.Button_1.setShortcut(QtGui.QKeySequence(choices[0][0:1]))
            self.Button_1.setEnabled(True)
            self.Button_1.setDefault(True)
            self.Button_1.setFocus()
            self.Button_3.setText(choices[1])
            self.Button_3.setShortcut(QtGui.QKeySequence(choices[1][0:1]))
            self.Button_3.setEnabled(True)
        else:
            self.Button_1.setText(choices[0])
            self.Button_1.setShortcut(QtGui.QKeySequence(choices[0][0:1]))
            self.Button_1.setEnabled(True)
            self.Button_1.setDefault(True)
            self.Button_1.setFocus()
            self.Button_2.setText(choices[1])
            self.Button_2.setShortcut(QtGui.QKeySequence(choices[1][0:1]))
            self.Button_2.setEnabled(True)
            self.Button_3.setText(choices[2])
            self.Button_3.setShortcut(QtGui.QKeySequence(choices[2][0:1]))
            self.Button_3.setEnabled(True)

        self.working_indicator.stop()
        self.WorkingIndicator.hide()

    def _seq_abort(self, exception=None):
        """
        This function ensures that sequence aborting is handled correctly if the sequencer is blocked waiting for input
        """

        # Release user input waiting loops
        if self.fail_queue is not None:
            self.fail_queue.put(False)
            self.fail_queue = None
        if self.abort_queue is not None:
            self.abort_queue.put(True)
            self.abort_queue = None

        # Release sequence blocking calls
        if self.blocked:
            self.input_queue.put("ABORT_FORCE")

    def clean_up(self):
        """
        This function is the second one called for normal termination, and the first one called for unusual termination.
        Check for abnormal termination, and stop the sequencer if required; then stop and delete the thread
        """

        if self.worker_thread is None:  # This function has already run, therefore main already has the status code
            return

        # The following actions must be done in a specific order, be careful when making changes to this section
        self.abort_timer.stop()
        self.closing = True

        if self.status_code == -1:  # Unusual termination - The sequencer hasn't finished yet, stop it
            self.status_code = self.worker.worker.stop()

        self.unregister_events()  # Prevent interruption by pubsub messages

        self.worker.deleteLater()  # Schedule the thread worker for deletion
        self.worker = None  # Remove the reference to allow the GC to clean up

        self.worker_thread.exit(self.status_code)  # Exit the thread
        self.worker_thread.wait(2000)  # 2 seconds for the thread to exit
        self.worker_thread.terminate()  # Force quit the thread if it is still running, if so, this will throw a warning
        self.worker_thread.deleteLater()  # Schedule the thread for deletion
        self.worker_thread = None  # Remove the reference to allow the GC to clean up

        #   Now close the GUI thread, return to the controller in main
        self.application.exit(self.status_code)

    """User IO handlers, emit signals to trigger main thread updates via slots.
       These are run in the sequencer thread"""

    def event_output(self, message, status="True"):
        self.output_signal.emit(message, str(status))

    def gui_user_input(self, message, choices=None, blocking=True):
        result = None
        if choices is not None:  # Button Prompt
            if blocking:
                self.input_signal.emit(message, choices)
            else:
                self.input_signal.emit(message, (choices[0],))
                self.timer_signal.emit()
        else:  # Text Prompt
            self.text_signal.emit(message)

        if blocking:  # Block sequencer until user responds
            self.blocked = True
            result = self.input_queue.get(True)
            self.blocked = False
            self.working.emit()
        else:
            self.fail_queue = choices[1]
            self.abort_queue = choices[2]
        return result

    """UI Event Handlers, process actions taken by the user on the GUI.
       These are run in the main thread """

    def text_input_submit(self):
        self.input_queue.put(self.UserInputBox.toPlainText())
        self.UserInputBox.clear()
        self.UserInputBox.setPlaceholderText("")
        self.UserInputBox.setEnabled(False)

    def button_1_click(self):
        self.input_queue.put(self.Button_1.text())
        self.button_reset()

    def button_2_click(self):
        if self.fail_queue is not None:
            self.fail_queue.put(self.Button_2.text())
            self.fail_queue = None
            self.abort_timer.stop()
            self.abort_queue = None
        else:
            self.input_queue.put(self.Button_2.text())
        self.button_reset()

    def button_3_click(self):
        self.input_queue.put(self.Button_3.text())
        self.button_reset()

    def button_reset(self, fail_only=False):
        self.Button_2.setText("")
        self.Button_2.setEnabled(False)
        self.Button_2.setDefault(False)
        if not fail_only:
            self.Button_1.setText("")
            self.Button_3.setText("")
            self.Button_1.setEnabled(False)
            self.Button_3.setEnabled(False)
            self.Button_1.setDefault(False)
            self.Button_3.setDefault(False)

    """Thread listener, called from the sequencer thread"""

    def _completion_code(self, code):
        """This function is the first one called when the sequencer completes normally.
           Set the exit code, and signal the main thread."""
        self.status_code = code
        self.finish.emit()

    """UI Callables, called from the sequencer thread"""

    def reformat_text(self, text_str, first_line_fill="", subsequent_line_fill=""):
        lines = []
        wrapper.initial_indent = first_line_fill
        wrapper.subsequent_indent = subsequent_line_fill
        for ind, line in enumerate(text_str.splitlines()):
            if ind != 0:
                wrapper.initial_indent = subsequent_line_fill
            lines.append(wrapper.fill(line))
        return '\n'.join(lines)

    def _image(self, path, overlay):
        if self.closing:
            return
        self.update_image.emit(path, overlay)

    def _user_action(self, msg, q, abort):
        """
        This is for tests that aren't entirely dependant on the automated system.
        This works by monitoring a queue to see if the test completed successfully.
        Also while doing this it is monitoring if the escape key is pressed to signal to the system that the test fails.

        Use this in situations where you want the user to do something (like press all the keys on a keypad) where the
        system is automatically monitoring for success but has no way of monitoring failure.
        :param msg:
         Information for the user
        :param q:
         The queue object to put false if the user fails the test
        :param abort:
         The queue object to abort this monitoring as the test has already passed.
        :return:
        None
        """
        if self.closing:
            q.put(False)
            abort.put(True)
            return
        self.gui_user_input(self.reformat_text(msg), ("Fail", q, abort), False)

    def _user_ok(self, msg, q):
        """
        This can be replaced anywhere in the project that needs to implement the user driver
        The result needs to be put in the queue with the first part of the tuple as 'Exception' or 'Result' and the
        second part is the exception object or response object
        :param msg:
         Message for the user to understand what to do
        :param q:
         The result queue of type queue.Queue
        :return:
        """
        if self.closing:
            q.put("Result", None)
            return
        self.gui_user_input(msg, ("Continue",))
        q.put("Result", None)

    def _user_choices(self, msg, q, choices, target, attempts=5):
        """
        This can be replaced anywhere in the project that needs to implement the user driver
        Temporarily a simple input function.
        The result needs to be put in the queue with the first part of the tuple as 'Exception' or 'Result' and the
        second part is the exception object or response object
        This needs to be compatible with forced exit. Look to user action for how it handles a forced exit
        :param msg:
         Message for the user to understand what to input
        :param q:
         The result queue of type queue.Queue
        :param target:
         Optional
         Validation function to check if the user response is valid
        :param attempts:
        :return:
        """
        if self.closing:
            q.put(("Result", "ABORT_FORCE"))
            return

        for _ in range(attempts):
            # This will change based on the interface
            ret_val = self.gui_user_input(self.reformat_text(msg), choices)
            ret_val = target(ret_val, choices)
            if ret_val:
                q.put(('Result', ret_val))
                return
        q.put('Exception', UserInputError("Maximum number of attempts {} reached".format(attempts)))

    def _user_input(self, msg, q, target=None, attempts=5, kwargs=None):
        """
        This can be replaced anywhere in the project that needs to implement the user driver
        Temporarily a simple input function.
        The result needs to be put in the queue with the first part of the tuple as 'Exception' or 'Result' and the
        second part is the exception object or response object
        This needs to be compatible with forced exit. Look to user action for how it handles a forced exit
        :param msg:
         Message for the user to understand what to input
        :param q:
         The result queue of type queue.Queue
        :param target:
         Optional
         Validation function to check if the user response is valid
        :param attempts:

        :param kwargs:
        :return:
        """
        if self.closing:
            q.put(('Result', "ABORT_FORCE"))
            return

        initial_indent = ">>> "
        subsequent_indent = "    "
        # additional space added due to wrapper.drop_white_space being True, need to
        # drop white spaces, but keep the white space to separate the cursor from input message
        msg = self.reformat_text(msg, initial_indent, subsequent_indent) + "\n>>> "
        wrapper.initial_indent = ""
        wrapper.subsequent_indent = ""
        for _ in range(attempts):
            # This will change based on the interface
            ret_val = self.gui_user_input(msg, None, True)
            if target is None or ret_val == "ABORT_FORCE":
                q.put(ret_val)
                return
            ret_val = target(ret_val, **kwargs)
            if ret_val:
                q.put(('Result', ret_val))
                return
        q.put('Exception', UserInputError("Maximum number of attempts {} reached".format(attempts)))

    def _user_display(self, msg):
        """
        :param msg:
        :return:
        """
        if self.closing:
            return

        self.event_output(self.reformat_text(msg), status="Active")

    def _user_display_important(self, msg):
        """
        :param msg:
        :return:
        """
        if self.closing:
            return

        self.event_output("")
        self.event_output("!" * wrapper.width, status="Active")
        self.event_output("")
        self.event_output(self.reformat_text(msg), status="Active")
        self.event_output("")
        self.event_output("!" * wrapper.width, status="Active")

    def _print_sequence_end(self, status, passed, failed, error, skipped, sequence_status):
        if self.closing:
            return

        self.event_output("#" * wrapper.width)
        self.event_output(self.reformat_text("Sequence {}".format(sequence_status)), status="Active")
        # self.event_output("Sequence {}".format(sequence_status))
        post_sequence_info = []
        if status == "PASSED":
            post_sequence_info.extend(RESOURCES["SEQUENCER"].context_data.get("_post_sequence_info_pass", []))
        elif status == "FAILED" or status == "ERROR":
            post_sequence_info.extend(RESOURCES["SEQUENCER"].context_data.get("_post_sequence_info_fail", []))
        post_sequence_info.extend(RESOURCES["SEQUENCER"].context_data.get("_post_sequence_info", []))

        if post_sequence_info:
            self.event_output("-" * wrapper.width)
            self.event_output("IMPORTANT INFORMATION")
            for itm in post_sequence_info:
                self.event_output(self.reformat_text(itm))
        self.event_output("-" * wrapper.width)
        self.event_output(self.reformat_text("Status: {}".format(status)))
        self.event_output("#" * wrapper.width)

    def _print_test_start(self, data, test_index):
        if self.closing:
            return

        self.progress.emit()
        self.event_output("*" * wrapper.width)
        self.event_output(self.reformat_text("Test {}: {}".format(test_index, data.test_desc)))
        self.event_output("-" * wrapper.width)
        self.label_update.emit(test_index, data.test_desc)
        self.tree_update.emit(test_index, "In Progress")

    def _print_test_seq_start(self, data, test_index):
        if self.closing:
            return

        self.ProgressBar.setMaximum(self.worker.worker.get_task_count())
        self.tree_init.emit(self.worker.worker.get_test_tree())
        self.progress.emit()
        self._print_test_start(data, test_index)

    def _print_test_complete(self, data, test_index, status):
        if self.closing:
            return

        sequencer = RESOURCES["SEQUENCER"]
        self.event_output("-" * wrapper.width)
        self.event_output(
            self.reformat_text("Checks passed: {}, Checks failed: {}".format(sequencer.chk_pass, sequencer.chk_fail)))
        # self.event_output("Checks passed: {}, Checks failed: {}".format(sequencer.chk_pass, sequencer.chk_fail))
        self.event_output(self.reformat_text("Test {}: {}".format(test_index, status.upper())))
        # self.event_output("Test {}: {}".format(test_index, status.upper()))
        self.event_output("-" * wrapper.width)

        if status.upper() in ["ERROR", "SKIPPED"]:
            return

        if sequencer.chk_fail == 0:
            self.tree_update.emit(test_index, "Passed")
        else:
            self.tree_update.emit(test_index, "Failed")

    def _print_test_skip(self, data, test_index):
        if self.closing:
            return

        self.event_output("\nTest Marked as skip")
        self.tree_update.emit(test_index, "Skipped")

    def _print_test_retry(self, data, test_index):
        if self.closing:
            return

        self.event_output(self.reformat_text("\nTest {}: Retry".format(test_index)))

    def _print_errors(self, exception, test_index):
        if self.closing:
            return

        if isinstance(exception, SequenceAbort):
            self.tree_update.emit(test_index, "Aborted")
            status = True
        else:
            status = False
            self.tree_update.emit(test_index, "Error")
        self.event_output("")
        self.event_output("!" * wrapper.width)
        self.event_output(
            self.reformat_text("Test {}: Exception Occurred, {} {}".format(test_index, type(exception), exception)),
            status=status)
        self.event_output("!" * wrapper.width)
        # TODO self.event_output traceback into a debug log file
        if fixate.config.DEBUG:
            traceback.print_tb(exception.__traceback__, file=sys.stderr)

    def round_to_3_sig_figures(self, chk):
        """
        Tries to round elements to 3 significant figures for formatting
        :param chk:
        :return:
        """
        ret_dict = {}
        for element in ["_min", "_max", "test_val", "nominal", "tol"]:
            ret_dict[element] = getattr(chk, element, None)
            try:
                ret_dict[element] = "{:.3g}".format(ret_dict[element])
            except:
                pass
        return ret_dict

    def _print_comparisons(self, passes, chk, chk_cnt, context):
        if passes:
            status = "PASS"
        else:
            status = "FAIL"
        format_dict = self.round_to_3_sig_figures(chk)
        if chk._min is not None and chk._max is not None:
            self.event_output(self.reformat_text(
                "\nCheck {chk_cnt}: {status} when comparing {test_val} {comparison} {_min} - {_max} : "
                "{description}".format(
                    status=status,
                    comparison=chk.target.__name__[1:].replace('_', ' '),
                    chk_cnt=chk_cnt,
                    description=chk.description, **format_dict)), status=passes)
        elif chk.nominal is not None and chk.tol is not None:
            self.event_output(self.reformat_text(
                "\nCheck {chk_cnt}: {status} when comparing {test_val} {comparison} {nominal} +- {tol}% : "
                "{description}".format(
                    status=status,
                    comparison=chk.target.__name__[1:].replace('_', ' '),
                    chk_cnt=chk_cnt,
                    description=chk.description, **format_dict)), status=passes)
        elif chk._min is not None or chk._max is not None or chk.nominal is not None:
            # Grabs the first value that isn't none. Nominal takes priority
            comp_val = next(format_dict[item] for item in ["nominal", "_min", "_max"] if format_dict[item] is not None)
            self.event_output(
                self.reformat_text("\nCheck {chk_cnt}: {status} when comparing {test_val} {comparison} {comp_val} : "
                                   "{description}".format(
                    status=status,
                    comparison=chk.target.__name__[1:].replace('_', ' '),
                    comp_val=comp_val,
                    chk_cnt=chk_cnt,
                    description=chk.description, **format_dict)), status=passes)
        else:
            if chk.test_val is not None:
                self.event_output(self.reformat_text(
                    "\nCheck {chk_cnt}: {status}: {test_val} : {description}".format(chk_cnt=chk_cnt,
                                                                                     description=chk.description,
                                                                                     status=status, **format_dict)),
                    status=passes)
            else:
                self.event_output(self.reformat_text(
                    "\nCheck {chk_cnt} : {status}: {description}".format(description=chk.description, chk_cnt=chk_cnt,
                                                                         status=status)), status=passes)
