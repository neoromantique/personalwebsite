import json
from feedgen.feed import FeedGenerator
from termcolor import colored
import os

# CONSTANTS
BLOG_TITLE = "Dave's Blog"
BLOG_LINK = "https://www.aizenberg.co.uk/blog/"
BLOG_DESC = "My Blog Description"
BLOG_PATH = "blog/"

# FUNCTIONS

# Load the blog from the blog directory and meta.json file

# Load the blog entries from the blog directory


def list_blog_entries() -> dict:
    blogDict = {}
    for blogItem in [a for a in os.listdir(BLOG_PATH) if os.path.isdir(BLOG_PATH + a)]:
        if not os.path.isfile(BLOG_PATH + blogItem + '/meta.json'):
            pass
        else:
            blogDict[blogItem] = load_blog_entry_meta(blogItem)
    return blogDict

# Load the blog entry meta data from the meta.json file


def load_blog_entry_meta(blogEntry: str) -> dict:
    # parse the meta.json file
    with open(BLOG_PATH + blogEntry + '/meta.json', 'r') as metaFile:
        metaDict = json.load(metaFile)
        return metaDict


# Generate the blog entry


def generate_blog_entry(blogEntry: str) -> None:
    pass

# Generate the feed


def generate_feed(blogItems: list) -> None:
    fg = FeedGenerator()
    fg.title(BLOG_TITLE)
    fg.link(href=BLOG_LINK, rel='alternate')
    fg.id(BLOG_LINK)
    fg.description(BLOG_DESC)

    for blogItem in blogItems:
        fe = fg.add_entry()
        fe.title(blogItems[blogItem].get('title'))
        fe.id(blogItems[blogItem].get('id'))
        fe.description(blogItems[blogItem].get('description'))
        fe.pubDate(blogItems[blogItem].get('date'))
        fe.link(href=BLOG_LINK + blogItem)
    fg.atom_file('blog/rss.xml')


# RUNTIME

if __name__ == "__main__":
    blogItems = list_blog_entries()
    print(colored('CI Helper 9000', 'red'), '::',
          colored('Listing blog entries', 'white'))
    for blogItem in blogItems:
        print(colored(blogItems[blogItem].get('kind'),
              'green'), colored(blogItem, 'white'))
    print(colored('', 'red'), '::', colored('Generating dynamic blog entries', 'white'), end=" " )
    print(colored('[Not implemented]', 'red'))
    # for blogItem in blogItems:
    #     generate_blog_entry(blogItem)

    print(colored('', 'red'), '::', colored('Generating ATOM feed', 'white'), end=" " )
    generate_feed(blogItems)
    print(colored('[Done]', 'green'))
