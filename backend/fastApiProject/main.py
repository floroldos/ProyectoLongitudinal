import heapq as pq
import re

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from Rubik2x2 import CubeRubik2x2

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/averageM")
async def averageM():
    with open("log2.txt", "r") as file:
        lines = file.readlines()
        total = 0
        count = 0
        for line in lines:
            moves = re.search(r'\d+', line)
            if moves:
                moves = int(moves.group(0))
                if moves > 0:
                    total += moves
                    count += 1
        if count > 0:
            return {"average": total / count}
        else:
            return {"average": 0}

@app.get("/resolve/")
async def resolve():
    current_cube = CubeRubik2x2()
    steps_to_shuffle = ['L', 'U', "U'", "R'", "D'", "R", "L'", "U", "R", "U'", "D'", "D'", "B'", "F'", "L'", "B", "R", "B'", "U'", "U"]
    for step in steps_to_shuffle:
        current_cube.rotate(step)

    steps_to_solve = ['U', "D'", "B'", 'U', 'U', 'U', 'D', 'D', 'D', 'U', 'U', 'D', 'D', 'D', 'U', 'U', 'D', 'D', 'D', 'U', 'U', 'D', 'D', 'U', 'L', "U'", "F'", 'D', "L'", 'D', 'L', "D'", 'F', "D'", "F'"]
    for step in steps_to_solve:
        current_cube.rotate(step)
        print(current_cube.display())


@app.get("/resolve/{cube}")
async def resolve(cube: str):
    print("Resolving cube: ", cube)
    current_cube = CubeRubik2x2()

    splitted = cube.split(',')
    for face in splitted:
        current_cube.rotate(face)
        current_cube.set_last_movement(face)

    if current_cube.is_solved():
        return {"message": "Cube already solved", "resolve": [], "state": current_cube.display()}

    steps_to_solve = []
    visited_steps = []

    max_steps = 15000
    current_steps = 0

    while True:
        priority_queue = []
        if current_steps >= max_steps:
            return {"message": "Max steps reached", "resolve": steps_to_solve, "state": current_cube.display()}

        # expandir nodos
        posibles_cubes = current_cube.get_posibles_steps()

        for cube_s in posibles_cubes:
            posibles_cubes_of_cubes = cube_s.get_posibles_steps()
            for cube_of_cube in posibles_cubes_of_cubes:
                if len(cube_s.get_last_movement()) != len(cube_of_cube.get_last_movement()) and (cube_s.get_last_movement().find(cube_of_cube.get_last_movement()) != -1 or cube_of_cube.get_last_movement().find(cube_s.get_last_movement()) != -1):
                    continue
                posibles_cubes_of_cubes_of_cubes = cube_of_cube.get_posibles_steps()
                for cube_of_cube_of_cube in posibles_cubes_of_cubes_of_cubes:
                    if len(cube_of_cube.get_last_movement()) != len(cube_of_cube_of_cube.get_last_movement()) and (cube_of_cube.get_last_movement().find(cube_of_cube_of_cube.get_last_movement()) != -1 or cube_of_cube_of_cube.get_last_movement().find(cube_of_cube.get_last_movement()) != -1):
                        continue
                    posibles_cubes_of_cubes_of_cubes_of_cubes = cube_of_cube_of_cube.get_posibles_steps()
                    for cube_of_cube_of_cube_of_cube in posibles_cubes_of_cubes_of_cubes_of_cubes:
                        if len(cube_of_cube_of_cube.get_last_movement()) != len(cube_of_cube_of_cube_of_cube.get_last_movement()) and ((cube_of_cube_of_cube.get_last_movement().find(cube_of_cube_of_cube_of_cube.get_last_movement()) != -1) or (cube_of_cube_of_cube_of_cube.get_last_movement().find(cube_of_cube_of_cube.get_last_movement()) != -1)):
                            continue
                        cube_of_cube_of_cube_of_cube.set_last_movement(
                            cube_s.get_last_movement() + "," + cube_of_cube.get_last_movement() + "," + cube_of_cube_of_cube.get_last_movement() + "," + cube_of_cube_of_cube_of_cube.get_last_movement())
                        pq.heappush(priority_queue, cube_of_cube_of_cube_of_cube)
                    cube_of_cube_of_cube.set_last_movement(cube_s.get_last_movement() + "," + cube_of_cube.get_last_movement() + "," + cube_of_cube_of_cube.get_last_movement())
                    pq.heappush(priority_queue, cube_of_cube_of_cube)
                cube_of_cube.set_last_movement(cube_s.get_last_movement() + "," + cube_of_cube.get_last_movement())
                pq.heappush(priority_queue, cube_of_cube)
            pq.heappush(priority_queue, cube_s)

        visited = True
        while visited:
            current_cube = pq.heappop(priority_queue)
            if current_cube.display() not in visited_steps:
                visited = False
            elif len(priority_queue) == 0:
                print(len(visited_steps))
                return {"message": "Error in visited!", "resolve": steps_to_solve, "state": current_cube.display()}

        visited_steps.append(current_cube.display())

        splitted = current_cube.get_last_movement().split(",")

        for s in splitted:
            steps_to_solve.append(s)

        if current_cube.is_white_face_solved():
            break

    print("Cara blanca resuelta...")
    # | ← indica un caracter sentinela para el front poner un mensaje y no aplicar un movimiento!
    steps_to_solve.append("|Cara blanca resuelta")

    if current_cube.is_solved():
        return returnCube(cube, current_cube, steps_to_solve)

    yellow_solved = False

    if current_cube.is_solved():
        yellow_solved = True

    if current_cube.faces['D'][1][0] == 'Y':
        yellow_resolved = 0
        for i in range(2):
            for j in range(2):
                if current_cube.faces['D'][i][j] == 'Y':
                    yellow_resolved += 1

        if yellow_resolved == 4:
            yellow_solved = True

    if not yellow_solved:
        while not yellow_solved:

            while current_cube.faces['D'][0][1] == 'Y':
                current_cube.rotate_D_prime()
                steps_to_solve.append("D'")

            while current_cube.faces['D'][0][1] != 'Y':
                current_cube.rotate_R()
                steps_to_solve.append("R")
                current_cube.rotate_U()
                steps_to_solve.append("U")
                current_cube.rotate_R_prime()
                steps_to_solve.append("R'")
                current_cube.rotate_U_prime()
                steps_to_solve.append("U'")

            yellow_resolved = 0
            for i in range(2):
                for j in range(2):
                    if current_cube.faces['D'][i][j] == 'Y':
                        yellow_resolved += 1

            if yellow_resolved == 4:
                yellow_solved = True

    # Amarrillo resuelto

    print("Cara amarilla resuelta...")
    white_solved_check = current_cube.is_white_face_solved()
    if not white_solved_check:
        for i in range(2):
            current_cube.rotate_U()
            steps_to_solve.append("U")
            if current_cube.is_white_face_solved():
                white_solved_check = True
                break
    if not white_solved_check:
        steps_to_solve.pop()
        steps_to_solve.pop()

        for i in range(2):
            current_cube.rotate_U_prime()
            steps_to_solve.append("U'")
            if current_cube.is_white_face_solved():
                break

    steps_to_solve.append("|Cara amarilla resuelta")

    if current_cube.is_solved():
        return returnCube(cube, current_cube, steps_to_solve)

    is_solved = False
    corner_correct = False
    posible_partial_solved = current_cube.copy()
    if (current_cube.faces['R'][1][0] == "R" and current_cube.faces['F'][1][1] == "G" and current_cube.faces['B'][1][
        1] == "B" and current_cube.faces['L'][1][0] == "O") or (
            current_cube.faces['R'][1][1] == "R" and current_cube.faces['B'][1][0] == "B" and
            current_cube.faces['B'][1][1] == "B" and current_cube.faces['L'][1][0] == "O"):
        corner_correct = True
    posibles_cubes = current_cube.get_posibles_steps()

    # ELIJE UNA ESQUINA RESUELTA ANTES QUE UNA CARA RESUELTA PORQUE LA ENCUENTRA ANTES,
    # A VECES ENCUENTRA POR EJEMPLO YENDO HACIA LA IZQUIERDA CON UN MOVIMIENTO SOLO LA ESQUINA EN SU LUGAR CUANDO AVANZANDO HACIA LA DERECHA CON DOS MOVIMIENTOS SE LLEGA A LA CARA RESUELTA.
    for cube_s in posibles_cubes:
        if is_solved:
            break

        if cube_s.faces['R'][0][0] != 'R' or cube_s.faces['R'][0][1] != 'R' or cube_s.faces['D'] != [['Y', 'Y'], ['Y', 'Y']]:
            continue

        if cube_s.faces['F'] == [['G', 'G'], ['G', 'G']] and cube_s.faces['L'] == [['O', 'O'], ['O', 'O']] and \
                cube_s.faces['B'] == [['B', 'B'], ['B', 'B']] and cube_s.faces['R'] == [['R', 'R'], ['R', 'R']]:
            steps_to_solve.append(cube_s.get_last_movement())
            current_cube.rotate(cube_s.get_last_movement())
            print("Verde, Naranja, Azul y Rojo resueltos")
            is_solved = True
            break
        if (cube_s.faces['R'][1][0] == "R" and cube_s.faces['F'][1][1] == "G" and cube_s.faces['B'][1][
        1] == "B" and cube_s.faces['L'][1][0] == "O") or (
            cube_s.faces['R'][1][1] == "R" and cube_s.faces['B'][1][0] == "B" and
            cube_s.faces['B'][1][1] == "B" and cube_s.faces['L'][1][0] == "O"):
            posible_partial_solved = cube_s.copy()
            posible_partial_solved.set_last_movement(cube_s.get_last_movement())
            corner_correct = True

        if cube_s.faces['F'] == [['G', 'G'], ['G', 'G']]:
            steps_to_solve.append(cube_s.get_last_movement())
            current_cube.rotate(cube_s.get_last_movement())

            finalAlgorithm("F", current_cube, steps_to_solve)
            current_cube.rotate("D'")
            steps_to_solve.append("D'")

            is_solved = True
            print("Verde resuelto")
            break

        elif cube_s.faces['L'] == [['O', 'O'], ['O', 'O']]:
            steps_to_solve.append(cube_s.get_last_movement())
            current_cube.rotate(cube_s.get_last_movement())
            finalAlgorithm("L", current_cube, steps_to_solve)
            current_cube.rotate_D_prime()
            steps_to_solve.append("D'")

            is_solved = True
            print("Naranja resuelto")
            break

        elif cube_s.faces['B'] == [['B', 'B'], ['B', 'B']]:
            steps_to_solve.append(cube_s.get_last_movement())
            current_cube.rotate(cube_s.get_last_movement())

            finalAlgorithm("B", current_cube, steps_to_solve)
            current_cube.rotate("D'")
            steps_to_solve.append("D'")
            print("Azul resuelto")
            is_solved = True
            break

        elif cube_s.faces['R'] == [['R', 'R'], ['R', 'R']]:
            steps_to_solve.append(cube_s.get_last_movement())
            current_cube.rotate(cube_s.get_last_movement())
            finalAlgorithm("R", current_cube, steps_to_solve)
            current_cube.rotate("D'")
            steps_to_solve.append("D'")
            is_solved = True
            print("Rojo resuelto")
            break
        else:
            posibles_cubes_of_cubes = cube_s.get_posibles_steps()
            for cube_of_cube in posibles_cubes_of_cubes:
                if cube_of_cube.faces['R'][0][0] != 'R' or cube_of_cube.faces['R'][0][1] != 'R' or cube_of_cube.faces['D'] != [['Y', 'Y'], ['Y', 'Y']]:
                    continue
                # Si rojo resuelto
                if cube_of_cube.faces['R'] == [['R', 'R'], ['R', 'R']] and cube_of_cube.faces['B'] == [['B', 'B'],
                                                                                                       ['B', 'B']] and \
                        cube_of_cube.faces['L'] == [['O', 'O'], ['O', 'O']] and cube_of_cube.faces['F'] == [['G', 'G'],
                                                                                                            ['G', 'G']]:
                    steps_to_solve.append(cube_s.get_last_movement())
                    steps_to_solve.append(cube_of_cube.get_last_movement())
                    current_cube.rotate(cube_s.get_last_movement())
                    current_cube.rotate(cube_of_cube.get_last_movement())
                    print("Rojo, Azul, Naranja y Verde resueltos")
                    is_solved = True
                    break

                elif cube_of_cube.faces['R'] == [['R', 'R'], ['R', 'R']]:
                    steps_to_solve.append(cube_s.get_last_movement())
                    steps_to_solve.append(cube_of_cube.get_last_movement())
                    current_cube.rotate(cube_s.get_last_movement())
                    current_cube.rotate(cube_of_cube.get_last_movement())

                    # B' L B' R R B L' B' R R B B D'
                    finalAlgorithm("R", current_cube, steps_to_solve)
                    current_cube.rotate("D'")
                    steps_to_solve.append("D'")
                    is_solved = True
                    print("Rojo resuelto")
                    break

                # Si azul resuelto
                elif cube_of_cube.faces['B'] == [['B', 'B'], ['B', 'B']]:
                    steps_to_solve.append(cube_s.get_last_movement())
                    steps_to_solve.append(cube_of_cube.get_last_movement())
                    current_cube.rotate(cube_s.get_last_movement())
                    current_cube.rotate(cube_of_cube.get_last_movement())

                    finalAlgorithm("B", current_cube, steps_to_solve)
                    current_cube.rotate("D'")
                    steps_to_solve.append("D'")

                    is_solved = True
                    print("Azul resuelto")
                    break

                # Si naranja resuelto
                elif cube_of_cube.faces['L'][0][0] == 'O' and cube_of_cube.faces['L'][0][1] == 'O' and \
                        cube_of_cube.faces['L'][1][0] == 'O' and \
                        cube_of_cube.faces['L'][1][1] == 'O':
                    steps_to_solve.append(cube_s.get_last_movement())
                    steps_to_solve.append(cube_of_cube.get_last_movement())
                    current_cube.rotate(cube_s.get_last_movement())
                    current_cube.rotate(cube_of_cube.get_last_movement())

                    finalAlgorithm("L", current_cube, steps_to_solve)
                    current_cube.rotate("D'")
                    steps_to_solve.append("D'")

                    is_solved = True
                    print("Naranja resuelto")
                    break

                # Si verde resuelto
                elif cube_of_cube.faces['F'][0][0] == 'G' and cube_of_cube.faces['F'][0][1] == 'G' and \
                        cube_of_cube.faces['F'][1][0] == 'G' and \
                        cube_of_cube.faces['F'][1][1] == 'G':
                    steps_to_solve.append(cube_s.get_last_movement())
                    steps_to_solve.append(cube_of_cube.get_last_movement())
                    current_cube.rotate(cube_s.get_last_movement())
                    current_cube.rotate(cube_of_cube.get_last_movement())

                    finalAlgorithm("F", current_cube, steps_to_solve)
                    current_cube.rotate("D'")
                    steps_to_solve.append("D'")

                    is_solved = True
                    print("Verde resuelto")
                    break
                elif (cube_of_cube.faces['R'][1][0] == "R" and cube_of_cube.faces['F'][1][1] == "G" and cube_of_cube.faces['B'][1][1] == "B" and cube_of_cube.faces['L'][1][0] == "O") or (
            cube_of_cube.faces['R'][1][1] == "R" and cube_of_cube.faces['B'][1][0] == "B" and
            cube_of_cube.faces['B'][1][1] == "B" and cube_of_cube.faces['L'][1][0] == "O"):
                    posible_partial_solved = cube_of_cube.copy()
                    posible_partial_solved.set_last_movement(cube_s.get_last_movement() + "," + cube_of_cube.get_last_movement())
                    corner_correct = True
                    break
    if not is_solved and corner_correct:
        print("Hay una esquina bien")
        if posible_partial_solved.faces != current_cube.faces:
            steps = posible_partial_solved.get_last_movement().split(",")
            print("Pasos para resolver la esquina bien: ", steps)
            for step in steps:
                current_cube.rotate(step)
                steps_to_solve.append(step)
        # SE TIENE QUE HACER DOS VECES
        finalAlgorithm("R", current_cube, steps_to_solve)

        # DEPENDE DE CUAL CARA QUEDA ARMADA:
        for i in range(2):
            current_cube.rotate("D'")
            steps_to_solve.append("D'")
            if current_cube.faces['F'] == [['G', 'G'], ['G', 'G']]:
                finalAlgorithm("F", current_cube, steps_to_solve)
                current_cube.rotate("D'")
                steps_to_solve.append("D'")
                break
            elif current_cube.faces['L'] == [['O', 'O'], ['O', 'O']]:
                finalAlgorithm("L", current_cube, steps_to_solve)
                current_cube.rotate("D'")
                steps_to_solve.append("D'")
                break
            elif current_cube.faces['B'] == [['B', 'B'], ['B', 'B']]:
                finalAlgorithm("B", current_cube, steps_to_solve)
                current_cube.rotate("D'")
                steps_to_solve.append("D'")
                break
            elif current_cube.faces['R'] == [['R', 'R'], ['R', 'R']]:
                finalAlgorithm("R", current_cube, steps_to_solve)
                current_cube.rotate("D'")
                steps_to_solve.append("D'")
                break
        if not current_cube.is_solved():
            steps_to_solve.pop()
            steps_to_solve.pop()
            current_cube.rotate("D")
            current_cube.rotate("D")
            for i in range(2):
                current_cube.rotate("D")
                steps_to_solve.append("D")
                if current_cube.faces['F'] == [['G', 'G'], ['G', 'G']]:
                    finalAlgorithm("F", current_cube, steps_to_solve)
                    current_cube.rotate("D'")
                    steps_to_solve.append("D'")
                    break
                elif current_cube.faces['L'] == [['O', 'O'], ['O', 'O']]:
                    finalAlgorithm("L", current_cube, steps_to_solve)
                    current_cube.rotate("D'")
                    steps_to_solve.append("D'")
                    break
                elif current_cube.faces['B'] == [['B', 'B'], ['B', 'B']]:
                    finalAlgorithm("B", current_cube, steps_to_solve)
                    current_cube.rotate("D'")
                    steps_to_solve.append("D'")
                    break
                elif current_cube.faces['R'] == [['R', 'R'], ['R', 'R']]:
                    finalAlgorithm("R", current_cube, steps_to_solve)
                    current_cube.rotate("D'")
                    steps_to_solve.append("D'")
                    break

    print(current_cube.display())
    print(steps_to_solve)
    return returnCube(cube, current_cube, steps_to_solve)


def returnCube(cube, current_cube, steps_to_solve):
    steps_to_solve.append("|Cubo resuelto")
    resolve_string = ""
    for step in steps_to_solve:
        resolve_string += step + ","
    with open("log2.txt", "a") as file:
        file.write(cube + " - " + str(len(resolve_string.split(',')) - 1) + "\n")
        file.write("cube: " + str(current_cube) + "\n")

        file.close()

    return {"message": "Cube solved", "steps": len(resolve_string.split(',')), "resolve": resolve_string,
            "state": current_cube.display()}


def finalAlgorithm(faceResolved, current_cube, steps_to_solve):
    if faceResolved == "R":
        current_cube.rotate_B_prime()
        steps_to_solve.append("B'")
        current_cube.rotate_L()
        steps_to_solve.append("L")
        current_cube.rotate_B_prime()
        steps_to_solve.append("B'")
        current_cube.rotate_R()
        steps_to_solve.append("R")
        current_cube.rotate_R()
        steps_to_solve.append("R")
        current_cube.rotate_B()
        steps_to_solve.append("B")
        current_cube.rotate_L_prime()
        steps_to_solve.append("L'")
        current_cube.rotate_B_prime()
        steps_to_solve.append("B'")
        current_cube.rotate_R()
        steps_to_solve.append("R")
        current_cube.rotate_R()
        steps_to_solve.append("R")
        current_cube.rotate_B()
        steps_to_solve.append("B")
        current_cube.rotate_B()
        steps_to_solve.append("B")

    elif faceResolved == "L":
        # F'RF'LLFR'F'LLFF
        current_cube.rotate_F_prime()
        steps_to_solve.append("F'")
        current_cube.rotate_R()
        steps_to_solve.append("R")
        current_cube.rotate_F_prime()
        steps_to_solve.append("F'")
        current_cube.rotate_L()
        steps_to_solve.append("L")
        current_cube.rotate_L()
        steps_to_solve.append("L")
        current_cube.rotate_F()
        steps_to_solve.append("F")
        current_cube.rotate_R_prime()
        steps_to_solve.append("R'")
        current_cube.rotate_F_prime()
        steps_to_solve.append("F'")
        current_cube.rotate_L()
        steps_to_solve.append("L")
        current_cube.rotate_L()
        steps_to_solve.append("L")
        current_cube.rotate_F()
        steps_to_solve.append("F")
        current_cube.rotate_F()
        steps_to_solve.append("F")

    elif faceResolved == "B":
        # L'FL'BBLF'L'BBLL
        current_cube.rotate_L_prime()
        steps_to_solve.append("L'")
        current_cube.rotate_F()
        steps_to_solve.append("F")
        current_cube.rotate_L_prime()
        steps_to_solve.append("L'")
        current_cube.rotate_B()
        steps_to_solve.append("B")
        current_cube.rotate_B()
        steps_to_solve.append("B")
        current_cube.rotate_L()
        steps_to_solve.append("L")
        current_cube.rotate_F_prime()
        steps_to_solve.append("F'")
        current_cube.rotate_L_prime()
        steps_to_solve.append("L'")
        current_cube.rotate_B()
        steps_to_solve.append("B")
        current_cube.rotate_B()
        steps_to_solve.append("B")
        current_cube.rotate_L()
        steps_to_solve.append("L")
        current_cube.rotate_L()
        steps_to_solve.append("L")

    elif faceResolved == "F":
        # R'BR'FFRB'R'FFRR
        current_cube.rotate_R_prime()
        steps_to_solve.append("R'")
        current_cube.rotate_B()
        steps_to_solve.append("B")
        current_cube.rotate_R_prime()
        steps_to_solve.append("R'")
        current_cube.rotate_F()
        steps_to_solve.append("F")
        current_cube.rotate_F()
        steps_to_solve.append("F")
        current_cube.rotate_R()
        steps_to_solve.append("R")
        current_cube.rotate_B_prime()
        steps_to_solve.append("B'")
        current_cube.rotate_R_prime()
        steps_to_solve.append("R'")
        current_cube.rotate_F()
        steps_to_solve.append("F")
        current_cube.rotate_F()
        steps_to_solve.append("F")
        current_cube.rotate_R()
        steps_to_solve.append("R")
        current_cube.rotate_R()
        steps_to_solve.append("R")
