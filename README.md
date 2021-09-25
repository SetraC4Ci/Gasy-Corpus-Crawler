# GCC (Gasy Corpus Crawler)

GCC (Gasy Corpus Crawler) is a set of python script to scrape and create a dataset of malagasy langage articles and corpus.
There is 2 version BeautifulSoup and Selenium, BeautifulSoup Version is way much faster. you can run Selenium version also for experimenting.


## Usage
* run the python site_url_scraping.py (site_url_scraping_bs.py to use bs4 version)
* run the python site_articles_scraping.py (site_articles_scraping_bs.py to use bs4 version)

Example if you wanna scrape wiki articles

```bash
$python wiki_url_scraping.py && python wiki_articles_scraping.py
```

## Contributing
Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

Please make sure to update tests as appropriate.

## License
[MIT](https://choosealicense.com/licenses/mit/)