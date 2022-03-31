import zipfile
import re
import string
import nltk
import math
from bs4 import BeautifulSoup
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from pymorphy2 import MorphAnalyzer

CORPUS_INDEX_FILEPATH = "../first_task/index.txt"


# generating corpus with lemmas instead of terms


# tf computing function
def compute_tf(corpus, bag):
    tf_dict = {}
    for word in bag:
        for doc in corpus.keys():
            tokens = corpus[doc]
            word_num = len(tokens)
            if doc not in tf_dict.keys():
                tf_dict[doc] = {}
            tf = tokens.count(word) / word_num
            tf_dict[doc][word] = tf
    return tf_dict


# idf computing function
def compute_idf(corpus, bag):
    idf_dict = {}
    number_of_documents = len(corpus)
    for word in bag:
        idf = math.log(number_of_documents / sum(1 if word in document else 0 for document in corpus.values()))
        idf_dict[word] = idf
    return idf_dict


# tf-idf computing function
def compute_tf_idf(tf_dict, idf_dict):
    tf_idf_dict = {}
    for doc in tf_dict.keys():
        tf_idf_dict[doc] = {}
        for word in tf_dict[doc]:
            tf_idf_dict[doc][word] = tf_dict[doc][word] * idf_dict[word]
    return tf_idf_dict


def parse_corpus(doc_index_filepath):
    # downloading all necessary assests nltk
    nltk.download("stopwords")
    nltk.download('punkt')

    # all tokens list
    tokens = set()

    # preparing stopwords set
    custom_stopwords = {'Copyright', '©', 'проза.ру', '...', 'стихи.ру', '→', '№', '–'}
    stopwords_extended = set(stopwords.words('russian')) | custom_stopwords

    # preparing custom punctuation set
    custom_punctuation = {'…'}
    punctuation_extended = set(string.punctuation) | custom_punctuation

    corpus = {}

    morph = MorphAnalyzer()
    index = {}
    # parsing pages from zip archive
    with open(doc_index_filepath) as pages:
        for line in pages:
            doc_num = line.strip('\n').split(':')[0]
            with zipfile.ZipFile('../first_task/pages.zip', 'r') as archive:
                page = archive.read(f'{doc_num}.html').decode()

                # removing all html tags and digits
                soup = BeautifulSoup(page, features='html.parser')
                raw_text = re.sub(r'\d+', '', soup.text)

                # removing punctuation from text
                no_punctuation_text = "".join([char.lower() for char in raw_text if char not in punctuation_extended])

                # tokenizing text
                text = word_tokenize(no_punctuation_text)

                # removing stopwords
                doc_tokens = [word.lower() for word in text if word.lower() not in stopwords_extended]

                corpus[doc_num] = doc_tokens

    morph = MorphAnalyzer()
    lemmatized_corpus = {}
    for doc in corpus.keys():
        tokens = corpus[doc]
        lemmatized_corpus[doc] = [morph.normal_forms(token)[0] for token in tokens]

    # generate term bag
    term_bag = set()
    for tokens in corpus.values():
        term_bag |= set(tokens)

    # generate lemma bag
    lemma_bag = {morph.normal_forms(term)[0] for term in term_bag}
    # compute tf for lemmas
    lemma_tf = compute_tf(lemmatized_corpus, lemma_bag)

    # compute ids for lemmas
    lemma_idf = compute_idf(lemmatized_corpus, lemma_bag)

    # compute tf-idf for lemmas
    lemma_tf_idf = compute_tf_idf(lemma_tf, lemma_idf)

    return lemma_tf_idf


def lemmatize_search(search):
    result = []
    morph = MorphAnalyzer()
    words = search.split()
    for word in words:
        result.append(morph.normal_forms(word)[0])
    return result


def get_document_links(links_filepath):
    i = 1
    links = {}
    with open(links_filepath) as file:
        for line in file:
            links[i] = line.rstrip('\n')
            i += 1
    return links


def compute_similarity(tf_idf, words):
    similarity_coefs = {}
    for doc in tf_idf.keys():
        similarity = 0
        for word in words:
            if word in tf_idf[doc].keys():
                similarity += tf_idf[doc][word]
        if similarity > 0:
            similarity_coefs[doc] = similarity
    return similarity_coefs

if __name__ == '__main__':
    tf_idf = parse_corpus(CORPUS_INDEX_FILEPATH)
    print('TF-IDF computed!')
    search = input('Enter search phrase')
    while search != 'exit':
        words = lemmatize_search(search)
        search_result = compute_similarity(tf_idf, words)
        if len(search_result) == 0:
            print('Oops, nothing was found.')
        else:
            docs = dict(sorted(search_result.items(), key=lambda item: item[1], reverse=True))
            for doc in docs:
                print(f'Document id: {doc}. Similarity: {docs[doc]}')
        search = input('Enter search phrase')
