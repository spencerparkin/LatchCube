# LatchCube.py

import math

from VectorMath import Vector, LinearTransform

class LatchCubieFace:
    def __init__( self, color, normal, constraint_direction = None ):
        self.color = color
        self.normal = normal
        self.constraint_direction = constraint_direction
        self.new_face = None

    def Clone( self ):
        # Notice that we do not clone the new_face member here,
        # but we clone everything else about the cubie face.
        face = LatchCubieFace( self.color, self.normal, self.constraint_direction )
        return face

class LatchCubie:
    def __init__( self, position ):
        self.position = position
        self.face_list = []
        if position.x == -1.0:
            self.face_list.append( LatchCubieFace( 'blue', Vector( -1, 0, 0 ), 'ccw' if position.y == 0.0 else None ) )
        if position.x == 1.0:
            self.face_list.append( LatchCubieFace( 'green', Vector( 1, 0, 0 ), 'cw' if position.z == 0.0 else None ) )
        if position.y == -1.0:
            self.face_list.append( LatchCubieFace( 'yellow', Vector( 0, -1, 0 ), 'ccw' if position.x == 0.0 else None ) )
        if position.y == 1.0:
            self.face_list.append( LatchCubieFace( 'white', Vector( 0, 1, 0 ), 'cw' if position.z == 0.0 else None ) )
        if position.z == -1.0:
            self.face_list.append( LatchCubieFace( 'red', Vector( 0, 0, -1 ), 'ccw' if position.x == 0.0 else None ) )
        if position.z == 1.0:
            self.face_list.append( LatchCubieFace( 'orange', Vector( 0, 0, 1 ), 'cw' if position.y == 0.0 else None ) )

    def FindFaceWithNormal( self, normal ):
        for face in self.face_list:
            if face.normal == normal:
                return face
        return None

class LatchCube:
    def __init__( self ):
        self.cubie_matrix = [
            [
                [
                    LatchCubie( Vector( x - 1, y - 1, z - 1 ) ) for z in range(3)
                ]
                for y in range(3)
            ]
            for x in range(3)
        ]

    def CubieAtPosition( self, position ):
        i = int( position.x )
        j = int( position.y )
        k = int( position.z )
        return self.cubie_matrix[i][j][k]

    def RotateFace( self, face, direction ):

        # Formulate the axis of rotation.
        if face == '+x':
            axis = Vector( 1, 0, 0 )
        elif face == '-x':
            axis = Vector( -1, 0, 0 )
        elif face == '+y':
            axis = Vector( 0, 1, 0 )
        elif face == '-y':
            axis = Vector( 0, -1, 0 )
        elif face == '+z':
            axis = Vector( 0, 0, 1 )
        elif face == '-z':
            axis = Vector( 0, 0, -1 )
        else:
            return False

        # Formulate the angle of rotation.
        if direction == 'ccw':
            angle = math.pi / 2.0
        elif direction == 'cw':
            angle = -math.pi / 2.0
        else:
            return False

        # This matrix's inverse is its transpose, so it
        # should work on positions and normals.
        transform = LinearTransform()
        transform.MakeRotation( axis, angle )

        # Determine which cubies are going to move.
        cubie_list = []
        for i in range( -1, 1 ):
            for j in range( -1, 1 ):
                if axis.x == 1.0 or axis.x == -1.0:
                    cubie_list.append( self.cubie_matrix[ int( axis.x ) ][i][j] )
                elif axis.y == 1.0 or axis.y == -1.0:
                    cubie_list.append( self.cubie_matrix[i][ int( axis.y ) ][j] )
                elif axis.z == 1.0 or axis.z == -1.0:
                    cubie_list.append( self.cubie_matrix[i][j][ int( axis.z ) ] )

        # This is what makes the Latch Cube so hard!!!
        for cubie in cubie_list:
            face = cubie.FindFaceWithNormal( axis )
            if face.constraint_direction and face.constraint_direction != direction:
                return False

        normal_list = []
        normal_list.append( Vector( -1, 0, 0 ) )
        normal_list.append( Vector( 1, 0, 0 ) )
        normal_list.append( Vector( 0, -1, 0 ) )
        normal_list.append( Vector( 0, 1, 0 ) )
        normal_list.append( Vector( 0, 0, -1 ) )
        normal_list.append( Vector( 0, 0, 1 ) )

        # Compute the face transitions.
        for cubie in cubie_list:
            position = transform * cubie.position
            target_cubie = self.CubieAtPosition( position )
            for normal in normal_list:
                face = cubie.FindFaceWithNormal( normal )
                if face:
                    target_normal = transform * normal
                    target_normal.RoundToNearestIntegerComponents()
                    target_face = target_cubie.FindFaceWithNormal( target_normal )
                    target_face.new_face = face.Clone()

        # Apply the face transitions.
        for cubie in cubie_list:
            for i in len( cubie.face_list ):
                face = cubie.face_list[i]
                if face.new_face:
                    cubie.face_list[i] = face.new_face

        return True