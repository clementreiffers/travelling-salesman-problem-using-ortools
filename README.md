# travelling_salesman_problem_lp

Travelling salesman problem solver using linear programming with Google Or-Tools.

## Description

### Travelling Salesman Problem

The Travelling Salesman Problem also known as TSP is an NP-hard problem in combinatorial optimization.  
Imagine a set of city disposed on a map, you have a set of salesman (population) and they must all go to every city in
the least amount of time/distance.  
The optimization solution is the one where a salesman goes through all the cities with the least distance or/and time.

In the image below you can see a representation of the tsp problem with cities named A, B, C, D. Going from a city to
another take more or less time than other depending on the distance.

<p align="center">
    <img src="https://user-images.githubusercontent.com/59691442/165635831-5bfc72b5-0dd3-4a9f-afb0-b5ffd402ee88.png" alt="tspExampleImage" style="height:400px"/>
</p>

### Problem modelisation

<p align="center">
    <img src="https://user-images.githubusercontent.com/59691442/169556846-231900f0-2195-478d-be14-0990f52ea1b4.png" alt="tspExampleImage" style="height:400px"/>
</p>

<!-- ### Modélisation de notre problème

__objectif__ : min(distance)

__variables__ de decisions :

__contraintes__ :
- aller dans toutes les villes
- commencer / terminer par sydney
- passer qu'une seule fois dans chaque ville (excepté la ville de départ, 2 fois) -->

<!-- ## Problem modelisation

__objectif__ : min(distance)

__variables__ :

__contraintes__ :
- aller dans toutes les villes
- commencer / terminer par sydney
- passer qu'une seule fois dans chaque ville (excepté la ville de départ, 2 fois) -->

## Program implementation

## How it works

Placeholder

### Excel data

Our project contains a excel file that is load by our app.
The excel contains the distances of all cities relativeness from each other.

|  |M.C.G.|Docklands|Adelaide Oval|
|--|--|--|--|
|M.C.G.|  0| 3 |657 |
|Docklands| 3|0 |654 |
|Adelaide Oval| 657|654|0|

The excel is loaded in our app and it will search the city you want to start from and move it to the first row.

For example, if you want to begin your tavel from Adelaide Oval, the data will look lie below :

|  |M.C.G.|Docklands|Adelaide Oval|
|--|--|--|--|
|Adelaide Oval| 657|654|0|
|M.C.G.|  0| 3 |657 |
|Docklands| 3|0 |654 |

## Documentations

TSP Linear Programming solver :  
<https://hal.archives-ouvertes.fr/hal-02947086/document>

Google Or-Tools :  
<https://developers.google.com/optimization/>
