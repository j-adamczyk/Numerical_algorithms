from collections import Counter
import numpy as np
import os
import pickle
import scipy.sparse as sparse


class Document:
    def __init__(self, title, word_count):
        self.title = title
        self.word_count = word_count


# used to cut simple English dump from text block to individual files
def format_simple_english_file(filename):
    with open(filename, "r", encoding="utf8") as file:
        curr_path = os.getcwd()
        article = ""
        title = ""
        save = True
        new_article = True
        for line in file:
            if new_article:
                title = line
                title = title[:-1]
                # omits any articles with characters forbidden in Windows file names
                if any(x in title for x in ["/", "\\", ":", "*", "?", "\"", "<", ">", "|"]):
                    save = False
                new_article = False
            else:
                if line != "\n" and save:
                    article += line
                elif line == "\n":
                    if save:
                        filepath = os.path.join(curr_path, "data", title + ".txt")
                        article_text = title + "\n" + article

                        with open(filepath, "w", encoding="utf-8") as article_file:
                            article_file.write(article_text)
                    else:
                        save = True
                    new_article = True
                    article = ""


# saves article processed by text_processing module
def save_processed_article(filename, bag_of_words):
    text = ""
    for word, count in bag_of_words.items():
        text = text + word + " " + str(count) + "\n"
    filepath = os.path.join(os.getcwd(), filename)
    with open(filepath, "w", encoding="utf-8") as article_file:
        article_file.write(text)


# loads previously processed data (with additional information for searching)
def load_processed_data():
    directory_path = os.path.join(os.getcwd(), "processed_data")
    index = 0  # indices should later correspond to matrix columns
    documents = dict()
    bag_of_all_words = Counter()
    for file in os.listdir(directory_path):
        filepath = os.path.join(directory_path, file)
        word_count = dict()
        bag_of_words = Counter()
        with open(filepath, "r", encoding="utf8") as text:
            for line in text:
                elems = line.split()  # elems[0] - word, elems[1] - word count
                word_count[elems[0]] = int(elems[1])
                bag_of_words[elems[0]] = 1
        bag_of_all_words += bag_of_words
        documents[index] = Document(file, word_count)
        index += 1
    return set(dict(bag_of_all_words).keys()), documents, bag_of_all_words


# saves term-by-document matrix
def save_term_by_document_matrix(matrix):
    filepath = os.path.join(os.getcwd(), "results", "term_by_document_matrix.npz")
    sparse.save_npz(filepath, matrix)


# loads term-by-document matrix
def load_term_by_document_matrix():
    filepath = os.path.join(os.getcwd(), "results", "term_by_document_matrix.npz")
    matrix = sparse.load_npz(filepath)
    return matrix


# saves term-by-document matrix after SVD and SVD object (they're paired)
def save_svd_matrix(matrix, svd):
    filepath = os.path.join(os.getcwd(), "results", "svd_matrix.npy")
    np.save(filepath, matrix)

    filepath = os.path.join(os.getcwd(), "results", "svd.pickle")
    with open(filepath, "wb") as file:
        pickle.dump(svd, file)


# loads term-by-document matrix after SVD and SVD object (the're paired)
def load_svd_matrix():
    filepath = os.path.join(os.getcwd(), "results", "svd_matrix.npy")
    matrix = np.load(filepath)

    filepath = os.path.join(os.getcwd(), "results", "svd.pickle")
    with open(filepath, "rb") as file:
        svd = pickle.load(file)

    return matrix, svd


# saves dictionary (probably terms or documents)
def save_dictionary(dictionary, type):
    filepath = os.path.join(os.getcwd(), "results", type + ".pickle")
    with open(filepath, "wb") as file:
        pickle.dump(dictionary, file)


# loads dictionary (probably terms or documents)
def load_dictionary(type):
    filepath = os.path.join(os.getcwd(), "results", type + ".pickle")
    print(filepath)
    with open(filepath, "rb") as file:
        dictionary = pickle.load(file)
    return dictionary


# loads article text
def load_article_text(filename):
    filepath = os.path.join(os.getcwd(), "data", filename + ".txt")
    article = ""
    with open(filepath, "r", encoding="utf-8") as file:
        # omit title line
        next(file)
        for line in file:
            article += line
    return article
