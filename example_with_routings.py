from ortools.constraint_solver import pywrapcp, routing_enums_pb2

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


def create_data_model():
    """Stores the data for the problem."""
    return {
        'distance_matrix': [[0, 3, 657, 2326, 464, 2724, 1375, 713, 598, 67, 705, 442, 105, 1893, 1343, 3157, 2067],
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
                            ],
        'num_vehicles': 1,
        'depot': 0
    }


def print_solution(manager, routing, solution):
    """Prints solution on console."""
    print(f'Objective: {solution.ObjectiveValue()} miles')
    index = routing.Start(0)
    plan_output = 'Route for vehicle 0:\n'
    route_distance = 0
    while not routing.IsEnd(index):
        plan_output += f' {manager.IndexToNode(index)} ->'
        previous_index = index
        index = solution.Value(routing.NextVar(index))
        route_distance += routing.GetArcCostForVehicle(previous_index, index, 0)
    plan_output += ' {}\n'.format(manager.IndexToNode(index))
    print(plan_output)
    plan_output += 'Route distance: {}miles\n'.format(route_distance)


def main():
    """Entry point of the program."""
    # Instantiate the data problem.
    data = create_data_model()

    # Create the routing index manager.
    manager = pywrapcp.RoutingIndexManager(len(data['distance_matrix']),
                                           data['num_vehicles'], data['depot'])

    # Create Routing Model.
    routing = pywrapcp.RoutingModel(manager)

    def distance_callback(from_index, to_index):
        """Returns the distance between the two nodes."""
        # Convert from routing variable Index to distance matrix NodeIndex.
        from_node = manager.IndexToNode(from_index)
        to_node = manager.IndexToNode(to_index)
        return data['distance_matrix'][from_node][to_node]

    transit_callback_index = routing.RegisterTransitCallback(distance_callback)

    # Define cost of each arc.
    routing.SetArcCostEvaluatorOfAllVehicles(transit_callback_index)

    # Setting first solution heuristic.
    search_parameters = pywrapcp.DefaultRoutingSearchParameters()
    search_parameters.first_solution_strategy = (
        routing_enums_pb2.FirstSolutionStrategy.PATH_CHEAPEST_ARC)

    # Solve the problem.
    solution = routing.SolveWithParameters(search_parameters)

    # Print solution on console.
    if solution:
        print_solution(manager, routing, solution)


if __name__ == '__main__':
    main()
