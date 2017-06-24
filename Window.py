# Window.py

import sys

from OpenGL import GL, GLU
from PyQt5 import QtGui, QtCore, QtWidgets
from LatchCube import LatchCube
from VectorMath import Vector, LinearTransform

class Window( QtGui.QOpenGLWindow ):
    def __init__( self, parent = None ):
        super().__init__( parent )
        self.cube = LatchCube()
        self.orientation = LinearTransform()

    def initializeGL( self ):
        GL.glShadeModel( GL.GL_SMOOTH )
        GL.glEnable( GL.GL_DEPTH_TEST )
        GL.glClearColor( 0.7, 0.7, 0.7, 0.0 )

    def paintGL( self ):
        GL.glClear( GL.GL_COLOR_BUFFER_BIT | GL.GL_DEPTH_BUFFER_BIT )

        viewport = GL.glGetIntegerv( GL.GL_VIEWPORT )
        width = viewport[2]
        height = viewport[3]

        aspectRatio = float( width ) / float( height )
        length = 2.5

        GL.glMatrixMode( GL.GL_PROJECTION )
        GL.glLoadIdentity()
        if aspectRatio > 1.0:
            GL.glOrtho( -length * aspectRatio, length * aspectRatio, -length, length, -1.0, 100.0 )
        else:
            GL.glOrtho( -length, length, -length / aspectRatio, length / aspectRatio, -1.0, 100.0 )

        GL.glMatrixMode( GL.GL_MODELVIEW )
        GL.glLoadIdentity()
        GLU.gluLookAt( 0.0, 0.0, 10.0, 0.0, 0.0, 0.0, 0.0, 1.0, 0.0 )

        GL.glBegin( GL.GL_QUADS )

        for x in range(3):
            for y in range(3):
                for z in range(3):
                    cubie = self.cube.cubie_matrix[x][y][z]
                    self.RenderCubieQuads( cubie )

        GL.glEnd()

        GL.glFlush()

    def RenderCubieQuads( self, cubie ):
        center = cubie.position
        quad_vertices = [
            Vector( -0.45, -0.45, 0.0 ),
            Vector( 0.45, -0.45, 0.0 ),
            Vector( 0.45, 0.45, 0.0 ),
            Vector( -0.45, 0.45, 0.0 )
        ]
        for face in cubie.face_list:
            self.RenderColor( face.color )
            frame = LinearTransform()
            frame.MakeFrame( face.normal )
            for vertex in quad_vertices:
                vertex = frame * vertex + center
                vertex = self.orientation * vertex
                GL.glVertex3f( vertex.x, vertex.y, vertex.z )

    def RenderColor( self, color ):
        if color == 'blue':
            GL.glColor3f( 0.0, 0.0, 1.0 )
        elif color == 'green':
            GL.glColor3f( 0.0, 1.0, 0.0 )
        elif color == 'yellow':
            GL.glColor3f( 1.0, 1.0, 0.0 )
        elif color == 'white':
            GL.glColor3f( 1.0, 1.0, 1.0 )
        elif color == 'red':
            GL.glColor3f( 1.0, 0.0, 0.0 )
        elif color == 'orange':
            GL.glColor3f( 1.0, 0.5, 0.0 )
        else:
            GL.glColor3f( 0.0, 0.0, 0.0 )

    def resizeGL( self, width, height ):
        GL.glViewport( 0, 0, width, height )