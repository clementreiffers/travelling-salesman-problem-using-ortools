# travelling_salesman_problem_lp

Travelling salesman problem solver using linear programming with Google Or-Tools.

## Description

The Travelling Salesman Problem also known as TSP is an NP-hard problem in combinatorial optimization.  
Imagine a set of city disposed on a map, you have a set of salesman (population) and they must all go to every city in
the least amount of time/distance.  
The optimization solution is the one where a salesman goes through all the cities with the least distance or/and time.

In the image below you can see a representation of the tsp problem with cities named A, B, C, D. Going from a city to
another take more or less time than other depending on the distance.

<p align="center">
    <img src="https://user-images.githubusercontent.com/59691442/165635831-5bfc72b5-0dd3-4a9f-afb0-b5ffd402ee88.png" alt="tspExampleImage" style="height:400px"/>
</p>

## Problem modelisation

Below is the problem modelisation in Linear Programming.

<p align="center">
    <img src="https://user-images.githubusercontent.com/59691442/169556846-231900f0-2195-478d-be14-0990f52ea1b4.png" alt="tspExampleImage" style="height:400px"/>
</p>

## Quick start

You need python3 to start the app. you also need some packages that are listed in the `requirements.txt`.  
To install them all type the following command :

```terminal
pip install -r requirements.txt
```

You can then start the program by double-clicking the main.py file.

If you want to change the excel file to use or change the city to begin with in your tsp. Just change the last line of the main.py file.

```py
if __name__ == '__main__':
    main("Sydney", "data.xlsx")
```

by

```py
if __name__ == '__main__':
    main("example_city", "example.xlsx")
```

## Program implementation

## Algorithm

The program is made only of one file, the "main.py" file.

The python file load the dataset and then proceed all the linear programming calculs.

## Excel data

Our project contains a excel file that is load by our app.
The excel contains the distances of all cities relativeness from each other.

**CSV Example :**

|  |M.C.G.|Docklands|Adelaide Oval|
|--|--|--|--|
|M.C.G.|  0| 3 |657 |
|Docklands| 3|0 |654 |
|Adelaide Oval| 657|654|0|

The excel is loaded in our app and it will search the city by the name you set in the variable `city_origin_name`. This name will be used to move the row of the city at the beginning of our project.

For example, if you want to begin your travel from Adelaide Oval, the data will look like below :

**CSV Example :**

|  |M.C.G.|Docklands|Adelaide Oval|
|--|--|--|--|
|Adelaide Oval| 657|654|0|
|M.C.G.|  0| 3 |657 |
|Docklands| 3|0 |654 |

### Linear Programming

Linear programming implementation is completely set in the solve_OrTools function.

Below is a part of the function solve_OrTools :

```py
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
```

## Routing implementation

To verify the app output result. We create a file named `example_with_routings.py` that will solve our tsp problem but by using routing.

Output placeholder.

## Contributors

Clément Reiffers :

- @clementreiffers
- <https://github.com/clementreiffers>

Quentin Morel :

- @Im-Rises
- <https://github.com/Im-Rises>

Adrien Tirlemont :

- @Meatisdelicious
- <https://github.com/Meatisdelicious>

## Documentations and API

Google Or-Tools :  
<https://developers.google.com/optimization/>

TSP solvers Or-Tools :
<https://developers.google.com/optimization/routing/tsp>

TSP Linear Programming solver :  
<https://hal.archives-ouvertes.fr/hal-02947086/document>
