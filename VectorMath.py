# VectorMath.py

import math

class Vector:
	def __init__( self, x = 0.0, y = 0.0, z = 0.0 ):
		self.x = float(x)
		self.y = float(y)
		self.z = float(z)
	
	def __add__( self, other ):
		sum = Vector()
		sum.x = self.x + other.x
		sum.y = self.y + other.y
		sum.z = self.z + other.z
		return sum

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
	
	def RoundToNearestIntegerComponents( self ):
		self.x = int( self.x )
		self.y = int( self.y )
		self.z = int( self.z )
		
class LinearTransform:
	def __init__( self, xAxis = Vector(), yAxis = Vector(), zAxis = Vector() ):
		self.xAxis = xAxis
		self.yAxis = yAxis
		self.zAxis = zAxis
	
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
	
	def __mul__( self, other ):
		if isinstance( other, LinearTransform ):
			pass
		elif isinstance( other, Vector ):
			sum = Vector()
			sum += self.xAxis * other.x
			sum += self.yAxis * other.y
			sum += self.zAxis * other.z
			return sum
		return None