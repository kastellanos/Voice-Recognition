__author__ = 'Andres'
'''
Created on Apr 16, 2015

@author: Andres
'''

import neurolab as nl

from Util import util_audio as ap
from Util import recording as rec


class voice_recognition():
    def __init__(self):
        # iniciar interface
        # cargar datos
        self.features = 20
        self.number_of_neurons = 100
        self.epochs = 10000
        self.show = 10000


    def process_data(self, dir_wavs, data_quantity):
        self.data = []
        for i in range(data_quantity):
            temp = '{0}s{1}.wav'.format(dir_wavs, i + 1)
            try:
                single_data = ap.extract_features(temp)
                self.data.append(single_data)
            except ValueError:
                print( "Algo esta mal con los datos de entrada")

    def get_data(self, dir_wavs, index):
        rec.record_to_file(('{0}s{1}.wav'.format(dir_wavs, index)))

    def create_som_network(self):
        self.features_data = [[-10, 10] for i in range(self.features)]
        self.network = nl.net.newc(self.features_data, self.number_of_neurons)

    def train_som_network(self):
        self.network.train(self.data, epochs=self.epochs, show=self.show)

    def test_som_network(self, data):
        self.winn = self.network.sim(self.data)
        self.neurona = 0
        for i in range(len(self.winn[0])):
            if self.winn[0][i] != 0:
                self.neurona = i
        w = self.network.layers[0].np['w']
        self.winner = w[self.neurona]
        self.distancia = []
        for i in data:
            temp = []
            for j in i:
                temp1 = []
                for k in range(len(j)):
                    dist = (self.winner[k] - j[k]) ** 2
                    dist = dist ** 0.5
                    temp1.append(dist)
                temp.append(sum(temp1[:]))
            self.distancia.append(temp)
        print self.distancia
        self.contador = 0
        self.win_comand = -1
        mini = float('inf')
        for i in self.distancia:

            for j in i:

                if j < mini:
                    print j, mini, self.contador
                    mini = j
                    self.win_comand = self.contador
            self.contador += 1
        print "contador:", self.win_comand



