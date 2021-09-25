"""scraping aoraha.mg with all url scraped in aoraha_url_scraping.py"""

from selenium import webdriver
from tqdm import tqdm
import os

if not os.path.exists(os.path.join("urls", "aoraha_urls.txt")):
    raise FileNotFoundError("you dont have aoraha urls yet, please run aoraha_url_scraping.py")

if(not os.path.exists("data") and not os.path.isdir("data")):
    os.mkdir("data")

driver = webdriver.Chrome()
driver.implicitly_wait(10)

adress_list_file = open(os.path.join("urls", "aoraha_urls.txt"), "r")
adress_list = adress_list_file.read().split("\n")

new_list = list(dict.fromkeys(adress_list))

print(len(adress_list), " = ", len(new_list))

for adress in tqdm(new_list):
    try:	
        driver.get(adress)
        title = "---- " + driver.find_element_by_class_name("two").text + " ----\n"
        content_elem = driver.find_element_by_class_name("entry-content").find_elements_by_tag_name("p")
        content_text = ""
        for elem in content_elem:
            content_text += elem.text + "\n"
        content_text = content_text.strip()
        with open(os.path.join("data", "aoraha_dataset.txt"), "a") as f:
            f.write(title + content_text + "\n")
    except:
        pass
driver.close()
