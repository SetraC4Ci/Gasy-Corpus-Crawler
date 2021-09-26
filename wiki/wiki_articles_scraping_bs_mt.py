import os
import random
from typing import List
import requests
import signal
import sys
import threading
from bs4 import BeautifulSoup
from tqdm import tqdm
from multiprocessing import Process, cpu_count

if not os.path.exists(os.path.join("urls", "wiki_urls.txt")):
    raise FileNotFoundError(
        "you dont have wiki urls yet, please run wiki_url_scraping.py")

if(not os.path.exists("data") and not os.path.isdir("data")):
    os.mkdir("data")

adress_list_file = open(os.path.join("urls", "wiki_urls.txt"))
urls = adress_list_file.readlines()


if(not os.path.exists(os.path.join("urls", "wiki_last_scrape_url_2.txt"))):
    last_url = ""
else:
    if(sys.argv[1] == '--from-start'):
        last_url = ""
        os.remove(os.path.join("data", "wiki_dataset_2.txt"))
    else:
        last_url = open(os.path.join(
            "urls", "wiki_last_scrape_url_2.txt"), "r").readline()


def scrape(url_to_scrape: list, process_nr: int, thread_nr: int):
    for url in tqdm(url_to_scrape, desc="Process" + str(process_nr) + "Thread"+str(thread_nr)):
        if("Asteroida" in url and random.random() < .35):
            return ""
        try:
            page = requests.get(url.strip())
            soup = BeautifulSoup(page.content, 'html.parser')
            content = soup.find(id="mw-content-text").get_text()

            content = content.replace("[hanova | hanova ny fango]", "").replace("\n\n\n", "\n").replace("[1]", "").replace("[2]", "").replace("[3]", "").replace(
                "[4]", "").replace("[5]", "").replace("[6]", "").replace("[7]", "").replace("[8]", "").replace("[9]", "").replace("[10]", "").encode("utf-8")

            # return content + b"\n\n\n"
            with open(os.path.join("data", "wiki_dataset_" + str(process_nr) + "_" + str(thread_nr) + ".txt"), "ab") as f:
                f.write(content + b"\n\n\n")
        except Exception as e:
            if(e == KeyboardInterrupt):
                exit(1)
            else:
                with open(os.path.join("urls", "wiki_failed.txt"), "a", encoding="utf-8") as f:
                    f.write(url + "\n")


def handler(signum, frame):
    res = input("Ctrl-c was pressed. Do you really want to exit? y/n ")
    if res == 'y':
        exit(1)


signal.signal(signal.SIGINT, handler)

def threadTask(u_li: list, p=1, nt=8):
    nthreads = nt
    threads = []
    for t in range(nthreads):
        start = int(t*(len(u_li)/nthreads))
        end = int((len(u_li)/nthreads)*(t+1))
        the = u_li[start: end] if t < nthreads-1 else u_li[start:]
        t = threading.Thread(target=scrape, args=(the, p, t))
        t.start()
        threads.append(t)
    for t in threads:
        t.join()
    print("Exiting Main Thread")

def processTaskWithTread(np=4, nt=8):
    nprocess = np
    processes = [ ]
    for p in range(nprocess):
        start = int(p*(len(urls)/nprocess))
        end = int((len(urls)/nprocess)*(p+1))
        the = urls[start: end] if p < nprocess-1 else urls[start:]
        p = Process(target=threadTask, args=(the, p, nt))
        p.start()
        processes.append(p)
    for p in processes:
        p.join()
    print("Exited main process")

def processTaskNoThread(np=4):
    nprocess = np
    processes = [ ]
    for p in range(nprocess):
        start = int(p*(len(urls)/nprocess))
        end = int((len(urls)/nprocess)*(p+1))
        the = urls[start: end] if p < nprocess-1 else urls[start:]
        p = Process(target=scrape, args=(the, p, 0))
        p.start()
        processes.append(p)
    for p in processes:
        p.join()
    print("Exited main process")

if __name__ == '__main__':
    processTaskNoThread(np=cpu_count())