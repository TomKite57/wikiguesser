#==============================================================================#
# Imports
import requests
from bs4 import BeautifulSoup
import random
import sys
import os
# My files
from scraper import run_scrape
from constants import *
from word_filter import all_filters_and_frequency
from utility import clear_screen

#==============================================================================#
def load_article_titles(fname):
    run_scrape()
    with open(fname, 'r') as file:
        titles = [line.strip() for line in file]
    return titles

def get_random_title(titles):
    return random.choice(titles)

def get_wikipedia_page(title):
    params = {
        "action": "parse",
        "format": "json",
        "page": title,
        "prop": "text",
        "section": 0,
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

    text = response.json()['parse']['text']
    soup = BeautifulSoup(text, 'html.parser')
    content = soup.find('div', {'class': 'mw-parser-output'})
    text = content.get_text()

    return text

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
        titles = load_article_titles(SCRAPE_FNAME)
        title = get_random_title(titles)

    my_game = game(title)
    my_game.play()
