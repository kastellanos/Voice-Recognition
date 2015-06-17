__author__ = 'Andres'

# -*- coding: utf-8 -*-

import sys

from PySide import QtGui

# from View import main_window as Vista
from View.vistas import MainWindow

try:
    import _portaudio as pa
except ImportError:
    print("Please build and install the PortAudio Python " +
          "bindings first.")
    sys.exit(-1)

app = QtGui.QApplication(sys.argv)
m = MainWindow()
m.show()
sys.exit(app.exec_())


