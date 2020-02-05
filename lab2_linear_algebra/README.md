# Laboratory 2 - matrix factorization, linear equations systems solvers, electrical circuit analyzer

## Task 1 - Gauss-Jordan elimination
Linear equation solver using simple method known from algebra classes. It's effective on paper, but 
very ineffective on paper, even more than simple Gauss elimination, having almost 2 times larger 
constant in terms of computational complexity (and also less effective numerically). It's improved 
a bit improved by partial or full pivoting, but it doesn't change much compared to better algorithms.

## Task 2 - LU factorication
Linear equation solver using LU factorization, without and with partial pivoting and matrix scaling. 
It's standard, simple and effective method of solving systems of linear equations.

## Task 3 - electical circuit analyzer
This simple program loads graph representing electical circuit from file. It should be a weighted 
directed graph with format "from to resistance", graph generators are also included (they were written 
fast and NetworkX is quite cranky in this regard, so expect some weird behaviours). 
After loading graph is represented as directed NetworkX graph with one edge having battery in it with 
electromotorical power E. Using Kirchhoff's laws it calculates current in every edge and plots it with Matplotlib. 
Calculations are performed using systems of sparse linear equations derived from Kirchhoff's laws, with care to take 
linearly separable square system of equations. It should be noted that this program uses regular Numpy methods for 
educational simplicity and should be changed to sparse matrix representations and operations for effectiveness in 
real-life applications.