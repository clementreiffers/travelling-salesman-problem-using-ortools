# import logging as log
import sys

import numpy as np
import pandas as pd
from ortools.linear_solver import pywraplp


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

    # on détermine le nombre de nœuds
    nombre_de_villes = distances.shape[0]
    all_nodes = range(nombre_de_villes)
    all_but_first_nodes = range(1, nombre_de_villes)

    # Create the model.
    solver_name = 'SCIP'
    model = pywraplp.Solver.CreateSolver(solver_name)
    model.EnableOutput()

    # generating decision variables X_ij
    x = {}
    for i in all_nodes:
        for j in all_nodes:
            x[(i, j)] = model.BoolVar('x_i%ij%i' % (i, j))

    u = {i: model.IntVar(0, nombre_de_villes, 'u_i%i' % i) for i in all_nodes}
    # constraint 1: leave every point exactly once
    for i in all_nodes:
        model.Add(sum(x[(i, j)] for j in all_nodes) == 1)

    # constraint 2: reach every point from exactly one other point
    # log.info(f'Creating {str(nombre_de_villes)} Constraint 2... ')
    for j in all_nodes:
        model.Add(sum(x[(i, j)] for i in all_nodes) == 1)

    # constraint 3.1: subtour elimination constraints (Miller-Tucker-Zemlin) part 1
    model.Add(u[0] == 1)

    # constraint 3.2: subtour elimination constraints (Miller-Tucker-Zemlin) part 2
    for i in all_but_first_nodes:
        model.Add(u[i] >= 2)
        model.Add(u[i] <= nombre_de_villes)

    # constraint 3.3: subtour elimination constraints (Miller-Tucker-Zemlin) part 3
    for i in all_but_first_nodes:
        for j in all_but_first_nodes:
            model.Add(u[i] - u[j] + 1 <= (nombre_de_villes - 1) * (1 - x[(i, j)]))

    # Minimize the total distance
    model.Minimize(sum(x[(i, j)] * distances[(i, j)] for i in all_nodes for j in all_nodes))

    # log.info('Solving MIP model... ')
    status = model.Solve()

    return u, model, status


def print_solution(u):
    num_nodes = len(u)
    all_nodes = range(num_nodes)
    for i in all_nodes:
        print(f'u({str(i)})={int(u[i].solution_value())}')


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
        print_solution(u)
    elif status == pywraplp.Solver.INFEASIBLE:
        print("le probleme n'est pas solvable")
    else:
        print(f"le probleme n'a pas pu être resolu, le probleme est : {status}")


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    main()
