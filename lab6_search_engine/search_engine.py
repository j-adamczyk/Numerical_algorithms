import file_manager
import numpy as np
from operator import itemgetter
import scipy.sparse as sparse
from sklearn.decomposition import TruncatedSVD
from sklearn.preprocessing import normalize


# creating and filling term-by-document sparse matrix
def create_term_by_document_matrix(terms, documents):
    matrix = sparse.lil_matrix((len(terms), len(documents)))

    # map index->term, makes writing to matrix easier
    terms_index_map = dict()
    index = 0
    for term in terms:
        terms_index_map[term] = index
        index += 1

    # documents already have their indices in map
    for index, document in documents.items():
        for word, count in document.word_count.items():
            matrix[terms_index_map[word], index] = count

    return matrix.tocsr(), terms_index_map


# multiplies every TF document vector by IDF vector and normalizes result
def documents_IDF_and_normalize(documents, bag_of_all_words):
    number_of_documents = len(documents)
    for index, document in documents.items():
        for word, count in document.word_count.items():
            IDF = np.log(number_of_documents / bag_of_all_words[word])
            document.word_count[word] *= IDF
        count_vector = np.array([list(document.word_count.values())])
        count_vector = normalize(count_vector)[0]
        i = 0
        for word, count in document.word_count.items():
            document.word_count[word] = count_vector[i]
            i += 1
    return documents


# performs low-rank approximation with SVD
# svd - SVD transformer class from scikit-learn
# it's basically LSI, since it's used for term-by-document matrix
def lower_matrix_rank(matrix, k):
    svd = TruncatedSVD(n_components=k).fit(matrix.T)
    low_rank_matrix = svd.transform(matrix.T)
    return low_rank_matrix, svd


# gets most similar documents
def get_similar_documents(matrix, query_vector, svd):
    query_vector_svd = svd.components_.dot(query_vector.todense())
    similarities = matrix.dot(query_vector_svd)
    return similarities


# performs actual query search
def query_search(query_text):
    import text_processing
    query = text_processing.process_query(query_text)
    terms_index_map = file_manager.load_dictionary("terms_index_map")

    query_vector = sparse.lil_matrix((len(terms_index_map), 1))
    for term, tf_idf in query.items():
        query_vector[terms_index_map[term], 0] = tf_idf

    similarities = get_similar_documents(low_rank_matrix, query_vector, svd)

    indexed_similarities = []
    number_of_documents = similarities.shape[0]
    for document_index in range(number_of_documents):
        similarity = similarities[document_index, 0]
        indexed_similarities.append((document_index, similarity))

    indexed_similarities.sort(key=itemgetter(1), reverse=True)
    result = []
    i = 0
    for similarity in indexed_similarities:
        # stop if either:
        # - there's no similarity at all
        # - chosen number of results has been achieved
        if similarity[1] <= 0 or i == result_number:
            break
        index = similarity[0]
        document_title = documents[index].title.replace(".txt", "")
        result.append((document_title, round(similarity[1], 3)))
        i += 1

    i = 0
    for similarity in indexed_similarities:
        if i == k:
            break

        print(documents[similarity[0]].title.replace(".txt", "") + " - " + str(round(similarity[1], 3)))
        i += 1

    return result


k = 200
result_number = 100

# uncomment only if you want to change k (search precision)
"""matrix = file_manager.load_term_by_document_matrix()
low_rank_matrix, svd = lower_matrix_rank(matrix, k)
file_manager.save_svd_matrix(low_rank_matrix, svd)"""

low_rank_matrix, svd = file_manager.load_svd_matrix()
documents = file_manager.load_dictionary("documents")
