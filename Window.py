# Window.py

import sys

from OpenGL import GL
from PyQt5 import QtGui, QtCore, QtWidgets
from LatchCube import LatchCube

class Window( QtGui.QOpenGLWindow ):
    def __init__( self, parent = None ):
        super().__init__( parent )
        self.cube = LatchCube()

    def initializeGL( self ):
        GL.glShadeModel( GL.GL_SMOOTH )
        GL.glEnable( GL.GL_DEPTH_TEST )
        GL.glClearColor( 1.0, 1.0, 1.0, 0.0 )

    def paintGL( self ):
        GL.glClear( GL.GL_COLOR_BUFFER_BIT | GL.GL_DEPTH_BUFFER_BIT )
        GL.glFlush()

    def resizeGL( self, width, height ):
        GL.glViewport( 0, 0, width, height )