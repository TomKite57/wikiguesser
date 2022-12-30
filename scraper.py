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

    return article_titles

def write_file(fname, contents):
    with open(fname, 'w+') as file:
        [file.write(f"{l}\n") for l in contents]

def run_scrape(*, force=False):
    if not os.path.exists(SCRAPE_FNAME):
        write_file(SCRAPE_FNAME, scrape_level_3())
        return

    if force:
        os.remove(SCRAPE_FNAME)
        write_file(SCRAPE_FNAME, scrape_level_3())


if __name__ == "__main__":
    run_scrape(force=True)
