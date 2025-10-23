import json
from feedgen.feed import FeedGenerator
import os
import sys
from datetime import datetime

# CONSTANTS
BLOG_TITLE = "Dave's Blog"
BLOG_LINK = "https://www.aizenberg.co.uk/blog/"
BLOG_DESC = "My Blog Description"
BLOG_PATH = "blog/"

# FUNCTIONS

def list_blog_entries() -> dict:
    """List all blog entries with valid meta.json files."""
    if not os.path.exists(BLOG_PATH):
        print(f"ERROR: Blog path '{BLOG_PATH}' does not exist",
              file=sys.stderr)
        sys.exit(1)

    blogDict = {}
    for blogItem in os.listdir(BLOG_PATH):
        item_path = os.path.join(BLOG_PATH, blogItem)
        if not os.path.isdir(item_path):
            continue

        meta_path = os.path.join(item_path, 'meta.json')
        if os.path.isfile(meta_path):
            meta = load_blog_entry_meta(blogItem)
            blogDict[blogItem] = meta

    if not blogDict:
        print("WARNING: No blog entries found", file=sys.stderr)

    return blogDict

def load_blog_entry_meta(blogEntry: str) -> dict:
    """Parse meta.json file. Fails on error."""
    meta_path = os.path.join(BLOG_PATH, blogEntry, 'meta.json')
    try:
        with open(meta_path, 'r') as metaFile:
            metaDict = json.load(metaFile)
    except json.JSONDecodeError as e:
        print(f"ERROR: Invalid JSON in {meta_path}: {e}",
              file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(f"ERROR: Failed to load {meta_path}: {e}",
              file=sys.stderr)
        sys.exit(1)

    # Validate required fields
    required = ['title', 'id', 'description', 'date']
    missing = [f for f in required if f not in metaDict]
    if missing:
        print(
            f"ERROR: Missing required fields in {meta_path}: "
            f"{', '.join(missing)}",
            file=sys.stderr
        )
        sys.exit(1)

    return metaDict

def generate_blog_entry(blogEntry: str) -> None:
    pass

def generate_feed(blogItems: dict) -> None:
    """Generate Atom feed from blog items."""
    if not blogItems:
        print("ERROR: Cannot generate feed with no entries",
              file=sys.stderr)
        sys.exit(1)

    fg = FeedGenerator()
    fg.title(BLOG_TITLE)
    fg.link(href=BLOG_LINK, rel='alternate')
    fg.id(BLOG_LINK)
    fg.description(BLOG_DESC)

    # Sort by date (newest first) - deterministic order
    sorted_items = sorted(
        blogItems.items(),
        key=lambda x: x[1].get('date', ''),
        reverse=True
    )

    for blogItem, meta in sorted_items:
        fe = fg.add_entry()
        fe.title(meta['title'])
        fe.id(meta['id'])
        fe.description(meta['description'])

        # Parse date if it's a string
        date = meta['date']
        if isinstance(date, str):
            try:
                date = datetime.fromisoformat(
                    date.replace('Z', '+00:00')
                )
            except ValueError as e:
                print(
                    f"ERROR: Invalid date format in {blogItem}: {e}",
                    file=sys.stderr
                )
                sys.exit(1)
        fe.pubDate(date)

        fe.link(href=BLOG_LINK + blogItem)

    output_path = os.path.join(BLOG_PATH, 'rss.xml')
    try:
        fg.atom_file(output_path)
    except Exception as e:
        print(f"ERROR: Failed to write feed: {e}", file=sys.stderr)
        sys.exit(1)

# RUNTIME

if __name__ == "__main__":
    print('-- Discovering blog entries...')
    blogItems = list_blog_entries()

    print(f'-- Found {len(blogItems)} blog entries:')
    for blogItem in blogItems:
        print(
            f"   {blogItems[blogItem].get('kind', 'unknown')}: "
            f"{blogItems[blogItem]['title']}"
        )

    print("-- Generating ATOM feed...")
    generate_feed(blogItems)
    print("✓ Feed generated successfully")
