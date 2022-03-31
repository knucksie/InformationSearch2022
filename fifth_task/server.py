from flask import Flask
from flask import render_template, request
from search_engine import parse_corpus, lemmatize_search, compute_similarity, get_document_links
CORPUS_INDEX_FILEPATH = "../first_task/index.txt"
LINKS_FILEPATH = "../first_task/pages.txt"
app = Flask(__name__)

TF_IDF = None
LINKS = None
@app.route('/')
def index():
    return render_template('form.html')


@app.route('/search', methods=['post'])
def search():
    if request.method == 'POST':
        search_request = username = request.form.get('search_request')
        words = lemmatize_search(search_request)
        search_result = compute_similarity(TF_IDF, words)
        if len(search_result) == 0:
            return 'Oops, nothing was found.'
        else:
            docs = dict(sorted(search_result.items(), key=lambda item: item[1], reverse=True))
            return render_template('search_result.html', search_result=search_result, links=LINKS)


if __name__ == '__main__':
    links = get_document_links(LINKS_FILEPATH)
    LINKS = links
    tf_idf = parse_corpus(CORPUS_INDEX_FILEPATH)
    TF_IDF = tf_idf
    app.run()
