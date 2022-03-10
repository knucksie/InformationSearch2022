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

            # adding tokens to common token set
            tokens |= doc_tokens

# writing token to document
with open('tokens.txt', 'w', encoding='utf-8') as output_file:
    output_file.write('\n'.join(tokens))

# initiating pymorphy morph analyzer
morph = MorphAnalyzer()

# grouping tokens by lemmas
lemmas = {}
for token in tokens:
    lemma = morph.normal_forms(token)[0]
    if lemma in lemmas.keys():
        lemmas[lemma].append(token)
    else:
        lemmas[lemma] = [token]

# writing tokens grouped by lemmas to file
with open('lemmas.txt', 'w', encoding='utf-8') as output_file:
    for lemma in lemmas.keys():
        output_file.write(f'{lemma}: {" ".join(lemmas[lemma])}\n')
