import os
import requests
from bs4 import BeautifulSoup
from tqdm import tqdm

# creating urls folder if not exist
if(not os.path.exists("urls") and not os.path.isdir("urls")):
    os.mkdir("urls")

not_adress = ['https://aoraha.mg/',
'https://www.lexpressmada.com/',
'https://lhebdo.mg/',
'javascript:void(0)']

def is_valid_adress(adress):
    for i in range(len(not_adress)):
        if adress == not_adress[i] or "cat" in adress or "pilo-kely" in adress:
            return False
    return True

def write_to_text(url_list, filename):
    with open(os.path.join("urls", filename),'a') as fichier:
        fichier.write('\n'.join(url_list))

BASE = "https://aoraha.mg/page/"

for i in tqdm(range(1, 390, 1)):
    adress_list = []
    url = BASE + str(i)
    page = requests.get(url)
    soup = BeautifulSoup(page.content, 'html.parser')
    # parentelem = driver.find_elements_by_class_name("entry-title")
    parentelem = soup.find_all(class_="entry-title")
    # print(parentelem)
    for elem in parentelem:
        # linkelem = elem.find_element_by_tag_name('a')
        linkelem = elem.find_next('a')
        # link = linkelem.get_attribute('href')
        link = linkelem.attrs["href"]
        if is_valid_adress(link): adress_list.append(link)
    write_to_text(adress_list, "aoraha_urls.txt")
    # print("navigating to", url)
# driver.close()