from bs4 import BeautifulSoup
import requests
import os
from tqdm import tqdm

if(not os.path.exists("urls") and not os.path.isdir("urls")):
    os.mkdir("urls")

SITE = "https://mg.wikipedia.org"
BASE = "https://mg.wikipedia.org/wiki/Manokana:Pejy_rehetra"

adress_list = []


def write_to_text(adress_list, filename):
    with open(os.path.join("urls", filename), 'a') as f:
        f.write(''.join(adress_list))


def get_links(soup: BeautifulSoup):
    adress_list = []
    all_pages_chunk = soup.find(class_="mw-allpages-chunk").extract()
    lis = all_pages_chunk.find_all("li")
    for li in lis:
        e = li.extract()
        link = e.find_next().attrs["href"]
        adress_list.append(SITE + link + "\n")
    write_to_text(adress_list, "wiki_urls.txt")


initial_page = "/wiki/Manokana:Pejy_rehetra"
next_page = "/wiki/Manokana:Pejy_rehetra"


def generator():
    while True:
        yield


for _ in tqdm(generator()):
    url = SITE + next_page
    page = requests.get(SITE + next_page)
    soup = BeautifulSoup(page.content, 'html.parser')
    get_links(soup)
    pagenav = soup.find_all("div", class_="mw-allpages-nav")
    try:
        p = pagenav[len(pagenav)-1]
        e = p.extract()
        x = e.find_all_next("a")
        a = x[0].find_parent().find_next().find_next()
        if(next_page == initial_page and a is None):
            next_page = x[0].find_parent().find_next().attrs["href"]
        elif(next_page != initial_page and a is None):
            print("we are on the last page")
            print(page.url)
            raise("we are on the last page")
        elif(next_page != initial_page and a is not None):
            next_page = a.attrs["href"]
    except Exception as e:
        print(e)
        break
