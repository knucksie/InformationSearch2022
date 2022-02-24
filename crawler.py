import requests
from user_agent import generate_user_agent

# use fake user agent to avoid anti robot blocks
fake_user_agent = generate_user_agent(os=('mac', 'linux'))
headers = {
    'User-Agent': fake_user_agent
}
# define input file name
pages_list = 'pages.txt'

# document number counter
doc_num = 0
with open(pages_list) as pages:
    for url in pages:
        doc_num += 1
        url = url.strip('\n')
        page = requests.get(url, headers=headers)
        # skip page if it does not exist
        if page.status_code == 200:
            filename = f'{doc_num}.html'
            # save page to file
            with open(filename, 'w', encoding="utf-8") as output_file:
                output_file.write(page.text)
            # add page (doc) num to index file
            with open('index.txt', 'a') as index:
                index.write(f'{doc_num}:{url}\n')
        # output progress to console
        print(f'{url} - done')

