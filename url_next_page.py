import json
import requests
from bs4 import BeautifulSoup

def next_page_list(url):
    # URL = 'http://quotes.toscrape.com'
    html_doc = requests.get(url)
    page_url_list = [url]
    html_doc = requests.get(url)
    while True:

        try:
            if html_doc.status_code == 200:
                soup = BeautifulSoup(html_doc.content, 'html.parser')
                next_page_data = soup.select('nav')[0].find_all('li', attrs={'class': 'next'})
                if next_page_data: # if next_page_data != []:
                    next_page = list(i.find('a')['href'] for i in next_page_data)[0]
                    html_doc = requests.get(url + next_page)
                    page_url_list.append(url + next_page)
                else:
                    break
            
        except Exception as err:
            print(err)
            break
    return page_url_list

if __name__=='__main__':
    URL = 'http://quotes.toscrape.com'

    # print(next_page_list(URL))

    with open('unique_about_authors', 'w') as f:
        json.dump(next_page_list(URL), f, ensure_ascii=False, indent=3)


