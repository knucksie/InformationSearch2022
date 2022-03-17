DISJUNCTION_SIGN = "|"
CONJUCTION_SIGN = "&"
NEGATION_SIGN = "!"


def parse_index(filepath, encoding):
    inverted_index = {}
    with open(filepath, encoding=encoding) as index_file:
        for line in index_file:
            term, *documents = line.rstrip('\n').split(' ')
            documents = set(documents)
            inverted_index[term] = documents
    return inverted_index


def boolean_search(search_request: str, inverted_index):
    prev_result = set()
    tokens = search_request.split(' ')
    start_token = tokens[0]
    try:
        search_result = inverted_index[start_token]
        if len(tokens) == 1:
            return search_result
        for i in range(1, len(tokens) - 1):
            if tokens[i] == DISJUNCTION_SIGN:
                search_result = search_result | inverted_index[tokens[i + 1]]
            elif tokens[i] == CONJUCTION_SIGN:
                search_result = search_result & inverted_index[tokens[i + 1]]
            elif tokens[i] == NEGATION_SIGN:
                search_result = search_result - inverted_index[tokens[i + 1]]
        return search_result
    except KeyError as error:
        raise ValueError('Nothind found in index')


if __name__ == '__main__':
    index = parse_index('inverted_index.txt', 'UTF-8')
    search_string = input('Enter your search request:')
    if not search_string:
        print('Error: empty search request.')
        exit(1)
    else:
        try:
            result = boolean_search(search_string, index)
            if result:
                print(f'Following documents were found: {", ".join(result)}')
            else:
                print('Nothing was found.')
        except ValueError:
            print('Nothing was found or search request is incorrect.')
