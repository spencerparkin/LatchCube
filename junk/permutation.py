def Lcm( number_list ):
    walk_list = number_list.copy()
    while not all( [ walk_list[0] == walk_list[i] for i in range( 1, len( walk_list ) ) ] ):
        j = 0
        for i in range( 1, len( walk_list ) ):
            if walk_list[i] < walk_list[j]:
                j = i
        walk_list[j] += number_list[j]
    return walk_list[0]

class Permutation:
    def __init__( self, cycle_list = None ):
        self.map = {}
        if cycle_list:
            for cycle in cycle_list:
                self.DefineCycle( cycle )
    
    def DefineCycle( self, cycle ):
        for i in range( len( cycle ) ):
            j = ( i + 1 ) % len( cycle )
            self.map[ cycle[i] ] = cycle[j]
    
    def Evaluate( self, input ):
        if not input in self.map:
            output = input
        else:
            output = self.map[ input ]
        return output
    
    def FactorIntoProductOfDisjointCycles( self ):
        factorization = []
        input_queue = [ i for i in len( self.map ) ]
        while len( input_queue ) > 0:
            cycle = [ input_queue.pop(0) ]
            while True:
                point = self.Evaluate( cycle[ len( cycle ) - 1 ] )
                if point == cycle[0]:
                    break
                cycle.append( point )
                input_queue.remove( point )
            if len( cycle ) > 1:
                cycle = Permutation( cycle )
                factorization.append( cycle )
    
    def Order( self ):
        factorization = self.FactorIntoProductOfDisjointCycles()
        return Lcm( [ len( factorization[i].map ) for i in len( factorization ) ] )
    
    def Parity( self ):
        factorization = self.FactorIntoProductOfDisjointCycles()
        sum = 0
        for cycle in factorization:
            sum += len( cycle.map ) - 1
        if sum % 2 == 0:
            return 'even'
        return 'odd'
    
    def Concatinate( self, permutation ):
        j = max( self.map.keys() + self.permutation.map.keys() )
        new_map = {}
        for i in range(j):
            new_map[i] = permutation.Evaluate( self.Evaluate(i) )
        self.map = new_map
        self.Trim()
    
    def Multiply( self, first, second ):
        self.map = {}
        self.Concatinate( first )
        self.Concatinate( second )
    
    def Product( self, permutation_list ):
        self.map = {}
        for permutation in permutation_list:
            self.Concatinate( permutation )
    
    def Inverse( self, permutation ):
        self.map = {}
        for i in permutation.map:
            j = permutation.map[i]
            if j in self.map:
                return False # This means the permutation was invalid.
            self.map[j] = i
        return True

    def IsIdentity( self ):
        return True if self.Damage() == 0 else False

    def Damage( self ):
        # It can be shown that the damage of a commutator is always less than the
        # damage of the permutations taken in the commutator product.  Similarly,
        # the damage of a conjugate is always the same as the damage of the permutation
        # having been conjugated by any other or the same permutation.
        self.Trim()
        return len( self.map )
    
    def Trim( self ):
        trim_list = []
        for i in range( len( self.map ) ):
            if self.map[i] == i:
                trim_list.append(i)
        for i in trim_list:
            del self.map[ trim_list[i] ]
    
    def MakeString( self ):
        pass