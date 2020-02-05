# Laboratory 4 - simulated annealing

DISCLAIMER: simulated annealing implemented and used in all 3 tasks has bugs, which limit it's effectiveness. It's implemented 
with tunable hyperparameters, reheating etc., but still doesn't work properly sometimes and after many hours I have given up hope. 
It still works as proof-of-concept and for educational purposes, though.

simulated annealing, TSP approximation, binary image generator, sudoku solver  

## Task 1 - TSP approximation
Using simulated annealing heuristic the approximate solution for Travelling Salesman Problem (TSP) is calculated for randomly 
generated points.

## Task 2 - binary image generator
Using custom "energy" functions, random binary images are changed using simulated annealing. Energy functions are minimized by 
the heuristic, but they can be arbitrary, resulting in "playing God" program, where artistic creations can be generated from data 
using simple rules defined by energy matrix.

## Task 3 - sudoku solver
This is a fine example of a problem where simulated annealing does not work very well. It can be optimized to solve even hard 
sudokus, but as a heuristic method of finding "good enough, but usually not the best" solution, simulated annealing struggles to 
solve sudoku. The reason is, it has only one solution, there is no "good enough". This is a common obstacle for many optimization 
algorithms, which are commonly not required to provide perfectly optimal solution. With enough random starts and upgrades it can still 
solve some examples, which I think of as a success.