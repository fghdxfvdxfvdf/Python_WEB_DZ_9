import json
import requests
from bs4 import BeautifulSoup
# from sqlalchemy.engine import create_engine
# from sqlalchemy.orm import sessionmaker

# from model import Quotes, Authors
from url_next_page import next_page_list


# URI = 'http://quotes.toscrape.com'
# path_quotes = 'quotes.json'
res_list = []


def parse_quotes(url):
    html_doc = requests.get(url)

    if html_doc.status_code == 200:

        soup = BeautifulSoup(html_doc.content, 'html.parser')
        datas = soup.select('div')[0].find_all('div', attrs={'class': 'quote'})
        quote_list = []
        author_list = []
        tag_list = []
        # res_list = []

        for data in datas:            
            
            quotes = data.find_all('span', class_='text')
            for quote in quotes:
                # quote_list.append(quote.text)

                authors = data.find_all('small', attrs={'class': 'author'})
                for author in authors:
                    # author_list.append(author.text)

                    tags = data.find_all('a', attrs={'class': 'tag'})

                    for tag in tags:
                        if tag.text in tag_list:
                            continue
                        tag_list.append(tag.text)
                    
                    result = {'quote': quote.text,
                            'author': author.text,
                            'tags': tag_list}
                    
                    tag_list = []
                    res_list.append(result)
                    
        return res_list[0]
        
    else:
        return {}    
    


def load_quotes(url_main, path):
    
    with open(path, 'w', encoding='utf-8') as f:
        for url in next_page_list(url_main):
            res_list.append(parse_quotes(url))
        json.dump(res_list, f, ensure_ascii=False, indent=3)


if __name__=='__main__':

    URL_main = 'http://quotes.toscrape.com'

    res_list = []
    
    with open('unique_about_authors', 'w', encoding='utf-8') as f:
        for url in next_page_list(URL_main):
            res_list.append(parse_quotes(url))
        json.dump(res_list, f, ensure_ascii=False, indent=3)
