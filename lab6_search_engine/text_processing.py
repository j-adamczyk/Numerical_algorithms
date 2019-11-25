from collections import Counter
import file_manager
import nltk
from nltk.corpus import stopwords
from nltk.stem.porter import PorterStemmer
from nltk.tokenize import sent_tokenize, word_tokenize
import numpy as np
import os
from sklearn import preprocessing
import string


# gets stemmed words and bag-of-words (count of occurrences of each word stem)
def process_article(text):
    # start by lowercasting whole article
    text = text.lower()

    # divide into words (according to punctuation)
    words = [word for sentence in sent_tokenize(text) for word in word_tokenize(sentence)]

    # remove English stop words while punctuation is still there
    english_stop_words = set(stopwords.words('english'))
    words = [word for word in words if word not in english_stop_words]

    # remove punctuation
    punctuation = set(string.punctuation)
    punctuation.add("...")
    words = [word for word in words if word not in punctuation]

    # stem words and leave only long enough stems
    stemmer = PorterStemmer()
    words = [stemmer.stem(word) for word in words]
    words = [word for word in words if len(word) > 2]

    # count occurrences of each word
    bag_of_words = dict(Counter(words))

    return bag_of_words


# processes all Simple English dump data
def process_all_articles():
    curr_path = os.getcwd()
    directory_path = os.path.join(curr_path, "data")
    for file in os.listdir(directory_path):
        filepath = os.path.join(directory_path, file)
        with open(filepath, "r", encoding="utf8") as text:
            bag_of_words = process_article(text.read())
            result_path = os.path.join(curr_path, "processed_data", file)
            file_manager.save_processed_article(result_path, bag_of_words)


# processes Simple English data dump
# result: saved TF-IDF term-by-document matrix with normalized columns
def full_dump_data_processing():
    import search_engine
    # check if necessary resources are installed
    try:
        nltk.data.find("tokenizers/punkt")
    except LookupError:
        nltk.download('punkt')
    try:
        nltk.data.find("corpora/stopwords")
    except LookupError:
        nltk.download('stopwords')

    process_all_articles()
    terms, documents, bag_of_all_words = file_manager.load_processed_data()
    documents = search_engine.documents_IDF_and_normalize(documents, bag_of_all_words)
    matrix, terms_index_map = search_engine.create_term_by_document_matrix(terms, documents)
    file_manager.save_term_by_document_matrix(matrix)
    file_manager.save_dictionary(documents, "documents")
    file_manager.save_dictionary(terms_index_map, "terms_index_map")
    file_manager.save_dictionary(bag_of_all_words, "bag_of_all_words")


# performs processing operations on query vector
def process_query(query_text):
    try:
        nltk.data.find("tokenizers/punkt")
    except LookupError:
        nltk.download('punkt')
    try:
        nltk.data.find("corpora/stopwords")
    except LookupError:
        nltk.download('stopwords')

    bag_of_words = process_article(query_text)

    bag_of_all_words = file_manager.load_dictionary("bag_of_all_words")
    matrix = file_manager.load_term_by_document_matrix()
    number_of_documents = matrix.shape[1]
    for word, count in bag_of_words.items():
        IDF = np.log(number_of_documents / bag_of_all_words[word])
        bag_of_words[word] *= IDF

    count_vector = np.array([list(bag_of_words.values())])
    count_vector = preprocessing.normalize(count_vector)[0]
    i = 0
    for word, count in bag_of_words.items():
        bag_of_words[word] = count_vector[i]
        i += 1

    return bag_of_words
