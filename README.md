# travelling_salesman_problem_lp

Travelling salesman problem solver using linear programming with Google Or-Tools.

## Modélisation de notre problème

__objectif__ : min(distance)

__variables__ de decisions :

__contraintes__ :
    - aller dans toutes les villes
    - commencer / terminer par sydney
    - passer qu'une seule fois dans chaque ville (excepté la ville de départ, 2 fois)

## Problem modelisation

__objectif__ : min(distance)

__variables__ de decisions :

__contraintes__ :
    - aller dans toutes les villes
    - commencer / terminer par sydney
    - passer qu'une seule fois dans chaque ville (excepté la ville de départ, 2 fois)

## Excel data

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
