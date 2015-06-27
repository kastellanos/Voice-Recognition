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
        self.firstPick = True

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
        self.hide()
        self.another_win.show()

    def _add_user_win(self):
        #if not self.another_win:
        self.another_win = AddUserWindow(pw=self)
        self.hide()
        self.another_win.show()

    def _login_win(self):
        self.another_win = LoginUserWindow(pw=self)
        # self.hide()
        self.another_win.show()

    def get_users_list(self):
        if self.firstPick:
            return self.comunication.users_list(self.firstPick)
            self.firstPick = False
        else:
            return self.comunication.users_list(self.firstPick)

    def add_user(self, username):
        self.comunication.add_user(username)

    def select_user(self, user_index):
        self.comunication.select_user(user_index)

    def get_current_user_index(self):
        return self.comunication.get_current_user_index()

    def get_user_by_index(self, index):
        return self.comunication.get_user_by_index(index)

    def get_cmd_list(self):
        return self.comunication.get_cmd_list()

    def get_user_cmd(self):
        return self.comunication.get_user_cmd()

    def add_command(self, index):
        self.comunication.add_cmd(index)

    def train_net(self, data):
        self.comunication.train_net(data)

    def get_cmd_index(self):
        return self.comunication.get_cmd_index()

    def add_test(self, index):
        self.comunication.add_test(index)

    def get_test_index(self):
        return self.comunication.get_test_index()

    def get_test_list(self):
        return self.comunication.get_test_list()

    def simulate(self, data):
        return self.comunication.simulate(data)

    def firstPick(self):
        return self.firstPick

    def setFirstPick(self, value):
        self.firstPick = value

    def activation_map(self, data):
        self.comunication.activation_map(data)
class SelectUserWindow(QtGui.QDialog):
    def __init__(self, pw):
        super(SelectUserWindow, self).__init__()
        self.setAttribute(QtCore.Qt.WA_DeleteOnClose)
        self.setMinimumSize(150, 150)
        self.another_win = None
        self.progressBar = QtGui.QProgressBar()

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
        self.close()
        self.pw.show()





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
        self.close()
        self.pw.show()


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
        btn_add_file_test = QtGui.QPushButton("Agregar Archivos prueba")

        layout.addWidget(text_users, 0, 0)
        layout.addWidget(btn_add_cmd, 0, 1)
        layout.addWidget(btn_add_test, 0, 2)
        layout.addWidget(btn_add_file_test, 0, 3)
        btn_add_cmd.clicked.connect(self._add_cmd_win)
        btn_add_test.clicked.connect(self._add_test_win)
        btn_add_file_test.clicked.connect(self._add_file_test_win)
        self.setLayout(layout)

    def show(self):
        self.configWindow()
        super(LoginUserWindow, self).show()

    def add_user(self):
        if self.username.text() != "":
            self.pw.add_user(self.username.text())

    def _add_cmd_win(self):
        #if not self.another_win:
        self.another_win = AddCommandWindow(pw=self.pw)

        self.another_win.show()

    def _add_test_win(self):
        self.another_win = AddTestWindow(pw=self.pw)
        self.another_win.show()

    def _add_file_test_win(self):
        self.another_win = AddFileTestWindow(pw=self.pw)
        self.another_win.show()

class AddTestWindow(QtGui.QDialog):
    def __init__(self, pw):
        super(AddTestWindow, self).__init__()
        self.setAttribute(QtCore.Qt.WA_DeleteOnClose)
        self.setMinimumSize(500, 150)
        self.another_win = None
        self.pw = pw

        self.en = ["uno", "dos", "tres", "cuatro", "cinco", "seis", "siete", "ocho", "nueve", "diez"]

    def configWindow(self):
        self.table = QtGui.QTableWidget()
        self.table.setRowCount(30)
        self.table.setColumnCount(3)
        self.table.setHorizontalHeaderLabels(["", "esperado", "Obtenido"])
        layout = QtGui.QGridLayout()
        command_name = QtGui.QLabel("Pruebas actuales")
        command_add = QtGui.QLabel("Agregar Prueba")
        self.cmd = QtGui.QComboBox()
        command_index = QtGui.QLabel("Numero probado")
        self.progress_train = QtGui.QProgressBar()
        self.progress_record = QtGui.QProgressBar()
        self.progress_train.setMaximum(1)

        self.progress_record.setMaximum(86)
        btn_show_statistics = QtGui.QPushButton("Ver estadisticas")
        btn_add_command = QtGui.QPushButton("Agregar Prueba")
        btn_cancel_command = QtGui.QPushButton("Mapa de activacion")
        btn_hit_map = QtGui.QPushButton("Mapa de activacion")
        self.cmd.addItems(self.en)
        layout.addWidget(command_name, 0, 0)
        layout.addWidget(self.table, 1, 0)
        layout.addWidget(command_add, 2, 0)

        layout.addWidget(self.progress_record, 3, 0)
        layout.addWidget(self.progress_train, 4, 0)
        layout.addWidget(command_index, 5, 0)
        layout.addWidget(self.cmd, 6, 0)
        layout.addWidget(btn_show_statistics, 6, 1)
        layout.addWidget(btn_add_command, 7, 0)
        layout.addWidget(btn_cancel_command, 7, 1)

        self.setLayout(layout)

        btn_add_command.clicked.connect(self.start_recording)
        btn_cancel_command.clicked.connect(self.activation_map)
        btn_show_statistics.clicked.connect(self.view_statistics)
        self.worker = md()
        self.worker.updateProgressQ.connect(self.set_Qprogress)

        self.worker.updateProgressS.connect(self.set_Sprogress)
        self.worker.record_finished.connect(self.update_table)

    def show(self):
        self.configWindow()
        super(AddTestWindow, self).show()

    def start_recording(self):
        self.cant = 1

        self.directory = "{}/test/".format(self.pw.get_user_by_index(self.pw.get_current_user_index()).strip())
        self.pw.add_test(self.cmd.currentIndex())
        self.worker.setWorkspace(self.directory, self.cant, single=True, num=self.pw.get_test_index())
        self.worker.start()


    def update_table(self, flag):
        if flag == 1:
            self.simulate()

            lista = self.pw.get_test_list()
            for i in range(len(lista)):
                k = QtGui.QCheckBox()
                self.table.setCellWidget(i, 0, k)
                self.table.setItem(i, 1, QtGui.QTableWidgetItem(lista[i][0]))
                self.table.setItem(i, 2, QtGui.QTableWidgetItem(lista[i][1]))
                if lista[i][1] == "Not tested":
                    self.table.item(i, 2).setBackground(QtGui.QColor('yellow'))
                if lista[i][1] == lista[i][0]:
                    self.table.item(i, 2).setBackground(QtGui.QColor('green'))
                else:
                    self.table.item(i, 2).setBackground(QtGui.QColor('red'))

    def checkBox_index(self):
        lista = self.pw.get_test_list()
        index = -1
        for i in range(len(lista)):

            if self.table.cellWidget(i, 0).isChecked():
                index = i
        return index

    def simulate(self, index=-1):
        if index == -1:

            ind = self.pw.get_test_index()

            dir = "{}/test/".format(self.pw.get_user_by_index(self.pw.get_current_user_index()).strip())
            data = self.worker.process_data(dir, 1, data_index=ind)
            self.pw.simulate(data)
        else:
            pass  # implementar checkbox test


    def set_Qprogress(self, progress):
        self.progress_train.setValue(progress)

    def set_Sprogress(self, progress):
        self.progress_record.setValue(progress)

    def activation_map(self):
        ind = self.checkBox_index()

        dir = "{}/test/".format(self.pw.get_user_by_index(self.pw.get_current_user_index()).strip())
        data = self.worker.process_data(dir, 1, data_index=ind + 1)
        self.pw.activation_map(data)

    def view_statistics(self):
        self.another_win = ViewStats(pw=self.pw)
        self.another_win.show()


# -----Add FILE test windows
class AddFileTestWindow(QtGui.QDialog):
    def __init__(self, pw):
        super(AddFileTestWindow, self).__init__()
        self.setAttribute(QtCore.Qt.WA_DeleteOnClose)
        self.setMinimumSize(500, 150)
        self.another_win = None
        self.pw = pw
        self.files_list = []
        self.en = ["uno", "dos", "tres", "cuatro", "cinco", "seis", "siete", "ocho", "nueve", "diez"]

    def configWindow(self):
        self.table = QtGui.QTableWidget()
        self.table.setRowCount(30)
        self.table.setColumnCount(3)
        self.table.setHorizontalHeaderLabels(["", "esperado", "Obtenido"])
        layout = QtGui.QGridLayout()
        command_name = QtGui.QLabel("Pruebas actuales")
        command_add = QtGui.QLabel("Agregar Prueba")
        self.cmd = QtGui.QComboBox()
        command_index = QtGui.QLabel("Numero probado")
        self.progress_train = QtGui.QProgressBar()
        self.progress_record = QtGui.QProgressBar()
        self.progress_train.setMaximum(1)

        self.progress_record.setMaximum(86)
        btn_show_statistics = QtGui.QPushButton("Ver estadisticas")
        btn_add_command = QtGui.QPushButton("Agregar Prueba")
        btn_cancel_command = QtGui.QPushButton("Mapa de activacion")
        btn_hit_map = QtGui.QPushButton("Mapa de activacion")
        self.cmd.addItems(self.en)
        layout.addWidget(command_name, 0, 0)
        layout.addWidget(self.table, 1, 0)
        layout.addWidget(command_add, 2, 0)

        layout.addWidget(self.progress_record, 3, 0)
        layout.addWidget(self.progress_train, 4, 0)
        layout.addWidget(command_index, 5, 0)
        layout.addWidget(self.cmd, 6, 0)
        layout.addWidget(btn_show_statistics, 6, 1)
        layout.addWidget(btn_add_command, 7, 0)
        layout.addWidget(btn_cancel_command, 7, 1)

        self.setLayout(layout)

        btn_add_command.clicked.connect(self.add_test)
        btn_cancel_command.clicked.connect(self.activation_map)
        btn_show_statistics.clicked.connect(self.view_statistics)
        self.worker = md()
        self.worker.updateProgressQ.connect(self.set_Qprogress)

        self.worker.updateProgressS.connect(self.set_Sprogress)
        self.worker.record_finished.connect(self.update_table)

    def add_test(self):
        self.fname = QtGui.QFileDialog.getOpenFileName(self, 'Open file')
        # self.fname = self.fname[0]
        self.directory = self.fname[0]
        self.files_list.append(self.directory)
        self.pw.add_test(self.cmd.currentIndex())
        self.update_table(1)

    def simulate(self, index=-2):
        if index == -2:

            ind = index

            dir = self.directory
            print dir
            data = self.worker.process_data(dir, 1, data_index=ind)
            self.pw.simulate(data)
        else:
            pass  # implementar checkbox test

    def show(self):
        self.configWindow()
        super(AddFileTestWindow, self).show()

    def update_table(self, flag):
        if flag == 1:
            self.simulate()

            lista = self.pw.get_test_list()
            for i in range(len(lista)):
                k = QtGui.QCheckBox()
                self.table.setCellWidget(i, 0, k)
                self.table.setItem(i, 1, QtGui.QTableWidgetItem(lista[i][0]))
                self.table.setItem(i, 2, QtGui.QTableWidgetItem(lista[i][1]))
                if lista[i][1] == "Not tested":
                    self.table.item(i, 2).setBackground(QtGui.QColor('yellow'))
                if lista[i][1] == lista[i][0]:
                    self.table.item(i, 2).setBackground(QtGui.QColor('green'))
                else:
                    self.table.item(i, 2).setBackground(QtGui.QColor('red'))

    def checkBox_index(self):
        lista = self.pw.get_test_list()
        index = -1
        for i in range(len(lista)):

            if self.table.cellWidget(i, 0).isChecked():
                index = i
        return index


    def set_Qprogress(self, progress):
        self.progress_train.setValue(progress)

    def set_Sprogress(self, progress):
        self.progress_record.setValue(progress)

    def activation_map(self):
        ind = self.checkBox_index()

        dir = self.files_list[ind]
        data = self.worker.process_data(dir, 1, data_index=-2)
        self.pw.activation_map(data)

    def view_statistics(self):
        self.another_win = ViewStats(pw=self.pw)
        self.another_win.show()


# --------------------------
# End Test
#view states
class ViewStats(QtGui.QDialog):
    def __init__(self, pw):
        super(ViewStats, self).__init__()
        self.setAttribute(QtCore.Qt.WA_DeleteOnClose)
        self.setMinimumSize(150, 150)
        self.another_win = None
        self.pw = pw
        #self.user_index = self.pw.get_current_user_index()
        self.en = ["uno", "dos", "tres", "cuatro", "cinco", "seis", "siete", "ocho", "nueve", "diez"]
        self.sirv = []
        self.sirv2 = 0

    def configWindow(self):
        self.table = QtGui.QTableWidget()
        self.table.setRowCount(30)
        self.table.setColumnCount(2)
        self.table.setHorizontalHeaderLabels(["Comando", "Porcentaje acierto"])

        layout = QtGui.QGridLayout()

        command_name = QtGui.QLabel("Estadisticas Individuales")
        command_add = QtGui.QLabel("Estadistica Total")
        self.cmd = QtGui.QComboBox()
        self.command_index = QtGui.QLabel("Siguiente numero de comando: " + str(1))
        self.progress_train = QtGui.QProgressBar()
        self.progress_record = QtGui.QProgressBar()
        self.progress_train.setMaximum(6)
        btn_generar_reporte = QtGui.QPushButton("Generar reporte")
        self.progress_record.setMaximum(86)

        self.cmd.addItems(self.pw.get_cmd_list())
        layout.addWidget(command_name, 0, 0)
        layout.addWidget(self.table, 1, 0)
        layout.addWidget(command_add, 2, 0)
        layout.addWidget(self.command_index, 3, 0)
        layout.addWidget(btn_generar_reporte, 4, 0)
        btn_generar_reporte.clicked.connect(self.generate_report)



        # self.progress_train.setValue(4)
        self.setLayout(layout)

        self.update_table(1)

    def show(self):
        self.configWindow()
        super(ViewStats, self).show()


    def update_table(self, flag):


        lista = self.pw.get_test_list()
        dicc = {}
        app = []
        dicci = {}
        for i in range(len(lista)):
            if lista[i][0] not in dicci:
                if lista[i][0] == lista[i][1]:
                    dicci[lista[i][0]] = 1
                else:
                    dicci[lista[i][0]] = 0
            else:
                if lista[i][0] == lista[i][1]:
                    dicci[lista[i][0]] += 1
            if lista[i][0] not in dicc:
                app.append(lista[i][0])
                dicc[lista[i][0]] = 1


            else:
                dicc[lista[i][0]] += 1

        counter = 0
        tem = 0
        self.sirv = []
        self.sirv2 = 0
        for i in range(len(app)):
            counter += dicc[app[i]]
            tem += dicci[app[i]]
            self.table.setItem(i, 0, QtGui.QTableWidgetItem(app[i]))
            self.sirv.append(str((dicci[app[i]] * 100.0) / dicc[app[i]]))
            self.table.setItem(i, 1, QtGui.QTableWidgetItem(str((dicci[app[i]] * 100.0) / dicc[app[i]])))
        self.sirv2 = (tem * 100.0) / counter
        self.command_index.setText("El porcentaje total de palabras reconocidas fue {}".format((tem * 100.0) / counter))

    def generate_report(self):
        dir = "{}/reporte.txt".format(self.pw.get_user_by_index(self.pw.get_current_user_index()))
        f = file(dir, "w")
        f.write("Porcentaje individual\n")
        for i in self.sirv:
            f.write(i)
            f.write("\n")
        f.write("Porcentaje Total\n")
        f.write(str(self.sirv2))
        f.write("\n")
        f.close()


#----------
#Start Add
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
        self.table = QtGui.QTableWidget()
        self.table.setRowCount(30)
        self.table.setColumnCount(2)
        self.table.setHorizontalHeaderLabels(["Numero", "Comando"])

        layout = QtGui.QGridLayout()

        command_name = QtGui.QLabel("Lista comandos actuales")
        command_add = QtGui.QLabel("Agregar comando")
        self.cmd = QtGui.QComboBox()
        command_index = QtGui.QLabel("Siguiente numero de comando: " + str(1))
        self.progress_train = QtGui.QProgressBar()
        self.progress_record = QtGui.QProgressBar()
        self.progress_train.setMaximum(6)

        self.progress_record.setMaximum(86)

        btn_add_command = QtGui.QPushButton("Agregar comando")
        btn_cancel_command = QtGui.QPushButton("Entrenar red")
        self.cmd.addItems(self.pw.get_cmd_list())
        layout.addWidget(command_name, 0, 0)
        layout.addWidget(self.table, 1, 0)
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
        btn_cancel_command.clicked.connect(self.train_network)

        self.worker = md()
        self.worker.updateProgressQ.connect(self.set_Qprogress)

        self.worker.updateProgressS.connect(self.set_Sprogress)
        self.worker.record_finished.connect(self.update_table)
        self.update_table(1)
    def show(self):
        self.configWindow()
        super(AddCommandWindow, self).show()

    def start_recording(self):
        self.cant = 6
        pos = self.pw.get_cmd_index()
        self.directory = "{}/train/{}/".format(self.pw.get_user_by_index(self.pw.get_current_user_index()).strip(),
            self.en[pos])
        self.worker.setWorkspace(self.directory, self.cant)
        self.worker.start()
        self.pw.add_command(self.cmd.currentIndex())


    def update_table(self, flag):
        if flag == 1:

            lista = self.pw.get_user_cmd()
            for i in range(len(lista)):
                self.table.setItem(i, 0, QtGui.QTableWidgetItem(lista[i][0]))
                self.table.setItem(i, 1, QtGui.QTableWidgetItem(lista[i][1]))


    def train_network(self):
        lista = self.pw.get_user_cmd()
        data = []

        for i, j in lista:
            dir = "{}/train/{}/".format(self.pw.get_user_by_index(self.pw.get_current_user_index()).strip(), i)
            data.extend(self.worker.process_data(dir, 6))
        self.pw.train_net(data)
    def set_Qprogress(self, progress):
        self.progress_train.setValue(progress)

    def set_Sprogress(self, progress):
        self.progress_record.setValue(progress)


app = QtGui.QApplication(sys.argv)
m = MainWindow()

m.show()
sys.exit(app.exec_())
