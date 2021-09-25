import requests
import os
import random
import signal
import sys
from bs4 import BeautifulSoup
from tqdm import tqdm

if not os.path.exists(os.path.join("urls", "wiki_urls.txt")):
    raise FileNotFoundError(
        "you dont have wiki urls yet, please run wiki_url_scraping.py")

if(not os.path.exists("data") and not os.path.isdir("data")):
    os.mkdir("data")

adress_list_file = open(os.path.join("urls", "wiki_urls.txt"))
urls = adress_list_file.readlines()


if(not os.path.exists(os.path.join("urls", "wiki_last_scrape_url.txt"))):
    last_url = ""
else:
    if(sys.argv[1] == '--from-start'):
        last_url = ""
        os.remove(os.path.join("data", "wiki_dataset.txt"))
    else:
        last_url = open(os.path.join(
            "urls", "wiki_last_scrape_url.txt"), "r").readline()


def handler(signum, frame):
    res = input("Ctrl-c was pressed. Do you really want to exit? y/n ")
    if res == 'y':
        exit(1)


signal.signal(signal.SIGINT, handler)

for url in tqdm(urls):
    with open(os.path.join("urls", "wiki_last_scrape_url.txt"), "w") as f:
        f.write(url)
    if(last_url != "" and urls.index(url) < urls.index(last_url)):
        continue
    if("Asteroida" in url and random.random() < .35):
        continue
    try:
        page = requests.get(url.strip())
        soup = BeautifulSoup(page.content, 'html.parser')
        content = soup.find(id="mw-content-text").extract().get_text()

        content = content.replace("[hanova | hanova ny fango]", "").replace("\n\n\n", "\n").replace("[1]", "").replace("[2]", "").replace("[3]", "").replace(
            "[4]", "").replace("[5]", "").replace("[6]", "").replace("[7]", "").replace("[8]", "").replace("[9]", "").replace("[10]", "").encode("utf-8")

        with open(os.path.join("data", "wiki_dataset.txt"), "ab") as f:
            f.write(content + b"\n\n\n")
    except Exception as e:
        # print("WE CATCHED AN EXCEPTION HERE")
        # with open(os.path.join("urls", "wiki_last_scrape_url.txt"), "w") as f:
        #     f.write(url)
        if(e == KeyboardInterrupt):
            exit(1)
        else:
            print("error with url " + url)
