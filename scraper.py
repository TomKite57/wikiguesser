#==============================================================================#
# Imports
import requests
from bs4 import BeautifulSoup
import os
from constants import *

def file_exists(fname):
    try:
        file = open(fname, 'r')
        file.close()
        return True
    except FileNotFoundError:
        return False

def get_candidate_tags(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.text, "html.parser")
    return soup.find_all("a")

def scrape_level_3():
    url = "https://en.wikipedia.org/wiki/Wikipedia:Vital_articles"
    article_titles = []
    URLs = []
    STARTED = False

    for elem in get_candidate_tags(url):
        title = elem.text
        if title=="FFLC":
            STARTED = True
            continue
        if title=="Wikipedia:WikiProject Vital Articles":
            break

        if (STARTED and title != "" and len(title) > 1 and elem.class_!="image" and not title.startswith("Level")):
            article_titles.append(title)
            URLs.append("https://en.wikipedia.org" + elem.attrs["href"])

    return article_titles, URLs

def write_file(fname, titles, urls):
    with open(fname, 'w+') as file:
        [file.write(f"{t}<=>{u}\n") for t, u in zip(titles, urls)]

def run_scrape(*, force=False):
    if not os.path.exists(SCRAPE_FNAME):
        articles, urls = scrape_level_3()
        write_file(SCRAPE_FNAME, articles, urls)
        return

    if force:
        os.remove(SCRAPE_FNAME)
        articles, urls = scrape_level_3()
        write_file(SCRAPE_FNAME, articles, urls)


if __name__ == "__main__":
    run_scrape(force=True)
