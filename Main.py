# Main.py

import sys

from PyQt5 import QtGui
from Window import Window

if __name__ == '__main__':

    app = QtGui.QGuiApplication( sys.argv )

    win = Window()
    win.resize( 640, 480 )
    win.show()

    sys.exit( app.exec_() )