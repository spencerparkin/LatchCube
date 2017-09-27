from permutation import Permutation

class RubiksCubeState:
    def __init__( self ):
        self.major_permutation = Permutation()
        self.minor_permutation = Permutation()

class RubiksCubeStateStackPushPopper:
    def __init__( self, solver ):
        self.solver = solver
    
    def __enter__( self ):
        self.solver.state_stack.push( self.solver.state[ len( self.solver.state_stack ) - 1 ].Clone() )
    
    def __exit__( self, type, exc, tb ):
        self.solver.state_stack.pop()

class RubiksCubeGroupSolver:
    R = 0
    L = 1
    U = 2
    D = 3
    F = 4
    B = 5
    Ri = 6
    Li = 7
    Ui = 8
    Di = 9
    Fi = 10
    Bi = 11
    
    def __init__( self ):
        self.major_generator_list = [
            Permutation( [ [ 24, 29, 31, 26 ], [ 25, 27, 30, 28 ], [ 2, 18, 42, 37 ], [ 4, 20, 44, 35 ], [ 7, 23, 47, 32 ] ] ), # R
            Permutation( [ [ 8, 13, 15, 10 ], [ 9, 11, 14, 12 ], [ 0, 39, 40, 16 ], [ 3, 36, 43, 19 ], [ 5, 34, 45, 21 ] ] ), # L
            Permutation( [ [ 0, 5, 7, 2 ], [ 1, 3, 6, 4 ], [ 8, 16, 24, 32 ], [ 9, 17, 25, 33 ], [ 10, 18, 26, 34 ] ] ), # U
            Permutation( [ [ 40, 45, 47, 42 ], [ 41, 43, 46, 44 ], [ 13, 37, 29, 31 ], [ 14, 38, 30, 22 ], [ 15, 39, 31, 23 ] ] ), # D
            Permutation( [ [ 16, 21, 23, 18 ], [ 17, 19, 22, 20 ], [ 5, 15, 42, 24 ], [ 6, 12, 41, 27 ], [ 7, 10, 40, 29 ] ] ), # F
            Permutation( [ [ 32, 37, 39, 34 ], [ 33, 35, 38, 36 ], [ 2, 31, 45, 8 ], [ 1, 28, 46, 11 ], [ 0, 26, 47, 13 ] ] ) # B
        ]
        # I think this can be thought of as a factor group of the Rubik's Cube group.  If you take the subgroup of all permutations that
        # change orientation, but not position, then that is a normal subgroup, and modding out by that subgroup gives you this group,
        # which can be thought of as all the permutations that change positions without regard to how orientation is changing.
        self.minor_generator_list = [
            Permutation( [ [ 0, 12, 14, 2 ], [ 8, 13, 9, 1 ] ] ), # R
            Permutation( [ [ 4, 16, 18, 6 ], [ 5, 10, 17, 11 ] ] ), # L
            Permutation( [ [ 12, 18, 16, 14 ], [ 19, 17, 15, 13 ] ] ), # U
            Permutation( [ [ 0, 2, 4, 6 ], [ 1, 3, 5, 7 ] ] ), # D
            Permutation( [ [ 0, 6, 18, 12 ], [ 7, 11, 19, 8 ] ] ), # F
            Permutation( [ [ 2, 14, 16, 4 ], [ 3, 9, 15, 10 ] ] ) # B
        ]
        for i in range(6):
            self.major_generator_list.append( Permutation().Inverse( self.major_generator_list[i] ) )
            self.minor_generator_list.append( Permutation().Inverse( self.minor_generator_list[i] ) )
        self.major_trial_list = [
            # Orient corners:
            [
                self.Di, self.Ri, self.D, self.R, self.Di, self.Ri, self.D, self.R, self.U,
                self.Ri, self.Di, self.R, self.D, self.Ri, self.Di, self.R, self.D, self.Ui
            ],
            # Orient edges:
            [
                 
            ]
        ]
        self.minor_trial_list = [
            # Permute corners:
            [ self.Ui, self.Li, self.U, self.R, self.U, self.L, self.Ui, self.Ri ],
            # Permute edges:
            [ self.R, self.U, self.Ri, self.Ui, self.R, self.U, self.Ri, self.Ui ]
        ]
        self.state_stack = [ RubiksCubeState() ]

    def ApplyMove( self, move ):
        state = self.CurrentState()
        state.major_permutation.Concatinate( self.major_generator_list[ move ] )
        state.minor_permutation.Concatinate( self.minor_generator_list[ move ] )

    def ApplyMoveSequence( self, move_sequence ):
        for move in move_sequence:
            self.ApplyMove( move )

    def CurrentState( self ):
        return self.state_stack[ len( self.state_stack ) - 1 ] 

    def CurrentPermutation( self, kind ):
        return getattr( self.CurrentState(), kind + '_permutation' )

    def FindSolutionSequence( self ):
        # Here we solve the position of all cubies first, then the orientation of all cubies.
        solution_sequence = []
        with RubiksCubeStateStackPushPopper( self ):
            for kind in [ 'minor', 'major' ]:
                while not self.CurrentPermutation( kind ).IsIdentity():
                    current_damage = self.CurrentPermutation( kind ).Damage()
                    reducing_sequence = None
                    for move_sequence in self.GenerateTrialSequences( getattr( self, kind + '_trial_list' ) ):
                        with RubiksCubeStateStackPushPopper( self ):
                            self.ApplyMoveSequence( move_sequence )
                            damage = self.CurrentPermutation( kind ).Damage()
                            if damage < current_damage:
                                reducing_sequence = move_sequence
                                break
                    if not reducing_sequence:
                        return None # We failed to find a solution.  :(
                    self.ApplyMoveSequence( reducing_sequence )
                    solution_sequence += reducing_sequence
        return solution_sequence

    def GenerateTrialSequences( self, trial_list, setup_sequence = [], teardown_sequence = [] ):
        for sequence in trial_list:
            generated_sequence = setup_sequence + sequence + teardown_sequence
            yield generated_sequence
        if len( setup_sequence ) <= 3:
            for i in range(12):
                setup_sequence.append(i)
                teardown_sequence = [ ( i + 6 ) % 12 ] + teardown_sequence
                yield from self.GenerateTrialSequences( trial_list, setup_sequence, teardown_sequence )
                setup_sequence.pop( len( setup_sequence ) - 1 )
                teardown_sequence.pop(0)