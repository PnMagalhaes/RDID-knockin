from PyQt5 import QtGui, QtWidgets
import sys
import dialog

class ExampleApp(QtWidgets.QDialog, dialog.Ui_Dialog):
    def __init__(self, parent=None):
        super(ExampleApp, self).__init__(parent)
        self.setupUi(self)

def main():
    app = QtWidgets.QApplication(sys.argv)
    form = ExampleApp()
    form.show()
    app.exec_()


if __name__ == '__main__':
    main()