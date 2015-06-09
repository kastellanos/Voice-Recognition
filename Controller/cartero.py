__author__ = 'Andres'
# from Model.process import voice_recognition as vr
#from Model.process import manageData as md

import os


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

    def users_list(self):
        print( os.path.isfile(self.file_name) )
        if not os.path.isfile(self.file_name):
            file_to_create = open(self.file_name, 'w')
            file_to_create.close()
        file_info = open(self.file_name, 'r')

        self.info = file_info.readlines()

        print self.info

        return self.info

    def add_user(self, username):
        file_info = open(self.file_name, "a")
        file_info.write(username + "\n")
        file_info.close()

    def select_user(self, user_index):
        self.user_index = user_index

    def get_current_user_index(self):
        return self.user_index

    def get_user_by_index(self, index):
        return self.info[index]