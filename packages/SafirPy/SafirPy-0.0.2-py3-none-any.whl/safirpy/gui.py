# -*- coding: utf-8 -*-

import sys
from PySide2.QtWidgets import QApplication, QLabel


def t1():
    app = QApplication(sys.argv)
    #label = QLabel("Hello World!")
    label = QLabel("<font color=red size=40>Hello World!</font>")
    label.show()
    app.exec_()


def t2():
    from PySide2.QtWidgets import QApplication
    from PySide2.QtQuick import QQuickView
    from PySide2.QtCore import QUrl

    app = QApplication([])
    view = QQuickView()
    url = QUrl("view.qml")

    view.setSource(url)
    view.setResizeMode(QQuickView.SizeRootObjectToView)
    view.show()
    app.exec_()


def t3():
    import sys
    from PySide2.QtWidgets import QApplication, QMessageBox

    # Create the application object
    app = QApplication(sys.argv)

    # Create a simple dialog box
    msg_box = QMessageBox()
    msg_box.setText("Hello World!")
    msg_box.show()

    sys.exit(msg_box.exec_())


def t4():
    from PySide2.QtWidgets import QApplication, QPushButton

    if __name__ == "__main__":
        # Create a QApplication
        app = QApplication([])

        # Create a button
        button = QPushButton('Exit')

        # Connect the button "clicked" signal to the exit() method
        # that finishes the QApplication
        button.clicked.connect(app.exit)

        button.show()
        app.exec_()


def t5():
    import sys
    import random
    from PySide2 import QtCore, QtWidgets, QtGui

    class MyWidget(QtWidgets.QWidget):
        def __init__(self):
            QtWidgets.QWidget.__init__(self)

            self.hello = ["Hallo Welt", "你好，世界", "Hei maailma",
                          "Hola Mundo", "Привет мир"]

            self.button = QtWidgets.QPushButton("Click me!")
            self.text = QtWidgets.QLabel("Hello World")
            self.text.setAlignment(QtCore.Qt.AlignCenter)

            self.layout = QtWidgets.QVBoxLayout()
            self.layout.addWidget(self.text)
            self.layout.addWidget(self.button)
            self.setLayout(self.layout)

            self.button.clicked.connect(self.magic)

        def magic(self):
            self.text.setText(random.choice(self.hello))

    app = QtWidgets.QApplication(sys.argv)

    widget = MyWidget()
    widget.show()

    sys.exit(app.exec_())


def t6():
    import sys
    from PySide2.QtWidgets import (QLineEdit, QPushButton, QApplication,
                                   QVBoxLayout, QDialog)

    class Form(QDialog):

        def __init__(self, parent=None):
            super(Form, self).__init__(parent)
            # Create widgets
            self.edit = QLineEdit("Write my name here")
            self.button = QPushButton("Show Greetings")
            # Create layout and add widgets
            layout = QVBoxLayout()
            layout.addWidget(self.edit)
            layout.addWidget(self.button)
            # Set dialog layout
            self.setLayout(layout)
            # Add button signal to greetings slot
            self.button.clicked.connect(self.greetings)

        # Greets the user
        def greetings(self):
            print("Hello %s" % self.edit.text())

    # Create the Qt Application
    app = QApplication(sys.argv)
    # Create and show the form
    form = Form()
    form.show()
    # Run the main Qt loop
    sys.exit(app.exec_())



if __name__ == '__main__':
    t6()
