# Lab 6: Search Engine

This mini-Google clone is search engine implementation, complete with SciPy backend and Flask frontend. 
It was used with Simple English Wikipedia dump, but it can use any text with reasonable amount of unique words.

## How backend works
Text is represented with bag-of-words implementation - dictionary mapping words to their occurrences. 
Preprocessing for texts includes deleting stop words (e. g. "the", "a", "he"), changing them to lowercase etc. 
Bags of words for separate texts are then used to create term-by-document sparse matrix. 
It's then changed to TF-IDF (Term Frequency - Inverse Document Frequency) matrix, reducing importance of most common words (they usually carry little information about document-specific subject). 
Column vectors (representing documents) are then normalized. It allows us to use cosine similarity measure as simple dot product of query bag-of-words vector and document vector. 
Similarities are then sorted in descending order and displayed, meaning more similar documents are first in search results. 
Matrix and query are huge, so they are optimized with SVD matrix compression, so instead of huge sparse matrix app is operating on small dense matrices. 
As an added bonus, SVD reduces data noise, yielding better search results.

## How frontend works
It's my first web app ever, so it's just a simple Flask "Hello world" template changed to use input field and display results. 
For debugging and educational purposes (and since we had to for the class), app also prints final sorted results to the console.
