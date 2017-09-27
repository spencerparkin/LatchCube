import math

from OpenGL import GL, GLU
from PyQt5 import QtGui, QtCore, QtWidgets
from cube import RubiksCube
from vector_math import Vector, LinearTransform

class RubiksCubeWindow( QtGui.QOpenGLWindow ):
    def __init__( self, parent = None ):
        super().__init__( parent )
        self.cube = RubiksCube()
        self.orientation = LinearTransform()
        self.animation_transform = LinearTransform()
        self.animation_axis = None
        self.animation_angle = 0.0
        self.animation_timer = QtCore.QTimer()
        self.animation_timer.start(1)
        self.animation_timer.timeout.connect( self.OnAnimationTimer )
        self.dragPos = None
        self.dragging = False
        self.setTitle( 'Rubik\'s Cube' )

    def initializeGL( self ):
        GL.glShadeModel( GL.GL_SMOOTH )
        GL.glEnable( GL.GL_DEPTH_TEST )
        GL.glClearColor( 0.7, 0.7, 0.7, 0.0 )

    def paintGL( self ):
        # TODO: Get the Z-buffer working.
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
            normal = face.normal
            if cubie.animation_transform:
                normal = cubie.animation_transform * normal
            normal = self.orientation * normal
            if normal.z < 0:
                continue
            self.RenderColor( face.color )
            frame = LinearTransform()
            frame.MakeFrame( face.normal )
            for vertex in quad_vertices:
                vertex = frame * vertex + center + face.normal * 0.5
                if cubie.animation_transform:
                    vertex = cubie.animation_transform * vertex
                vertex = self.orientation * vertex
                GL.glVertex3f( vertex.x, vertex.y, vertex.z )
            # TODO: Render constraint arrows.

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

    def mousePressEvent( self, event ):
        button = event.button()
        if button == QtCore.Qt.LeftButton:
            self.dragPos = event.pos()
            self.dragging = True

    def mouseMoveEvent( self, event ):
        if self.dragging:
            pos = event.pos()
            dragVector = Vector()
            dragVector.x = float( pos.x() - self.dragPos.x() )
            dragVector.y = float( pos.y() - self.dragPos.y() )
            self.dragPos = pos
            scale = 0.01
            xAngle = scale * dragVector.y
            yAngle = scale * dragVector.x
            xAxisRotation = LinearTransform()
            yAxisRotation = LinearTransform()
            xAxisRotation.MakeRotation( Vector( 1.0, 0.0, 0.0 ), xAngle )
            yAxisRotation.MakeRotation( Vector( 0.0, 1.0, 0.0 ), yAngle )
            self.orientation = xAxisRotation * self.orientation
            self.orientation = yAxisRotation * self.orientation
            self.orientation.Orthonormalize() # Do this just to deal with accumulated round-off error.
            self.update()

    def mouseReleaseEvent( self, event ):
        self.dragging = False

    def ClearAnimation( self ):
        for i in range(3):
            for j in range(3):
                for k in range(3):
                    self.cube.cubie_matrix[i][j][k].animation_transform = None

    def wheelEvent( self, event ):
        angleDelta = event.angleDelta().y()
        steps = angleDelta / 120
        self.animation_angle = math.pi / 2.0 * float( steps )
        direction = 'cw'
        if steps < 0:
            steps = -steps
            direction = 'ccw'
        axis = self.FindFacingAxis()
        if not axis:
            return
        self.ClearAnimation()
        while steps > 0:
            if not self.cube.RotateFace( axis, direction ):
                return
            steps -= 1
        cubie_list = self.cube.CollectCubiesForAxis( axis )
        for cubie in cubie_list:
            cubie.animation_transform = self.animation_transform
        self.animation_axis = axis
        self.animation_transform.MakeRotation( self.animation_axis, self.animation_angle )
        self.update()

    def OnAnimationTimer( self ):
        if math.fabs( self.animation_angle ) > 0.0:
            animation_rate = math.pi / 128.0
            if self.animation_angle > 0.0:
                self.animation_angle -= animation_rate
                if self.animation_angle < 0.0:
                    self.animation_angle = 0.0
            else:
                self.animation_angle += animation_rate
                if self.animation_angle > 0.0:
                    self.animation_angle = 0.0
            self.animation_transform.MakeRotation( self.animation_axis, self.animation_angle )
            self.update()

    def FindFacingAxis( self ):
        best_axis = None
        best_z = 0.0
        for i in range(2):
            for j in range(3):
                axis = Vector()
                c = 1.0 if i == 0 else -1.0
                axis.x = c if j == 0 else 0.0
                axis.y = c if j == 1 else 0.0
                axis.z = c if j == 2 else 0.0
                transformed_axis = self.orientation * axis
                if transformed_axis.z > best_z:
                    best_z = transformed_axis.z
                    best_axis = axis
        return best_axis