__author__ = 'Andres'

'''
Created on Apr 15, 2015

@author: Andres
'''
import os

from PySide import QtCore, QtGui
import numpy as np

from Model import process

class MainWindow(QtGui.QDialog):
    def procesado(self):
        self.proceso = process.voice_recognition()

    def __init__(self, n):

        super(MainWindow, self).__init__()
        self.setAttribute(QtCore.Qt.WA_DeleteOnClose)
        self.setMinimumSize(150, 150)
        self.n = n
        # self.window_zero()
        if n == 0:
            self.window_zero()
        elif n == 1:
            self.window_one()
        elif n == 2:
            self.window_two()
        elif n == 3:
            self.procesado()
            self.proceso.create_som_network()
            self.comandos = [("Comandos", "")]
            self.en = ["uno", "dos", "tres", "cuatro", "cinco", "seis", "siete", "ocho", "nueve", "diez"]
            self.data_record = []
            self.window_three()
            self.variable = True
        elif n == 4:
            self.window_four()
        else:
            # self.window_beta()
            pass


        # self.createActions()
        # self.statusBar()
        self.setWindowTitle("Voice Recognition(Alpha)")

    def window_zero(self):
        layout = QtGui.QGridLayout()
        self.btn_new_user = QtGui.QPushButton("Nuevo Usuario")
        self.btn_login = QtGui.QPushButton("Iniciar sesion")
        layout.addWidget(self.btn_new_user, 0, 0)
        layout.addWidget(self.btn_login, 0, 1)
        self.setLayout(layout)
        self.btn_new_user.clicked.connect(self.createWindow1)
        self.btn_login.clicked.connect(self.createWindow2)

    def createWindow1(self):
        self.window1 = MainWindow(1)
        self.window1.show()

    def createWindow2(self):
        self.window2 = MainWindow(2)
        self.window2.show()

    def createWindow3(self):
        self.window3 = MainWindow(3)
        self.window3.show()

    def createWindow4(self):
        self.window4 = MainWindow(4)
        self.window4.show()

    def training_process(self):
        self.actual = len(self.comandos) + 1
        self.windowt = MainWindow(100)
        layout = QtGui.QGridLayout()
        self.command_name = QtGui.QLabel("Nombre comando")
        self.text_command = QtGui.QTextEdit("vacio")
        self.command_index = QtGui.QLabel("Indice 1")
        self.btn_start_training = QtGui.QPushButton("Empezar entrenamiento")
        self.btn_add_command = QtGui.QPushButton("Agregar comando")
        self.command_index = QtGui.QLabel("Se debe repetir \"{}\" 6 veces.".format(self.actual))

        self.enum_progress = QtGui.QLabel("{}/6".format(0))
        self.progress_train = QtGui.QProgressDialog()
        layout.addWidget(self.command_name, 0, 0)
        layout.addWidget(self.text_command, 1, 0)
        layout.addWidget(self.command_index, 2, 0)
        layout.addWidget(self.btn_start_training, 3, 0)
        layout.addWidget(self.enum_progress, 4, 0)
        layout.addWidget(self.progress_train, 5, 0)
        layout.addWidget(self.btn_add_command, 6, 0)
        self.progress_train.setMaximum(6)
        # self.progress_train.setValue(4)
        self.windowt.setLayout(layout)
        self.windowt.show()
        self.btn_start_training.clicked.connect(self.start_recording)
        self.btn_add_command.clicked.connect(self.process_recording)

    def start_recording(self):

        self.cant = 6
        self.directory = "train/{}/".format(self.en[self.actual - 1])
        if not os.path.exists(self.directory):
            os.makedirs(self.directory)
        for i in range(self.cant):
            self.proceso.get_data(self.directory, i + 1)
            self.enum_progress.setText("{}/6".format(i + 1))
            self.progress_train.setValue(i + 1)

    def process_recording(self):
        self.proceso.process_data(self.directory, self.cant)
        self.data_record.append(self.proceso.data)
        self.comandos.append((self.text_command.toPlainText(), self.directory))
        # self.proceso.train_som_network()
        self.update_table()

    def window_one(self):
        layout = QtGui.QGridLayout()
        self.label_register = QtGui.QLabel("Registro")
        self.btn_train_login = QtGui.QPushButton("Entrenar inicio de sesion")
        self.btn_train_register = QtGui.QPushButton("Registrar datos de usuario")
        self.btn_add_user = QtGui.QPushButton("Agregar Usuario")
        self.btn_cancel = QtGui.QPushButton("Cancelar")
        layout.addWidget(self.label_register, 0, 0)
        layout.addWidget(self.btn_train_login, 1, 0)
        layout.addWidget(self.btn_train_register, 2, 0)
        layout.addWidget(self.btn_add_user, 3, 0)
        layout.addWidget(self.btn_cancel, 3, 1)
        self.setLayout(layout)

    def update_table(self):
        for i in range(len(self.comandos)):
            self.table.setItem(i, 0, QtGui.QTableWidgetItem(self.comandos[i][0]))

    def window_three(self):
        self.layout1 = QtGui.QGridLayout()
        self.btn_new_command = QtGui.QPushButton("Nuevo Comando")
        self.btn_talk = QtGui.QPushButton("Hablar")

        self.table = QtGui.QTableWidget()
        self.table.setRowCount(10)
        self.table.setColumnCount(1)
        self.table.setItem(0, 0, QtGui.QTableWidgetItem("Comandos"))

        self.layout1.addWidget(self.table, 0, 0)
        self.layout1.addWidget(self.btn_new_command, 0, 1)
        self.layout1.addWidget(self.btn_talk, 1, 0)
        self.setLayout(self.layout1)
        self.btn_new_command.clicked.connect(self.training_process)
        self.btn_talk.clicked.connect(self.recognice_patern)

    def recognice_patern(self):

        self.test_directory = "test/"
        if not os.path.exists(self.test_directory):
            os.makedirs(self.test_directory)
        self.proceso.get_data(self.test_directory, 1)
        self.proceso.process_data(self.test_directory, 1)
        data_to_process = []
        for i in self.data_record:
            data_to_process.extend(i)
        variable = np.asarray(data_to_process)

        np.savetxt("control.csv", variable, delimiter=",")

        if self.variable:
            self.proceso.data = data_to_process
            self.proceso.train_som_network()
            self.variable = False
        # print len(self.data_record)
        self.proceso.test_som_network(self.data_record)
        print( self.comandos[self.proceso.win_comand + 1])
        os.system("espeak -ves-la+f5 \"Se esta ejecutando el comando {}\"".format(
            self.comandos[self.proceso.win_comand + 1][0]))

    def window_four(self):
        layout = QtGui.QGridLayout()
        # self.layout_train = QtGui.QLabel("Se debe repetir \"{}\" 6 veces.".format(index))

        self.btn_add_command = QtGui.QPushButton("Agregar comando")
        layout.addWidget(self.layout_train, 0, 0)


    def window_two(self):
        layout = QtGui.QGridLayout()
        self.btn_start_try = QtGui.QPushButton("Empezar intento")
        self.progress = QtGui.QProgressDialog()
        layout.addWidget(self.btn_start_try, 0, 0)
        layout.addWidget(self.progress, 1, 0)
        self.setLayout(layout)

        self.btn_start_try.clicked.connect(self.record_voice)




