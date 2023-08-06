# -*- coding: utf-8 -*-

import sys

from PySide2.QtWidgets import QApplication, QLabel
import PySide2.QtWidgets as qtw


class Form(qtw.QDialog):

    def __init__(self, parent=None):
        super(Form, self).__init__(parent)
        # Create widgets
        self.edit = qtw.QLineEdit("input file path")
        self.button = qtw.QPushButton("select")

        # Create layout and add widgets
        layout = qtw.QVBoxLayout()
        layout.addWidget(self.edit)
        layout.addWidget(self.button)

        # Set dialog layout
        self.setLayout(layout)

        # Add button signal to greetings slot
        self.button.clicked.connect(self.get_file_path)

    # Greets the user
    def greetings(self):
        print("Hello %s" % self.edit.text())
        print(self.edit.isReadOnly())
        self.edit.setReadOnly(not self.edit.isReadOnly())

    def get_file_path(self):
        path_string = qtw.QFileDialog().getOpenFileName()
        print(path_string)
        return path_string


if __name__ == '__main__':
    # Create the Qt Application
    app = QApplication(sys.argv)
    # Create and show the form
    form = Form()
    form.show()
    # Run the main Qt loop
    sys.exit(app.exec_())
