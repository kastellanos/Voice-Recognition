# -*- coding: utf-8 -*-
__author__ = 'Andres'
'''
Created on Apr 16, 2015

@author: Andres
'''
# Modified som workspace
import os

from PySide import QtCore

from Model.minisomc import MiniSom
from Util import util_audio as ap
from Util import recording as rec


class voice_recognition():
    def __init__(self, features=13, number_of_neurons=10, epochs=1000, data=None):
        # iniciar interface
        # cargar datos
        self.features = features
        self.number_of_neurons = number_of_neurons
        self.epochs = epochs
        self.show = 1000
        self.data = data
        self.data_mapping = {}

    def create_som_network(self):
        x = y = self.number_of_neurons
        self.network = MiniSom(x, y, self.features)

    def train_som_network(self, data):
        self.data = data
        datos = 6
        temp = 1
        counter = 0
        self.network.train_random(self.data, self.epochs)
        for i in range(len(self.data)):
            self.data_mapping[self.network.winner(self.data[i])] = temp
            counter += 1
            if counter == 6:
                counter = 0
                temp += 1

    def save_som_network(self, path):
        self.network.save(path)

    def load_som_network(self, path):
        self.network.load(path)



    def find_winner(self, x):
        self.winner = self.network.winner(x)
        if self.winner in self.data_mapping:
            return self.data_mapping[self.winner]
        else:
            map = self.network.activate(x)
            mini = float('inf')
            index = 0
            for i in self.data_mapping:
                if map[i[0]][i[1]] < mini:
                    index = self.data_mapping[i]
                    mini = map[i[0]][i[1]]
            return index

    def activ(self, data):
        return self.network.activate(data)

class manageData(QtCore.QThread):
    updateProgressQ = QtCore.Signal(int)
    updateProgressS = QtCore.Signal(int)
    record_finished = QtCore.Signal(int)
    def __init__(self):
        self.data = []
        self.rec = rec.recording()
        QtCore.QThread.__init__(self)

    def record_data(self, dir_wavs, index):
        """
        Lanza la interfaz de grabación, la cual permite un responsive recording.
        :param dir_wavs: Directorio en el que se almacena la grabación
        :param index: indice de identificación del erchivo ej. index = 1 -> s1.wav ...
        :return: void function
        """
        self.rec.record_to_file(('{0}s{1}.wav'.format(dir_wavs, index)))

    def setWorkspace(self, path, q, single=False, num=0):
        self.path = path
        self.quantity = q
        self.single = single
        self.test = num
        self.rec.updateProgressS.connect(self.emitSome)

    def emitSome(self, some):
        self.updateProgressS.emit(some)

    def run(self, *args, **kwargs):
        if not os.path.exists(self.path):
            os.makedirs(self.path)
        if self.single == False:
            for i in range(self.quantity):
                self.record_data(self.path, i + 1)
                self.updateProgressQ.emit(i + 1)
            self.record_finished.emit(1)
        else:
            self.record_data(self.path, self.test)
            self.updateProgressQ.emit(1)
            self.record_finished.emit(1)
    def setProgress(self, progress):
        self.progressBar.setValue(progress)

    def process_data(self, dir_wavs, data_quantity, data_index=-1):
        """
        Procesa las grabaciones previamente realizadas, extrayendo las caracteristicas.

        :param dir_wavs: Directorio en el que se almacena la grabación.
        :param data_quantity: cantidad de datos que seran procesados en el directorio, empieza desde el indice 1
                              hasta data_quantity.
        :return: datos procesados.
        """
        if data_index != -1:
            temp = "{0}s{1}.wav".format(dir_wavs, data_index)
            single_data = ap.extract_features(temp)
            return single_data
        else:
            self.data = []
            for i in range(data_quantity):
                temp = '{0}s{1}.wav'.format(dir_wavs, i + 1)
                try:
                    single_data = ap.extract_features(temp)
                    self.data.append(single_data)

                except ValueError:
                    print( "Algo esta mal con los datos de entrada")
            # print self.data

            return self.data



