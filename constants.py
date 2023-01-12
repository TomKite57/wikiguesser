#==============================================================================#
# Constants
WIKI_ENDPOINT = "https://en.wikipedia.org/w/api.php"

FREQUENT_FNAME = "frequent.dat"
FREQUENCY_CUTOFF = 363503

SCRAPE_FNAME = "wikiscrape.dat"

MASS_SCRAPE_FNAME = "full_scrape_with_frequent_words.json"

CUSTOM_TOKENS = ["\'\'", "``", "retrieved", "archived", "isbn", "doi", "oclc",
                 "pdf", "original", "'s", "disambiguation", "ibn", "article",
                 "cite", "related", "citations", "list", "edit", "redirects",
                 "vs", "uses", "series", "index", "outline", "part", "using", "ed.",
                 r"\\displaystyle", r"\\frac", r"\\log", r"\\text", "citation",
                 "et", "pmid", "redirect", "use", "used", "link", "l\u00fc", "pp.",
                 "di", "pp", "de", "wayback", "op", "'the", "...", "s2cid",
                 "issn", "january", "february", "march", "april", "may", "june",
                 "july", "august", "september", "october", "november", "december", "z." "e.g",
                 "2016-04-04", "i", "ii", "iii", "iv", "v", "vi", "viii", "ix", "x", "ce",
                 "press", "sq", "km2", "mi", "=p", "n_", "km", "ft", "m3", "m2", "n-1",
                 "x_", "y_", "pmc", "within", "le", "les", "archive", "bdw", "bwv",
                 "2009-12-13", "fl", "pa", "kpc", "v_", "ed", "f_", "www.constituteproject.org",
                 "2021-04-30", "2016-09-10", "2022-08-29", "b^", "el", "en", "del", "m_", "la"
                 "san", "ar5", "kpa", "torr", "eds.", "oz", "via", "978-1405177689", "mg",
                 "2020-08-25", "du", "des", "kg", "ar", "2/3", "978-0-333-78676-5", "ss",
                 "uss", "12.00", "ics", "type", "mya", "vol", "jstor", "st.", "nm",
                 "te", "li", "iso", "da", "lccn", "cm", "la", "pmc", "became", "known",
                 "among", "term", "main", "acording", "however"]


WELCOME_ASCII = \
r""" __          ___ _    _
 \ \        / (_) |  (_)
  \ \  /\  / / _| | ___  __ _ _   _  ___  ___ ___  ___ _ __
   \ \/  \/ / | | |/ / |/ _` | | | |/ _ \/ __/ __|/ _ \ '__|
    \  /\  /  | |   <| | (_| | |_| |  __/\__ \__ \  __/ |
     \/  \/   |_|_|\_\_|\__, |\__,_|\___||___/___/\___|_|
                         __/ |
                        |___/                               """

CORRECT_ASCII = \
r"""     _       _____ ____  _____  _____  ______ _____ _______      _
  /\| |/\   / ____/ __ \|  __ \|  __ \|  ____/ ____|__   __|  /\| |/\
  \ ` ' /  | |   | |  | | |__) | |__) | |__ | |       | |     \ ` ' /
 |_     _| | |   | |  | |  _  /|  _  /|  __|| |       | |    |_     _|
  / , . \  | |___| |__| | | \ \| | \ \| |___| |____   | |     / , . \
  \/|_|\/   \_____\____/|_|  \_\_|  \_\______\_____|  |_|     \/|_|\/

                                                                      """

INCORRECT_ASCII = \
r"""  ____       _   _              _            _                      _     _   _                _
 |  _ \     | | | |            | |          | |                    | |   | | (_)              | |
 | |_) | ___| |_| |_ ___ _ __  | |_   _  ___| | __  _ __   _____  _| |_  | |_ _ _ __ ___   ___| |
 |  _ < / _ \ __| __/ _ \ '__| | | | | |/ __| |/ / | '_ \ / _ \ \/ / __| | __| | '_ ` _ \ / _ \ |
 | |_) |  __/ |_| ||  __/ |    | | |_| | (__|   <  | | | |  __/>  <| |_  | |_| | | | | | |  __/_|
 |____/ \___|\__|\__\___|_|    |_|\__,_|\___|_|\_\ |_| |_|\___/_/\_\\__|  \__|_|_| |_| |_|\___(_)

                                                                                                 """

STAR_ASCII = \
r"""     _
  /\| |/\
  \ ` ' /
 |_     _|
  / , . \
  \/|_|\/

          """
