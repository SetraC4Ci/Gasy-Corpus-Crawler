from selenium import webdriver
import os

if not os.path.exists(os.path.join("urls", "wiki_urls.txt")):
    raise FileNotFoundError("you dont have wiki urls yet, please run wiki_url_scraping.py")


if(not os.path.exists("data") and not os.path.isdir("data")):
    os.mkdir("data")

driver = webdriver.Chrome()
driver.implicitly_wait(10)

adress_list_file = open(os.path.join("urls", "wiki_urls.txt"))
adresses = adress_list_file.readlines()

for url in adresses:
    try:
        driver.get(url.strip())
        text_elem = driver.find_element_by_id("mw-content-text")
        text = str(text_elem.text).replace("[hanova | hanova ny fango]", "")
        with open(os.path.join("data", "wiki_dataset.txt"), "a") as f:
            f.write(text + "\n\n\n")
    except:
        print("error with url " + url)



# driver.get("https://mg.wikipedia.org/wiki/Famadihana")
# text_elem = driver.find_element_by_id("mw-content-text")
# print(str(text_elem.text).replace("[hanova | hanova ny fango]", ""))

driver.close()
adress_list_file.close()