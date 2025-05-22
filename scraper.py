from tqdm import tqdm
from bs4 import BeautifulSoup
import requests
import os
import json


def scrape(url):
    
    #### send request to website and store response as a variable
    response = requests.get(url)
    
    #### check if request was successful
    if response.status_code != 200: 
        print(response.status_code)
        quit()
        
        #### parse html content
    soup = BeautifulSoup(response.text, 'html.parser')
#    print(soup)
#    quit()

    #### get book page links
    books = soup.find_all('article', class_='product_pod')
    links = []
    for book in books:
        tags = book.find_all('a', href=True)
        for t in tags:
#            print(t)
            link = url + '/' + t['href']
#            print(link)
            links.append(link)
    links = list(set(links))

    #### visit each book page and get product description
    product_info = {}
    for l in tqdm(links):
        response = requests.get(l)
        if response.status_code != 200:
            print(response.status_code)
            quit()

        d = {}
        
        #### parse content
        soup = BeautifulSoup(response.text, 'html.parser')
        
        #### get book title
        d['title'] = soup.find('title').string
        
        #### get product description
        #### get all <p> tags
        tags = soup.find_all('p')
        for t in tags:
            if not t.attrs:
                d['description'] = t.string
        
        #### get price and universal product code
        table = soup.find('table', class_="table table-striped")
        tags = table.find_all('tr')
        for t in tags:
            #### get price
            if t.find('th').string == 'Price (excl. tax)':
                d['price'] = t.find('td').string
            #### use universal product code as unique key for 
            #### each book
            if t.find('th').string == 'UPC':
                product_info[t.find('td').string] = d

    return product_info
        

def main():
    
    #### scrape
    url = 'https://books.toscrape.com'
    product_info = scrape(url)
    
    #### save scraped data
    data_dir = f'{os.getcwd()}/data'
    if not os.path.exists(data_dir): os.makedirs(data_dir)
    with open(f'{data_dir}/scraped_data.json', 'w') as f:
        json.dump(product_info, f)
    

if __name__ == '__main__':
    main()
