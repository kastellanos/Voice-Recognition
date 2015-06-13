__author__ = 'Andres'

# -*- coding: utf-8 -*-

import sys

from PySide import QtGui

from View import main_window as Vista

try:
    import _portaudio as pa
except ImportError:
    print("Please build and install the PortAudio Python " +
          "bindings first.")
    sys.exit(-1)

app = QtGui.QApplication(sys.argv)

ventana = Vista.MainWindow(3)

ventana.show()


sys.exit(app.exec_())


