# -*- coding: utf-8 -*-
__author__ = 'Andres'

import copy

import numpy as np
import scipy.io.wavfile as wav
import librosa


def read_wave(path):
    """
    read_wave( path )
        Extrae la señal y el sample rate de un archivo .wav

        Utiliza el modulo de entrada/salida de scipy para archivos wav
        lee los datos del archivo y retorna la señal y el ratio.
    """
    rate, signal = wav.read(path)
    return signal, rate


def mfcc_vector(ceps):
    """
    mfcc_vector( ceps )
        Convierte la matriz de mfcc features(mxn) en un vector(1xn)

        Utiliza la función mean de numpy para calcular la media de
        cada columna de la matriz ceps para asi retornar estos valores
        en un vector.

        Parámetros
        ceps--- Matriz de mxn
            m---Frames en los que fue dividida la señal
            n---Numero de caracteristicas extraidas
        Salida
          Vx--- Vector de 1xn
    """
    feat_arr = []
    num_ceps = len(ceps)

    feat_arr.append(np.mean(ceps[:], axis=1))
    Vx = np.array(feat_arr)
    # print(len(Vx[0]))
    return Vx


def create_mfcc(x, y):
    """
    create_mfcc(x,y)
        Extrae los Coeficientes Cepstrales en las Frecuencias de Mel
        (Mel Frequency Cepstral coefficients)

        Utiliza la funcioón mfcc del modulo feature de la libreria librosa

        Parámetros
        x---señal
        y---sample rate
    """
    return librosa.feature.mfcc(x, y, n_mfcc=26)


def extract_features(file_path):
    """
    extract_features( file_path )
        Procesa la señal utilizando el proceso de extraccion de datos
        de un archivo .wav, para luego extraer los coeficientes mfcc,
        y convertirlos en un vector.

        Parámetros
        file_path---Ruta del archivo a procesar
    """
    signal, rate = read_wave(file_path)
    y = create_mfcc(signal, rate)
    z = mfcc_vector(y)
    print len(z), len(z[0])
    k = z[0]
    return k[:13]


def preprocess_mfcc(mfcc):
    mfcc_cp = copy.deepcopy(mfcc)
    for i in range(mfcc.shape[1]):
        mfcc_cp[:, i] = mfcc[:, i] - np.mean(mfcc[:, i])
        mfcc_cp[:, i] = mfcc_cp[:, i] / np.max(np.abs(mfcc_cp[:, i]))
    return mfcc_cp

