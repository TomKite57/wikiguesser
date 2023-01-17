#==============================================================================#
# Imports
import requests
from bs4 import BeautifulSoup, NavigableString, Tag
import random
import sys
import os
import json
from tqdm import tqdm
import re
# My files
from scraper import run_scrape
from constants import *
from word_filter import all_filters_and_frequency
from utility import clear_screen
import unicodedata

#==============================================================================#
def load_article_titles(fname):
    run_scrape()
    titles = []
    urls = []
    with open(fname, 'r') as file:
        for line in file:
            t, u = line.strip().split("<=>")
            titles.append(t)
            urls.append(u)
    return titles, urls

def get_random_title(titles, urls):
    rand_ind = random.randrange(len(urls))
    return titles[rand_ind], urls[rand_ind]

def filter_children(soup):
    blacklist = ['External_links', 'Primary_sources', 'Scholarly_articles',
                 'Books', 'General_and_cited_references', 'Citations',
                 'Explanatory_notes', 'Notes', 'See_also']
    for child in soup.find_all():
        if child is None or child.attrs is None:
            continue
        if child.has_attr('role') and child.get('role') == 'navigation':
            child.decompose()
        elif child.has_attr('class') and 'mw-headline' in child.get('class'):
            if child.has_attr('id') and child.get('id') in blacklist:
                parent = child.parent
                next_sibling = parent.next_sibling
                while next_sibling is not None:
                    next_next_sibling = next_sibling.next_sibling
                    if not isinstance(next_sibling, NavigableString):
                        next_sibling.decompose()
                    next_sibling = next_next_sibling
                parent.decompose()



def get_wikipedia_page(title):
    params = {
        "action": "parse",
        "format": "json",
        "page": title,
        "prop": "text",
        #"section": -1,
        "rvprop": "content",
        "utf8": 1,
        "formatversion": 2,
        "origin": "*"
    }

    response = requests.get(WIKI_ENDPOINT, params=params)

    if response.status_code != 200:
        error_message = f"An error occurred: {response.status_code}"
        print(error_message)
        raise Exception(error_message)

    try:
        text = response.json()['parse']['text']
        soup = BeautifulSoup(text, 'html.parser')
        filter_children(soup)

        #prettyHTML = soup.prettify()   #prettify the html
        #print(prettyHTML)
        #with open("html_dump.txt", 'w') as file:
        #    file.write(prettyHTML)
        #return

        text = soup.get_text()
    except:
        print(f"Failed to get wikipedia page: {title}")
        for k, v in response.json().items():
            print(f"{k} => {v}")
        raise Exception()

    return text

def custom_token_in_hints(hints):
    for word in CUSTOM_TOKENS:
        if word in set(hints):
            return True
    return False

def mass_scrape():
    if (not os.path.exists(MASS_SCRAPE_FNAME)):
        with open(MASS_SCRAPE_FNAME, 'w') as file:
            pass

    with open(MASS_SCRAPE_FNAME, 'r') as openfile:
        if (os.stat(MASS_SCRAPE_FNAME).st_size != 0):
            current_scrape = json.load(openfile)
        else:
            current_scrape = dict()

    all_titles, _ = load_article_titles(SCRAPE_FNAME)
    for title in tqdm(all_titles):
        ascii_title = unicodedata.normalize('NFKD', title).encode('ascii', 'ignore').decode('UTF-8')

        if ascii_title in current_scrape and not custom_token_in_hints(current_scrape[ascii_title]):
            continue

        hints = all_filters_and_frequency(get_wikipedia_page(title), title)[::-1]

        current_scrape[ascii_title] = hints

        with open(MASS_SCRAPE_FNAME, "w") as outfile:
            outfile.write(json.dumps(current_scrape, indent=4))


class game():
    def __init__(self, title):
        self.title = title
        self.ordered_guesses = all_filters_and_frequency(get_wikipedia_page(self.title), self.title)
        self.guess_count = 0
        self.prev_guesses = []
        self.revealed_words = []

    def welcome_message(self):
        print(WELCOME_ASCII)
        print("A popular Wikipedia article has been picked at random.")
        print("Guess the title of the article to reveal common words from that article.")
        print("Press enter to continue")
        input()

    def more_turns(self):
        return len(self.ordered_guesses)!=0

    def secret_print(self):
        str = " ".join(["_" if ch!=" " else " " for ch in self.title])

        str += "  ("
        title_words = self.title.split()
        for i, t in enumerate(title_words):
            str += f"{len(t)}"
            if i != len(title_words)-1:
                str += ","
        str += ")"

        print(str)

    def public_print(self):
        print("The article is: ")
        print(" ".join(self.title))

    def reveal_new_word(self):
        self.revealed_words.append(self.ordered_guesses.pop())

    def print_all_clues(self):
        total = len(self.ordered_guesses) + len(self.revealed_words)
        current = len(self.revealed_words)
        current_str = str(current)

        num_space = len(str(total))
        left_space = len(" (/) ") + 2*num_space

        current_str = ' '*(num_space-len(current_str)) + current_str

        for i, w in enumerate(self.revealed_words):
            if i==len(self.revealed_words)-1:
                print(fr" ({current_str}/{total}) [{w}]")
            else:
                print(fr"{' '*left_space}[{w}]")

    def play(self):
        clear_screen()
        self.welcome_message()

        while (self.more_turns()):
            clear_screen()
            self.reveal_new_word()
            self.secret_print()
            self.print_all_clues()
            user_guess = input("Guess the wikipedia article: ")
            #print("#"*25)
            if (user_guess.lower() == self.title.lower()):
                self.win_state()
                return
        self.lose_state()

    def win_state(self):
        print(CORRECT_ASCII)
        self.public_print()

    def lose_state(self):
        print(INCORRECT_ASCII)
        self.public_print()



if __name__ == "__main__":
    if (len(sys.argv) > 1):
        title = " ".join(sys.argv[1:])
    else:
        titles, urls = load_article_titles(SCRAPE_FNAME)
        title, url = get_random_title(titles, urls)

    if title == "mass_scrape":
        mass_scrape()
    else:
        my_game = game(title)
        #my_game.play()
        print(my_game.title)
        print(my_game.ordered_guesses)
