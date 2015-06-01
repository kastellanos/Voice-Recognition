__author__ = 'Andres'

# -*- coding: utf-8 -*-

import sys

from PySide import QtGui

from View import main_window as Vista


app = QtGui.QApplication(sys.argv)

ventana = Vista.MainWindow(3)

ventana.show()

# proce = proceso.voice_recognition()
# proce.get_data("train/", 3)

sys.exit(app.exec_())


