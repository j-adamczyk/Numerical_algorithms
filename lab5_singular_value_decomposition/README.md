# Laboratory 5 - Singular Value Decomposition (SVD)

## Task 1 - geometric interpretation
SVD can be thought of as a method of understanding shape of linear space created by given system of 
equations. Program illustrates it with shaping sphere, changing it into an ellipsoid and using SVD 
to create vectors representing space shape changes.

## Task 2 - low-rank approximation
SVD and its singular values can be used to reduce size (rank) of the matrix. This method is known 
as a low-rank approximation, since it approximates the original matrix using the largest singular values, 
which can be thought of as the "most important" parts of the original matrix. Using only a part of them, 
the original matrix is compressed. This simple method can be used with Pillow for image compression, 
greatly reducing the size of original image without overly lowering the quality.