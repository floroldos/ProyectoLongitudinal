class CubeRubik2x2:
    def __init__(self, last_movement = ""):
        self.faces = {
            'U': [['W'] * 2 for _ in range(2)],  # Blanco
            'D': [['Y'] * 2 for _ in range(2)],  # Amarillo
            'F': [['G'] * 2 for _ in range(2)],  # Verde
            'B': [['B'] * 2 for _ in range(2)],  # Azul
            'L': [['O'] * 2 for _ in range(2)],  # Naranja
            'R': [['R'] * 2 for _ in range(2)]   # Rojo
        }
        self.last_movement = last_movement

    def copy(self):
        new_cube = CubeRubik2x2()
        for face in self.faces:
            for i in range(2):
                for j in range(2):
                    new_cube.faces[face][i][j] = self.faces[face][i][j]
        return new_cube

    def rotate_face(self, face):
        self.faces[face][0][0], self.faces[face][0][1], self.faces[face][1][1], self.faces[face][1][0] = \
            self.faces[face][1][0], self.faces[face][0][0], self.faces[face][0][1], self.faces[face][1][1]

    def rotate_face_prime(self, face):
        self.faces[face][0][0], self.faces[face][0][1], self.faces[face][1][1], self.faces[face][1][0] = \
            self.faces[face][0][1], self.faces[face][1][1], self.faces[face][1][0], self.faces[face][0][0]

    def rotate_U(self):
        self.rotate_face('U')
        self.faces['F'][0], self.faces['R'][0], self.faces['B'][0], self.faces['L'][0] = \
            self.faces['R'][0], self.faces['B'][0], self.faces['L'][0], self.faces['F'][0]

    def rotate_U_prime(self):
        self.rotate_face_prime('U')
        self.faces['F'][0], self.faces['R'][0], self.faces['B'][0], self.faces['L'][0] = \
            self.faces['L'][0], self.faces['F'][0], self.faces['R'][0], self.faces['B'][0]

    def rotate_D(self):
        self.rotate_face('D')
        self.faces['F'][1], self.faces['R'][1], self.faces['B'][1], self.faces['L'][1] = \
            self.faces['L'][1], self.faces['F'][1], self.faces['R'][1], self.faces['B'][1]

    def rotate_D_prime(self):
        self.rotate_face_prime('D')
        self.faces['F'][1], self.faces['R'][1], self.faces['B'][1], self.faces['L'][1] = \
            self.faces['R'][1], self.faces['B'][1], self.faces['L'][1], self.faces['F'][1]

    def rotate_F(self):
        self.rotate_face('F')
        temp = [self.faces['U'][1][0], self.faces['U'][1][1]]
        self.faces['U'][1][0], self.faces['U'][1][1] = self.faces['L'][1][1], self.faces['L'][0][1]
        self.faces['L'][1][1], self.faces['L'][0][1] = self.faces['D'][0][1], self.faces['D'][0][0]
        self.faces['D'][0][1], self.faces['D'][0][0] = self.faces['R'][0][0], self.faces['R'][1][0]
        self.faces['R'][0][0], self.faces['R'][1][0] = temp[0], temp[1]

    def rotate_F_prime(self):
        self.rotate_face_prime('F')
        temp = [self.faces['U'][1][0], self.faces['U'][1][1]]
        self.faces['U'][1][0], self.faces['U'][1][1] = self.faces['R'][0][0], self.faces['R'][1][0]
        self.faces['R'][0][0], self.faces['R'][1][0] = self.faces['D'][0][1], self.faces['D'][0][0]
        self.faces['D'][0][1], self.faces['D'][0][0] = self.faces['L'][1][1], self.faces['L'][0][1]
        self.faces['L'][1][1], self.faces['L'][0][1] = temp[0], temp[1]

    def rotate_B(self):
        self.rotate_face('B')
        temp = [self.faces['U'][0][0], self.faces['U'][0][1]]
        self.faces['U'][0][0], self.faces['U'][0][1] = self.faces['R'][0][1], self.faces['R'][1][1]
        self.faces['R'][0][1], self.faces['R'][1][1] = self.faces['D'][1][1], self.faces['D'][1][0]
        self.faces['D'][1][1], self.faces['D'][1][0] = self.faces['L'][1][0], self.faces['L'][0][0]
        self.faces['L'][1][0], self.faces['L'][0][0] = temp[0], temp[1]

    def rotate_B_prime(self):
        self.rotate_face_prime('B')
        temp = [self.faces['U'][0][0], self.faces['U'][0][1]]
        self.faces['U'][0][0], self.faces['U'][0][1] = self.faces['L'][1][0], self.faces['L'][0][0]
        self.faces['L'][1][0], self.faces['L'][0][0] = self.faces['D'][1][1], self.faces['D'][1][0]
        self.faces['D'][1][1], self.faces['D'][1][0] = self.faces['R'][0][1], self.faces['R'][1][1]
        self.faces['R'][0][1], self.faces['R'][1][1] = temp[0], temp[1]

    def rotate_L(self):
        self.rotate_face('L')
        temp = [self.faces['U'][0][0], self.faces['U'][1][0]]
        self.faces['U'][0][0], self.faces['U'][1][0] = self.faces['B'][1][1], self.faces['B'][0][1]
        self.faces['B'][1][1], self.faces['B'][0][1] = self.faces['D'][0][0], self.faces['D'][1][0]
        self.faces['D'][0][0], self.faces['D'][1][0] = self.faces['F'][0][0], self.faces['F'][1][0]
        self.faces['F'][0][0], self.faces['F'][1][0] = temp[0], temp[1]

    def rotate_L_prime(self):
        self.rotate_face_prime('L')
        temp = [self.faces['U'][0][0], self.faces['U'][1][0]]
        self.faces['U'][0][0], self.faces['U'][1][0] = self.faces['F'][0][0], self.faces['F'][1][0]
        self.faces['F'][0][0], self.faces['F'][1][0] = self.faces['D'][0][0], self.faces['D'][1][0]
        self.faces['D'][0][0], self.faces['D'][1][0] = self.faces['B'][1][1], self.faces['B'][0][1]
        self.faces['B'][1][1], self.faces['B'][0][1] = temp[0], temp[1]

    def rotate_R(self):
        self.rotate_face('R')
        temp = [self.faces['U'][0][1], self.faces['U'][1][1]]
        self.faces['U'][0][1], self.faces['U'][1][1] = self.faces['F'][0][1], self.faces['F'][1][1]
        self.faces['F'][0][1], self.faces['F'][1][1] = self.faces['D'][0][1], self.faces['D'][1][1]
        self.faces['D'][0][1], self.faces['D'][1][1] = self.faces['B'][1][0], self.faces['B'][0][0]
        self.faces['B'][1][0], self.faces['B'][0][0] = temp[0], temp[1]

    def rotate_R_prime(self):
        self.rotate_face_prime('R')
        temp = [self.faces['U'][0][1], self.faces['U'][1][1]]
        self.faces['U'][0][1], self.faces['U'][1][1] = self.faces['B'][1][0], self.faces['B'][0][0]
        self.faces['B'][1][0], self.faces['B'][0][0] = self.faces['D'][0][1], self.faces['D'][1][1]
        self.faces['D'][0][1], self.faces['D'][1][1] = self.faces['F'][0][1], self.faces['F'][1][1]
        self.faces['F'][0][1], self.faces['F'][1][1] = temp[0], temp[1]

    def rotate(self, face):
        if face == '':
            return
        elif face == 'U':
            self.rotate_U()
        elif face == 'U\'':
            self.rotate_U_prime()
        elif face == 'D':
            self.rotate_D()
        elif face == 'D\'':
            self.rotate_D_prime()
        elif face == 'F':
            self.rotate_F()
        elif face == 'F\'':
            self.rotate_F_prime()
        elif face == 'B':
            self.rotate_B()
        elif face == 'B\'':
            self.rotate_B_prime()
        elif face == 'L':
            self.rotate_L()
        elif face == 'L\'':
            self.rotate_L_prime()
        elif face == 'R':
            self.rotate_R()
        elif face == 'R\'':
            self.rotate_R_prime()

    def cube_value(self):
        return self.piece_value()

    def piece_value(self):
        mismatch_count = 0
        for i in range(2):
            for j in range(2):
                if self.faces['U'][i][j] != 'W':
                    mismatch_count += 3
                else:
                    solved = self.check_upper_piece(i, j)
                    if not solved:
                        mismatch_count += 2

                if self.faces['D'][i][j] == 'W':
                    mismatch_count += 1
        return mismatch_count


    def sticker_value(self):
       solved_state = {
           'U': [['W', 'W'], ['W', 'W']],
           'D': [['Y', 'Y'], ['Y', 'Y']],
           'F': [['G', 'G'], ['G', 'G']],
           'B': [['B', 'B'], ['B', 'B']],
           'L': [['O', 'O'], ['O', 'O']],
           'R': [['R', 'R'], ['R', 'R']]
       }

       current_state = self.faces
       mismatch_count = 0

       for face in solved_state:
           for i in range(2):
               for j in range(2):
                   if current_state[face][i][j] != solved_state[face][i][j]:
                       mismatch_count += 1

       return mismatch_count

    def is_white_face_solved(self):
        for i in range(2):
            for j in range(2):
                if self.faces['U'][i][j] != 'W':
                    return False
                else:
                    solved = self.check_upper_piece(i, j)
                    if not solved:
                        return False

        return True

    def check_upper_piece(self, i, j):
        if i == 0 and j == 0:
            return self.faces['B'][0][1] == 'B' and self.faces['L'][0][0] == 'O'
        elif i == 0 and j == 1:
            return self.faces['B'][0][0] == 'B' and self.faces['R'][0][1] == 'R'
        elif i == 1 and j == 0:
            return self.faces['F'][0][0] == 'G' and self.faces['L'][0][1] == 'O'
        elif i == 1 and j == 1:
            return self.faces['F'][0][1] == 'G' and self.faces['R'][0][0] == 'R'

    def is_laterals_solved(self):
        for face in ['F', 'B', 'L', 'R']:
            color = self.faces[face][0][0]
            if not all(self.faces[face][i][j] == color for i in range(2) for j in range(2)):
                return False
        return True




    def is_solved(self):
        solved_state = {
            'U': [['W', 'W'], ['W', 'W']],
            'D': [['Y', 'Y'], ['Y', 'Y']],
            'F': [['G', 'G'], ['G', 'G']],
            'B': [['B', 'B'], ['B', 'B']],
            'L': [['O', 'O'], ['O', 'O']],
            'R': [['R', 'R'], ['R', 'R']]
        }

        current_state = {
            'U': self.faces['U'],
            'D': self.faces['D'],
            'F': self.faces['F'],
            'B': self.faces['B'],
            'L': self.faces['L'],
            'R': self.faces['R']
        }

        for face in solved_state:
            for i in range(2):
                for j in range(2):
                    if current_state[face][i][j] != solved_state[face][i][j]:
                        return False

        return True


    def __lt__(self, other):
        """
        Compares two cube objects based on the number of stickers in the correct position.
        Returns True if the current cube has fewer stickers in the correct position than the other cube.
        """
        return self.cube_value() < other.cube_value()

    def __str__(self):
        return str(self.display())

    def set_last_movement(self, last_movement):
        self.last_movement = last_movement

    def get_last_movement(self):
        return self.last_movement

    def get_posibles_steps(self, last_movement = ""):
        moves = {
            'U': CubeRubik2x2.rotate_U,
            'U\'': CubeRubik2x2.rotate_U_prime,
            'D': CubeRubik2x2.rotate_D,
            'D\'': CubeRubik2x2.rotate_D_prime,
            'F': CubeRubik2x2.rotate_F,
            'F\'': CubeRubik2x2.rotate_F_prime,
            'B': CubeRubik2x2.rotate_B,
            'B\'': CubeRubik2x2.rotate_B_prime,
            'L': CubeRubik2x2.rotate_L,
            'L\'': CubeRubik2x2.rotate_L_prime,
            'R': CubeRubik2x2.rotate_R,
            'R\'': CubeRubik2x2.rotate_R_prime
        }

        inverse_moves = {
            'U': 'U\'', 'U\'': 'U',
            'D': 'D\'', 'D\'': 'D',
            'F': 'F\'', 'F\'': 'F',
            'B': 'B\'', 'B\'': 'B',
            'L': 'L\'', 'L\'': 'L',
            'R': 'R\'', 'R\'': 'R'
        }

        cubes = []
        for move, action in moves.items():
            if last_movement != inverse_moves.get(move, ''):
                cube = self.copy()
                action(cube)
                cube.set_last_movement(move)
                cubes.append(cube)
        return cubes

    def display(self):
        result = {}
        for face, grid in self.faces.items():
            result[face] = [' '.join(row) for row in grid]
        return result
