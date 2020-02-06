# Laboratory 1 - computer arithmetic, numerical stability, deterministic chaos

## Task 1 - pairwise summation
Comparison of naive linear array summation and pairwise (recursive) summation algorithm.
Obviously pairwise summation is vastly superior in terms of numerical stability.

## Task 2 - Kahan summation algorithm
Main advantage of this simple method is using numerical error from previous operation 
in the next one, effectively making arithmetic error O(1), at the cost of being slower 
than pairwise summation.

## Task 3 - series partial sums
Riemann's dzeta function and Dirichlet's eta function are implemented and compared 
in terms of forward and backward series partial summation. It proves that computer arithmetic 
is not associative.

## Task 4 - logistic map
Simple logistic equation given by $x_{n+1}=rx_n(1-x_n)$ is the very basic example of 
deterministic chaos, a. k. a. butterfly effect. It's clearly visible on bifurcation 
diagrams that for smallest changes of values in calculations this expression varies wildly, 
but deterministically.
