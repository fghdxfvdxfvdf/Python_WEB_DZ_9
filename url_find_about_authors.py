import json
import requests
from bs4 import BeautifulSoup
from url_next_page import next_page_list


def about_authors_def(url: str) -> list:
    all_url = next_page_list(url)

    unique_about_authors = []
    for url in all_url: 

        html_doc = requests.get(url)
        if html_doc.status_code == 200:
            soup = BeautifulSoup(html_doc.content, 'html.parser')
            datas = soup.select('div')[0].find_all('div', attrs={'class': 'quote'})

            for data in datas:       
                about_authors = data.find('a')['href']

                if about_authors in unique_about_authors:
                    continue
                unique_about_authors.append(about_authors)

    return unique_about_authors


if __name__=='__main__':
    URL = 'http://quotes.toscrape.com'

    # print(about_authors_def(URL))

    with open('unique_about_authors', 'w') as f:
        for about_author in about_authors_def(URL):
            f.write(f'{URL}{about_author}\n')
