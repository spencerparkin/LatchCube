import math

class Vector:
    def __init__( self, x = 0.0, y = 0.0, z = 0.0 ):
        self.x = float( x )
        self.y = float( y )
        self.z = float( z )

    def __add__( self, other ):
        sum = Vector()
        sum.x = self.x + other.x
        sum.y = self.y + other.y
        sum.z = self.z + other.z
        return sum

    def __sub__( self, other ):
        diff = Vector()
        diff.x = self.x - other.x
        diff.y = self.y - other.y
        diff.z = self.z - other.z
        return diff

    def __mul__( self, other ):
        product = Vector()
        if isinstance( other, Vector ):
            product.x = self.x * other.x
            product.y = self.y * other.y
            product.z = self.z * other.z
        elif type( other ) is float:
            product.x = self.x * other
            product.y = self.y * other
            product.z = self.z * other
        return product

    def __eq__( self, other ):
        if self.x != other.x:
            return False
        if self.y != other.y:
            return False
        if self.z != other.z:
            return False
        return True

    def Clone( self ):
        return Vector( self.x, self.y, self.z )

    def Normalize( self ):
        length = self.Length()
        if length != 0.0:
            self.Scale( 1.0 / length )

    def Scale( self, scalar ):
        self.x *= scalar
        self.y *= scalar
        self.z *= scalar

    def Length( self ):
        return math.sqrt( self.x * self.x + self.y * self.y + self.z * self.z )

    def Dot( self, other ):
        return self.x * other.x + self.y * other.y + self.z * other.z

    def Cross( self, other ):
        product = Vector()
        product.x = self.y * other.z - self.z * other.y
        product.y = self.z * other.x - self.x * other.z
        product.z = self.x * other.y - self.y * other.x
        return product

    def LargestAbsComponent( self ):
        absX = math.fabs( self.x )
        absY = math.fabs( self.y )
        absZ = math.fabs( self.z )
        if absX > absY:
            if absX > absZ:
                return 'x'
            else:
                return 'z'
        else:
            if absY > absZ:
                return 'y'
            else:
                return 'z'

    def SmallestAbsComponent( self ):
        absX = math.fabs( self.x )
        absY = math.fabs( self.y )
        absZ = math.fabs( self.z )
        if absX < absY:
            if absX < absZ:
                return 'x'
            else:
                return 'z'
        else:
            if absY < absZ:
                return 'y'
            else:
                return 'z'

    def BestOrthogonalVector( self ):
        ortho_vecs = [
            Vector( 0.0, self.z, -self.y ),
            Vector( self.z, 0.0, -self.x ),
            Vector( self.y, -self.x, 0.0 ),
        ]
        best_vec = None
        best_length = 0.0
        for vec in ortho_vecs:
            length = vec.Length()
            if length > best_length:
                best_length = length
                best_vec = vec
        return best_vec

    def RoundToNearestIntegerComponents( self ):
        self.x = float( round( self.x ) )
        self.y = float( round( self.y ) )
        self.z = float( round( self.z ) )

    def ProjectOnto( self, other ):
        scale = self.Dot( other )
        projection = other * scale
        return projection

    def RejectFrom( self, other ):
        projection = self.ProjectOnto( other )
        rejection = self - projection
        return rejection

class LinearTransform:
    def __init__( self, xAxis = None, yAxis = None, zAxis = None ):
        self.xAxis = xAxis.Clone() if xAxis else Vector( 1.0, 0.0, 0.0 )
        self.yAxis = yAxis.Clone() if yAxis else Vector( 0.0, 1.0, 0.0 )
        self.zAxis = zAxis.Clone() if zAxis else Vector( 0.0, 0.0, 1.0 )

    def MakeRotation( self, axis, angle ):
        ca = math.cos( angle )
        sa = math.sin( angle )
        omca = 1.0 - ca

        self.xAxis.x = omca * axis.x * axis.x + ca
        self.xAxis.y = omca * axis.x * axis.y + axis.z * sa
        self.xAxis.z = omca * axis.x * axis.z - axis.y * sa

        self.yAxis.x = omca * axis.y * axis.x - axis.z * sa
        self.yAxis.y = omca * axis.y * axis.y + ca
        self.yAxis.z = omca * axis.y * axis.z + axis.x * sa

        self.zAxis.x = omca * axis.z * axis.x + axis.y * sa
        self.zAxis.y = omca * axis.z * axis.y - axis.x * sa
        self.zAxis.z = omca * axis.z * axis.z + ca

    def MakeFrame( self, vec ):
        self.zAxis = vec.Clone()
        self.zAxis.Normalize()
        self.yAxis = self.zAxis.BestOrthogonalVector()
        self.yAxis.Normalize()
        self.xAxis = self.yAxis.Cross( self.zAxis )

    def Clone( self ):
        return LinearTransform( self.xAxis.Clone(), self.yAxis.Clone(), self.zAxis.Clone() )

    def __mul__( self, other ):
        if isinstance( other, LinearTransform ):
            product = LinearTransform()
            product.xAxis = self * other.xAxis
            product.yAxis = self * other.yAxis
            product.zAxis = self * other.zAxis
            return product
        elif isinstance( other, Vector ):
            sum = Vector()
            sum += self.xAxis * other.x
            sum += self.yAxis * other.y
            sum += self.zAxis * other.z
            return sum
        return None

    def Orthonormalize( self ):
        self.xAxis.Normalize()
        self.yAxis.RejectFrom( self.xAxis )
        self.yAxis.Normalize()
        self.zAxis = self.xAxis.Cross( self.yAxis )