import os
import requests
import signal
import threading

from tqdm import tqdm
from bs4 import BeautifulSoup
from multiprocessing import Process, cpu_count


if not os.path.exists(os.path.join("urls", "aoraha_urls.txt")):
    raise FileNotFoundError(
        "you dont have aoraha urls yet, please run aoraha_url_scraping.py")

if(not os.path.exists("data") and not os.path.isdir("data")):
    os.mkdir("data")

adress_list_file = open(os.path.join("urls", "aoraha_urls.txt"), "r")
adress_list = adress_list_file.readlines()

new_list = list(dict.fromkeys(adress_list))

# print(len(adress_list), " = ", len(new_list))


def scrape(url_list: list, process_nr: int, thread_nr: int):
    for url in tqdm(url_list):
        try:
            page = requests.get(url)
            soup = BeautifulSoup(page.content, 'html.parser')
            #title = soup.find(class_="two").get_text()
            content_text = soup.find(class_="entry-content").get_text().strip().encode("utf-8")
            with open(os.path.join("data", "aoraha_dataset_" + str(process_nr) + "_" + str(thread_nr) + ".txt"), "ab") as f:
                f.write(content_text + b"\n\n")
        except:
            pass


def handler(signum, frame):
    res = input("Ctrl-c was pressed. Do you really want to exit? y/n ")
    if res == 'y':
        exit(1)


signal.signal(signal.SIGINT, handler)

def divideListBy(nb: int, lst: list):
    return [lst[i::nb] for i in range(nb)]


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

def processTaskWithTread(urls: list, np=4, nt=8):
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

def processTaskNoThread(urls: list, np=4):
    nprocess = np
    processes = [ ]
    urls = divideListBy(nprocess, urls)
    for p in range(nprocess):
        # start = int(p*(len(urls)/nprocess))
        # end = int((len(urls)/nprocess)*(p+1))
        # the = urls[start: end] if p < nprocess-1 else urls[start:]
        p = Process(target=scrape, args=(urls[p], p, 0), name="aoraha_scraping"+str(p))
        p.start()
        processes.append(p)
    for p in processes:
        p.join()
    print("Exited main process")

if __name__ == '__main__':
    processTaskNoThread(urls=new_list, np=cpu_count())
