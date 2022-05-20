# import logging as log
import sys

import numpy as np
import pandas as pd
from ortools.linear_solver import pywraplp

cities = {
    0: "M.C.G.",
    1: "Docklands",
    2: "Adelaide Oval",
    3: "Cazaly's Stadium",
    4: "Manuka Oval",
    5: "Perth Stadium",
    6: "Gabba",
    7: "S.C.G.",
    8: "Bellerive Oval",
    9: "Kardinia Park",
    10: "Sydney",
    11: "York Park",
    12: "Eureka Stadium",
    13: "Traeger Park",
    14: "Carrara",
    15: "Marrara Oval",
    16: "Riverway Stadium",
}


def solve_OrTools(distances: np.ndarray):
    """
    :param distances: la matrice avec toutes les distances
    :return:  solution X, model, status
    """
    # on vérifie que la matrice reçue a bien 2 dimensions et après que
    # ses 2 dimensions contiennent le même nombre de distances, car on
    # travaille avec une matrice carrée
    if distances.ndim != 2 and distances.shape[0] != distances.shape[1]:
        raise ValueError("Invalid dima dimensions detected. Square matrix expected.")

    # on détermine le nombre de villes et on cree des variables qui vont servir à itérer dessus
    nombre_de_villes = distances.shape[0]
    index_villes = range(nombre_de_villes)
    index_villes_sauf_premiere = range(1, nombre_de_villes)

    # on cree le modele en mode scip
    model = pywraplp.Solver.CreateSolver('SCIP')
    model.EnableOutput()

    # on génère les variables de decisions sous forme de booleen pour savoir si on passer par cette ville ou pas
    x = {}
    for i in index_villes:
        for j in index_villes:
            x[(i, j)] = model.BoolVar(f"x_i{i}j{j}")

    # on initialise les variables de decision
    u = {i: model.IntVar(0, nombre_de_villes, f"u_i{i}") for i in index_villes}

    # on veut un seul successeur
    for i in index_villes:
        model.Add(sum(x[(i, j)] for j in index_villes) == 1)

    # on veut un seul prédécesseur
    for j in index_villes:
        model.Add(sum(x[(i, j)] for i in index_villes) == 1)

    # constraint 3.1: subtour elimination constraints (Miller-Tucker-Zemlin) part 1
    model.Add(u[0] == 1)

    # constraint 3.2: subtour elimination constraints (Miller-Tucker-Zemlin) part 2
    for i in index_villes_sauf_premiere:
        model.Add(u[i] >= 2)
        model.Add(u[i] <= nombre_de_villes)

    # constraint 3.3: subtour elimination constraints (Miller-Tucker-Zemlin) part 3
    for i in index_villes_sauf_premiere:
        for j in index_villes_sauf_premiere:
            model.Add(u[i] - u[j] + 1 <= (nombre_de_villes - 1) * (1 - x[(i, j)]))

    # on veut que la distance soir la plus petite possible
    model.Minimize(sum(x[(i, j)] * distances[(i, j)] for i in index_villes for j in index_villes))

    status = model.Solve()

    return u, model, status


def print_solution(u, cities):
    num_nodes = len(u)
    all_nodes = range(num_nodes)
    solution = {int(u[i].solution_value()):i for i in all_nodes}
    solution = sorted(solution.items())
    for i in solution:
        print(f"{i[1]}->", end="")
    print(solution[0][1])

def main():
    # Drop useless lines
    df = pd.read_excel("data.xlsx", "sheet1")
    df = df.dropna(how="all")

    # Convert to numpy array and delete cities' name
    test_dima = np.array(df)
    test_dima = np.delete(test_dima, 0, axis=1)
    test_dima = np.delete(test_dima, 0, axis=0)

    dima = test_dima

    # now solve problem
    u, model, status = solve_OrTools(dima)

    # check problem response
    if status == pywraplp.Solver.OPTIMAL:
        print(f'Objective value ={str(model.Objective().Value())}')
        print_solution(u, cities)
    elif status == pywraplp.Solver.INFEASIBLE:
        print("le probleme n'est pas solvable")
    else:
        print(f"le probleme n'a pas pu être resolu, le probleme est : {status}")


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    main()
