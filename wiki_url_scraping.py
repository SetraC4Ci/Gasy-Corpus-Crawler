"""scrape all malagasy langage wiki articles url and store those url in file"""

from selenium import webdriver
import time
import os

if(not os.path.exists("urls") and not os.path.isdir("urls")):
    os.mkdir("urls")

driver = webdriver.Chrome()
driver.implicitly_wait(10)

BASE = "https://mg.wikipedia.org/wiki/Manokana:Pejy_rehetra"

driver.get(BASE)

adress_list = []

def write_to_text(adress_list, filename):
    with open(os.path.join("urls", filename),'a') as f:
        f.write(''.join(adress_list))

def get_links():
    adress_list = []
    parent_elem = driver.find_elements_by_class_name("allpagesredirect")
    for elem in parent_elem:
        linkelem = elem.find_element_by_tag_name('a')
        link = linkelem.get_attribute('href')
        adress_list.append(link + "\n")
    parent_elem = driver.find_elements_by_class_name("mw-allpages-chunk")
    for elem in parent_elem:
        li_elem = elem.find_elements_by_tag_name('li')
        for li in li_elem:
            a_elem = li.find_element_by_tag_name('a')
            link = a_elem.get_attribute('href')
            adress_list.append(link + "\n")
    write_to_text(adress_list, "wiki_urls.txt")

while True:
    get_links()
    try:
        next_page_elem = driver.find_element_by_partial_link_text("Pejy manaraka")
    except:
        print("end of all pages")
        break
    next_page_link = next_page_elem.get_attribute('href')
    driver.get(next_page_link)

driver.close()
