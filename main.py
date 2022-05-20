import logging as log
import sys

import numpy as np
# also required packages: openpyxl
from ortools.linear_solver import pywraplp


def solve_OrTools(dima:np.ndarray):
    """
    :param dima: the distance matrix
    :return:  solution X, model, status
    """

    if dima.ndim != 2 or dima.shape[0] != dima.shape[1]:
        raise ValueError("Invalid dima dimensions detected. Square matrix expected.")

    # determine number of nodes
    num_nodes = dima.shape[0]
    all_nodes = range(num_nodes)
    all_but_first_nodes = range(1, num_nodes)

    # Create the model.
    solver_name = 'SCIP'
    log.info(f'Instantiating solver {solver_name}')
    model = pywraplp.Solver.CreateSolver(solver_name)
    model.EnableOutput()

    log.info('Defining MIP model... ')
    # generating decision variables X_ij
    log.info(f'Creating {str(num_nodes * num_nodes)} boolean x_ij variables... ')
    x = {}
    for i in all_nodes:
        for j in all_nodes:
            x[(i, j)] = model.BoolVar('x_i%ij%i' % (i, j))

    log.info(f'Creating {str(num_nodes)} boolean u_i variables... ')
    u = {i: model.IntVar(0, num_nodes, 'u_i%i' % i) for i in all_nodes}
    # constraint 1: leave every point exactly once
    log.info(f'Creating {str(num_nodes)} Constraint 1... ')
    for i in all_nodes:
        model.Add(sum(x[(i, j)] for j in all_nodes) == 1)

    # constraint 2: reach every point from exactly one other point
    log.info(f'Creating {str(num_nodes)} Constraint 2... ')
    for j in all_nodes:
        model.Add(sum(x[(i, j)] for i in all_nodes) == 1)

    # constraint 3.1: subtour elimination constraints (Miller-Tucker-Zemlin) part 1
    log.info('Creating 1 Constraint 3.1... ')
    model.Add(u[0] == 1)

    # constraint 3.2: subtour elimination constraints (Miller-Tucker-Zemlin) part 2
    log.info(f'Creating {len(all_but_first_nodes)} Constraint 3.2... ')
    for i in all_but_first_nodes:
        model.Add(u[i] >= 2)
        model.Add(u[i] <= num_nodes)

    # constraint 3.3: subtour elimination constraints (Miller-Tucker-Zemlin) part 3
    log.info(f'Creating {len(all_but_first_nodes)} Constraint 3.2... ')
    for i in all_but_first_nodes:
        for j in all_but_first_nodes:
            model.Add(u[i] - u[j] + 1 <= (num_nodes - 1) * (1 - x[(i, j)]))

    # Minimize the total distance
    model.Minimize(sum(x[(i, j)] * dima[(i, j)] for i in all_nodes for j in all_nodes))

    log.info('Solving MIP model... ')
    status = model.Solve()

    return u, model, status


def print_solution(u):
    num_nodes = len(u)
    all_nodes = range(num_nodes)
    for i in all_nodes:
        log.info(f'u({str(i)})={int(u[i].solution_value())}')


def main():
    # configure logger for info level
    log.basicConfig(
        format='%(asctime)s %(levelname)-8s %(message)s',
        level=log.INFO,
        datefmt='%Y-%m-%d %H:%M:%S',
        stream=sys.stdout)

    dima = np.array([
        [0, 3, 657, 2326, 464, 2724, 1375, 713, 598, 67, 705, 442, 105, 1893, 1343, 3157, 2067],
        [3, 0, 654, 2326, 467, 2721, 1376, 716, 599, 64, 708, 443, 102, 1891, 1345, 3156, 2067],
        [657, 654, 0, 2124, 960, 2130, 1602, 1165, 1166, 629, 1151, 1040, 555, 1329, 1597, 2624,
         1912],
        [2326, 2326, 2124, 0, 2074, 3439, 1393, 1965, 2892, 2366, 1956, 2729, 2301, 1450, 1459,
         1678, 285],
        [464, 467, 960, 2074, 0, 3090, 947, 249, 855, 531, 242, 702, 534, 1959, 907, 3144, 1797],
        [2724, 2721, 2130, 3439, 3090, 0, 3608, 3293, 3015, 2673, 3279, 2963, 2621, 1990, 3623,
         2663, 3384],
        [1375, 1376, 1602, 1393, 947, 3608, 0, 734, 1788, 1438, 732, 1642, 1411, 1967, 66, 2854,
         1114],
        [713, 716, 1165, 1965, 249, 3293, 734, 0, 1055, 780, 16, 913, 781, 2032, 686, 3158, 1682],
        [598, 599, 1166, 2892, 855, 3015, 1788, 1055, 0, 584, 1056, 163, 665, 2469, 1741, 3746,
         2623],
        [67, 64, 629, 2366, 531, 2673, 1438, 780, 584, 0, 772, 435, 82, 1891, 1407, 3163, 2110],
        [705, 708, 1151, 1956, 242, 3279, 732, 16, 1056, 772, 0, 912, 771, 2017, 686, 3144, 1673],
        [442, 443, 1040, 2729, 702, 2963, 1642, 913, 163, 435, 912, 0, 517, 2326, 1598, 3597, 2461],
        [105, 102, 555, 2301, 534, 2621, 1411, 781, 665, 82, 771, 517, 0, 1809, 1384, 3081, 2048],
        [1893, 1891, 1329, 1450, 1959, 1990, 1967, 2032, 2469, 1891, 2017, 2326, 1809, 0, 2008,
         1298, 1418],
        [1343, 1345, 1597, 1459, 907, 3623, 66, 686, 1741, 1407, 686, 1598, 1384, 2008, 0, 2912,
         1180],
        [3157, 3156, 2624, 1678, 3144, 2663, 2854, 3158, 3746, 3163, 3144, 3597, 3081, 1298, 2912,
         0, 1862],
        [2067, 2067, 1912, 285, 1797, 3384, 1114, 1682, 2623, 2110, 1673, 2461, 2048, 1418, 1180,
         1862, 0]
    ])

    # now solve problem
    u, model, status = solve_OrTools(dima)

    # check problem response
    if status == pywraplp.Solver.OPTIMAL:
        log.info('Solution:')
        log.info('optimal solution found.')
        log.info(f'Objective value ={str(model.Objective().Value())}')
        print_solution(u)
    elif status == pywraplp.Solver.INFEASIBLE:
        log.info('The problem is infeasible.')
    else:
        log.info(f'The problem could not be solved. Return state was: {status}')


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    main()
