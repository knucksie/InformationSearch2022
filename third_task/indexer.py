import zipfile
import re
import string
import nltk
from bs4 import BeautifulSoup
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from pymorphy2 import MorphAnalyzer

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

morph = MorphAnalyzer()
index = {}
# parsing pages from zip archive
with open('../first_task/index.txt') as pages:
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
            doc_tokens = {word.lower() for word in text if word.lower() not in stopwords_extended}

            for token in doc_tokens:
                term = morph.normal_forms(token)[0]
                if term in index.keys():
                    index[term].add(doc_num)
                else:
                    index[term] = {doc_num}

# writing index to document
with open('inverted_index.txt', 'w', encoding='utf-8') as output_file:
    for term in index.keys():
        output_file.write(f'{term} {" ".join(index[term])}\n')
