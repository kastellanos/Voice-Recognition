__author__ = 'Andres'

'''
Created on Apr 15, 2015

+-------------------------------+
|                               |
|        Main Window            |
|                               |
+---------+---------+-----------+
|         |         |           |
| Select  | Add     | Login     |
| User    | User    |           |
|         |         |           |
+---------+---------+-----+-----+
                          |
                          |
                          |
                          v
                 +--------+-----------------------+
                 |                                |
                 |                                |
                 +--------------------------------+
                 |                                |
                 |                                |
                 +--------------------------------+
                 |                                |
                 |                                |
                 +--------------------------------+
http://asciiflow.com/
https://www.websequencediagrams.com/
@author: Andres
'''

import sys

from PySide import QtCore, QtGui


# from Model.process import voice_recognition as vr
from Model.process import manageData as md
import Controller.cartero as cart


class MainWindow(QtGui.QDialog):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.setAttribute(QtCore.Qt.WA_DeleteOnClose)
        self.setMinimumSize(150, 150)
        self.another_win = None
        self.comunication = cart.carta()
        self.window_conf()

    def window_conf(self):
        #create layouts
        layout = QtGui.QGridLayout()
        #create buttons
        btn_select_user = QtGui.QPushButton("Seleccionar usuario")
        btn_add_user = QtGui.QPushButton("Nuevo usuario")
        btn_login = QtGui.QPushButton("Ingresar")

        #set position of button in layout
        layout.addWidget(btn_select_user, 0, 0)
        layout.addWidget(btn_add_user, 0, 1)
        layout.addWidget(btn_login, 0, 2)

        #conect button to function
        btn_select_user.clicked.connect(self._select_user_win)
        btn_add_user.clicked.connect(self._add_user_win)
        btn_login.clicked.connect(self._login_win)

        #set layout
        self.setLayout(layout)

    def _select_user_win(self):
        #if not self.another_win:
        self.another_win = SelectUserWindow(pw=self)

        self.another_win.show()

    def _add_user_win(self):
        #if not self.another_win:
        self.another_win = AddUserWindow(pw=self)

        self.another_win.show()

    def _login_win(self):
        self.another_win = LoginUserWindow(pw=self)

        self.another_win.show()

    def get_users_list(self):
        return self.comunication.users_list()

    def add_user(self, username):
        self.comunication.add_user(username)

    def select_user(self, user_index):
        self.comunication.select_user(user_index)

    def get_current_user_index(self):
        return self.comunication.get_current_user_index()

    def get_user_by_index(self, index):
        return self.comunication.get_user_by_index(index)


class SelectUserWindow(QtGui.QDialog):
    def __init__(self, pw):
        super(SelectUserWindow, self).__init__()
        self.setAttribute(QtCore.Qt.WA_DeleteOnClose)
        self.setMinimumSize(150, 150)
        self.another_win = None
        self.pw = pw

    def configWindow(self):
        layout = QtGui.QGridLayout()
        text_users = QtGui.QLabel("Seleccione el usuario")
        self.list_users = QtGui.QComboBox()
        btn_ok = QtGui.QPushButton("Seleccionar")

        layout.addWidget(text_users, 0, 0)
        layout.addWidget(self.list_users, 0, 1)
        layout.addWidget(btn_ok, 0, 2)

        self.list_users.addItems(self.pw.get_users_list())
        btn_ok.clicked.connect(self.select_user)
        self.setLayout(layout)

    def show(self):
        self.configWindow()
        super(SelectUserWindow, self).show()

    def select_user(self):
        index = self.list_users.currentIndex()
        self.pw.select_user(index)


class AddUserWindow(QtGui.QDialog):
    def __init__(self, pw):
        super(AddUserWindow, self).__init__()
        self.setAttribute(QtCore.Qt.WA_DeleteOnClose)
        self.setMinimumSize(150, 150)
        self.another_win = None
        self.pw = pw

    def configWindow(self):
        layout = QtGui.QGridLayout()
        text_users = QtGui.QLabel("Escriba el nombre de usuario que desea utilizar")
        self.username = QtGui.QLineEdit()
        btn_create = QtGui.QPushButton("create")

        layout.addWidget(text_users, 0, 0)
        layout.addWidget(self.username, 0, 1)
        layout.addWidget(btn_create, 0, 2)

        btn_create.clicked.connect(self.add_user)

        self.setLayout(layout)

    def show(self):
        self.configWindow()
        super(AddUserWindow, self).show()

    def add_user(self):
        if self.username.text() != "":
            self.pw.add_user(self.username.text())


class LoginUserWindow(QtGui.QDialog):
    def __init__(self, pw):
        super(LoginUserWindow, self).__init__()
        self.setAttribute(QtCore.Qt.WA_DeleteOnClose)
        self.setMinimumSize(150, 150)
        self.another_win = None
        self.pw = pw
        self.user_index = self.pw.get_current_user_index()
        self.another_win = None

    def configWindow(self):
        layout = QtGui.QGridLayout()
        text_users = QtGui.QLabel("Bienvenido, " + self.pw.get_user_by_index(self.user_index))

        btn_add_cmd = QtGui.QPushButton("Agregar comandos")
        btn_add_test = QtGui.QPushButton("Agregar pruebas")

        layout.addWidget(text_users, 0, 0)
        layout.addWidget(btn_add_cmd, 0, 1)
        layout.addWidget(btn_add_test, 0, 2)

        btn_add_cmd.clicked.connect(self._add_cmd_win)

        self.setLayout(layout)

    def show(self):
        self.configWindow()
        super(LoginUserWindow, self).show()

    def add_user(self):
        if self.username.text() != "":
            self.pw.add_user(self.username.text())

    def _add_cmd_win(self):
        #if not self.another_win:
        self.another_win = AddCommandWindow(pw=self)

        self.another_win.show()


class AddCommandWindow(QtGui.QDialog):
    def __init__(self, pw):
        super(AddCommandWindow, self).__init__()
        self.setAttribute(QtCore.Qt.WA_DeleteOnClose)
        self.setMinimumSize(150, 150)
        self.another_win = None
        self.pw = pw
        #self.user_index = self.pw.get_current_user_index()
        self.en = ["uno", "dos", "tres", "cuatro", "cinco", "seis", "siete", "ocho", "nueve", "diez"]

    def configWindow(self):
        table = QtGui.QTableWidget()
        table.setRowCount(10)
        table.setColumnCount(2)
        table.setHorizontalHeaderLabels(["Numero", "Comando"])

        layout = QtGui.QGridLayout()

        command_name = QtGui.QLabel("Lista comandos actuales")
        command_add = QtGui.QLabel("Agregar comando")
        self.cmd = QtGui.QLineEdit()
        command_index = QtGui.QLabel("Siguiente numero de comando: " + str(1))
        self.progress_train = QtGui.QProgressBar()
        self.progress_record = QtGui.QProgressBar()
        self.progress_train.setMaximum(6)

        self.progress_record.setMaximum(86)

        btn_add_command = QtGui.QPushButton("Entrenar comando")
        btn_cancel_command = QtGui.QPushButton("Cancelar")

        layout.addWidget(command_name, 0, 0)
        layout.addWidget(table, 1, 0)
        layout.addWidget(command_add, 2, 0)
        layout.addWidget(command_index, 3, 0)
        layout.addWidget(self.progress_record, 4, 0)
        layout.addWidget(self.progress_train, 5, 0)
        layout.addWidget(self.cmd, 6, 0)
        layout.addWidget(btn_add_command, 7, 0)
        layout.addWidget(btn_cancel_command, 7, 1)

        # self.progress_train.setValue(4)
        self.setLayout(layout)

        btn_add_command.clicked.connect(self.start_recording)
        btn_cancel_command.clicked.connect(self.cancel_recording)

        self.worker = md()
        self.worker.updateProgressQ.connect(self.set_Qprogress)
        btn_add_command.clicked.connect(self.start_recording)
        self.worker.updateProgressS.connect(self.set_Sprogress)

    def show(self):
        self.configWindow()
        super(AddCommandWindow, self).show()

    def start_recording(self):
        self.cant = 6
        self.directory = "train/{}/".format(self.en[2 - 1])
        self.worker.setWorkspace(self.directory, self.cant)
        self.worker.start()

    def cancel_recording(self):
        pass

    def set_Qprogress(self, progress):
        self.progress_train.setValue(progress)

    def set_Sprogress(self, progress):
        self.progress_record.setValue(progress)


app = QtGui.QApplication(sys.argv)
m = MainWindow()
m.show()
sys.exit(app.exec_())

app = QtGui.QApplication(sys.argv)
m = MainWindow()
m.show()
sys.exit(app.exec_())