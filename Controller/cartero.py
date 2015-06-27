__author__ = 'Andres'
import os

import numpy as np
import matplotlib.pyplot as plt

from Model.process import voice_recognition as vr


class carta():
    def __init__(self):
        #self.proceso = vr(number_of_neurons=6)
        #self.data_process = md()
        #        self.proceso.create_som_network()
        self.comandos = [("Comandos", "")]
        self.en = ["uno", "dos", "tres", "cuatro", "cinco", "seis", "siete", "ocho", "nueve", "diez"]
        self.data_record = []
        self.file_name = "lista_usuarios.txt"
        self.variable = True
        self.user_index = 0
        self.info = []
        self.user_list = []
        self.command_list = ["Abrir Google Chrome", "Abrir Administrador de tareas", "Abrir consola",
                             "Abrir calculadora", "Abrir internet explorer",
                             "Abrir paint", "Abrir notepad", "Abrir reproductor", "Apagar sistema", "Reiniciar sistema"]

    def get_cmd_list(self):
        return self.command_list

    def add_cmd(self, index):
        self.user_list[self.get_current_user_index()].add_command(self.command_list[index])

    def users_list(self, firstPick):

        if not os.path.isfile(self.file_name):
            file_to_create = open(self.file_name, 'w')
            file_to_create.close()
        file_info = open(self.file_name, 'r')
        m = file_info.readlines()
        k = []

        if firstPick:
            for i in m:
                self.user_list.append(usuario(name=i.strip()))
                k.append(i.strip())

        else:
            for i in m:
                k.append(i.strip())
        self.info = k

        return self.info

    def add_user(self, username):
        file_info = open(self.file_name, "a")
        self.user_list.append(usuario(name=username))
        file_info.write(username + "\n")
        file_info.close()

    def select_user(self, user_index):
        self.user_index = user_index

        if os.path.isfile(self.get_user_by_index(user_index) + ".gop"):
            self.user_list[user_index].load(self.get_user_by_index(user_index))
            us = usuario()
            # us.load(self.get_user_by_index(user_index).strip())
            self.user_list.append(us)


    def get_current_user_index(self):
        return self.user_index

    def get_user_by_index(self, index):
        return self.info[index]

    def get_user_cmd(self):
        return self.user_list[self.get_current_user_index()].get_command_list()

    def train_net(self, data):
        self.user_list[self.get_current_user_index()].train_network(data)
        self.user_list[self.get_current_user_index()].save()

    def get_cmd_index(self):
        return self.user_list[self.get_current_user_index()].get_cmd_index()

    def add_test(self, index):
        self.user_list[self.get_current_user_index()].add_test(self.en[index])

    def get_test_index(self):
        return self.user_list[self.get_current_user_index()].get_test_index()

    def get_test_list(self):
        return self.user_list[self.get_current_user_index()].get_test_list()

    def simulate(self, data):
        temp = self.user_list[self.get_current_user_index()].simulate(data)

        return temp

    def activation_map(self, dato):
        self.user_list[self.get_current_user_index()].activation_map(dato)


class usuario(object):
    def __init__(self, name="", state=False, cmd_index=0):
        self.name = name
        self.state = state
        self.cmd_index = cmd_index
        self.neuro = 10
        self.net = vr(number_of_neurons=self.neuro)

        self.net.create_som_network()
        self.list_cmd = []
        self.en = ["uno", "dos", "tres", "cuatro", "cinco", "seis", "siete", "ocho", "nueve", "diez"]
        self.command_list = ["Abrir Google Chrome", "Abrir Administrador de tareas", "Abrir consola",
                             "Abrir calculadora", "Abrir internet explorer",
                             "Abrir paint", "Abrir notepad", "Abrir reproductor", "Apagar sistema", "Reiniciar sistema"]
        self.data = []
        self.test_list = []
        self.test_index = 0

    def set_state(self, state):
        self.state = state

    def set_cmd_index(self, cmd_index):
        self.cmd_index = cmd_index

    def get_state(self):
        return self.state

    def get_cmd_index(self):
        return self.cmd_index

    def add_command(self, cmd_name):
        self.list_cmd.append((self.en[self.cmd_index], cmd_name))
        self.cmd_index += 1

    def get_command_list(self):
        return self.list_cmd

    def train_network(self, data):
        self.data = data
        self.state = True
        self.net.train_som_network(data)
        print ("entrenado")

    def add_test(self, command):
        self.test_index += 1
        self.test_list.append([command, "Not tested"])

    def get_test_index(self):
        return self.test_index

    def get_test_list(self):
        return self.test_list

    def excec_command(self, ind):
        index = ind
        self.command_exc = ["start chrome.exe", "taskmgr.exe", "start cmd.exe", "calc.exe", "start iexplore.exe",
                            "mspaint", "notepad", "wmplayer", "shutdown /f now", "shutdown /r"]

        indc = 0
        for i in self.command_list:
            if i == index:
                index = indc
            indc += 1

        os.system(self.command_exc[index])

    def simulate(self, data):
        self.ka = self.list_cmd[self.net.find_winner(data) - 1][1].strip()
        print (self.list_cmd)
        print ("winner: ", self.net.find_winner(data))
        print( "espeak -ves-la+f4 \"Se esta ejecutando el comando {}\"".format(
            self.ka) )

        os.system("espeak -ves-la+f4 \"Se esta ejecutando el comando {}\"".format(
            self.list_cmd[self.net.find_winner(data) - 1][1].strip()))
        self.test_list[self.test_index - 1][1] = self.en[self.net.find_winner(data) - 1]
        self.excec_command(self.ka)
        return self.net.find_winner(data) - 1

    def save(self):
        f = file(str(self.name) + ".gop", "wb")

        f.write(self.name + "\n")
        f.write(str(self.state) + "\n")
        f.write(str(self.cmd_index) + "\n")

        f.close()
        np.savetxt(self.name + "/comandos.csv", self.list_cmd, delimiter=",", fmt="%s")
        np.savetxt(self.name + "/datos.csv", self.data, delimiter=",")

    def load(self, name):
        f = file(name + ".gop", "rb")
        self.name = f.readline().strip()
        self.state = bool(f.readline())
        self.cmd_index = int(f.readline())
        self.list_cmd = np.loadtxt(name + "/comandos.csv", usecols=(0, 1), delimiter=",", dtype=str)

        self.data = np.loadtxt(name + "/datos.csv", delimiter=",")
        self.train_network(self.data)

    def activation_map(self, data):
        map = self.net.activ(data)
        x = []
        y = []
        z = []
        p = []
        mini = float('inf')
        het = np.min(map)

        for i in range(self.neuro):
            for j in range(self.neuro):
                x.append(i + 1)
                y.append(j + 1)
                z.append(map[i][j])

                if map[i][j] < mini:
                    mini = map[i][j]
                    p = (i, j)

        s = [20 * 3 ** 3 for n in range(len(x))]
        plt.figure()

        plt.text(p[0] + 1, p[1] + 1, str(self.net.find_winner(data)))
        plt.scatter(x, y, c=z, s=s)
        plt.show()

# us = usuario(name="xxx")
#us.save()

