import json
import requests
from bs4 import BeautifulSoup

from url_find_about_authors import about_authors_def


def parse_authors(url):
    
    html_doc = requests.get(url)
    if html_doc.status_code == 200:
        soup = BeautifulSoup(html_doc.content, 'html.parser')

        authors = soup.find('h3', attrs={'class': 'author-title'})

        borns = soup.find('span', class_='author-born-date')

        borns_location = soup.find('span', class_='author-born-location')

        descriptions = soup.find('div', class_='author-description')
                
        result = {'author': authors.text,
                'borns': borns.text,
                'borns_location': borns_location.text,
                'descriptions': descriptions.text.strip()}

        return result
    
    else:
        return {}   

def load_authors(url_main, path):

    result_list = []
    with open(path, 'w', encoding='utf-8') as f:
        for about_author in about_authors_def(url_main):
            url = f'{url_main}{about_author}'
            result_list.append(parse_authors(url))    
        json.dump(result_list, f, indent=3, ensure_ascii=False)


URI = 'http://quotes.toscrape.com'
path_authors = 'authors.json'
load_authors(URI, path_authors)

if __name__=='__main__':
    
    URL_main = 'https://quotes.toscrape.com'

    result_list = []
    
    with open('parse_quotes', 'w', encoding='utf-8') as f:
    
        for about_author in about_authors_def(URL_main):
            
            url = f'{URL_main}{about_author}'
            
            result_list.append(parse_authors(url))
    
        json.dump(result_list, f, indent=3, ensure_ascii=False)
