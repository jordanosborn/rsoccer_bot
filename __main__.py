import praw
import json
from multiprocessing import Pool
import sys
import bs4
import requests
from nltk.tokenize import word_tokenize
import pandas
from time import sleep
import re
from urllib.parse import urlsplit

# Setup zone.
if len(sys.argv) > 1 and sys.argv[1] == '-v':
    import logging
    handler = logging.StreamHandler()
    handler.setLevel(logging.DEBUG)
    logger = logging.getLogger('prawcore')
    logger.setLevel(logging.DEBUG)
    logger.addHandler(handler)

with open('secrets.json') as f:
    secrets = json.loads(f.read())

reddit = praw.Reddit(**secrets['soccer_goal_bot'])

sr = secrets['soccer_goal_bot']['subreddits']

subreddits = {key: reddit.subreddit(key) for key in sr}

class CommentChain:
    def __init__(self, top_level_comment):
        pass
    def analyse_text(self, text):
        pass

submissions = set()
submissions_to_check = set([])
valid_urls = ['streamja.com', 'streamable.com', 'streamgoals.com']

def string_contains(string):
    #country names player names etc.
    keyword_regex = re.compile(
        r"[\s]*?\[{0,1}[\s]*?[\d]+?[\s]*?\]{0,1}[\s]*?-[\s]*?\[{0,1}[\s]*?[\d]+?[\s]*?\]{0,1}|[gG][oO][aA][lL] |against |\d{0,1}\d{1}'"
    )
    out = keyword_regex.findall(string)

    return True if len(out) != 0 else False

def url_valid(url):
    #country names player names etc.
    valid = False
    for v in valid_urls:
        if url.find(v) != -1:
            valid = True
            break
    return valid


def download_file(url, output):
    r = requests.get(url, stream=True)
    with open(output, 'wb') as f:
        for chunk in r.iter_content(chunk_size=1024):
            if chunk:
                f.write(chunk)

def parse_page(string, url):
    soup = bs4.BeautifulSoup(string, 'lxml')
    base_url = "{0.scheme}://{0.netloc}/".format(urlsplit(url))
    videos = soup.find_all(['source', 'video'])
    for video in videos:
        try:
            print(video['src'])
            if video['src'].find('http') == 0:
                return video['src']
            elif video['src'].find('//') == 0:
                return 'https:' + video['src']
            else:
                return base_url + video['src']
        except KeyError:
            return None



def eventloop():
    while True:
        for submission in subreddits['soccer'].stream.submissions():
            title = submission.title
            if string_contains(title) and url_valid(submission.url):
                print(title)
                url = submission.url
                submissions.add(submission.id)
                video_url = parse_page(requests.get(url).text, url)
                print(video_url)
                if video_url is not None:
                    download_file(video_url, title + '.' + video_url.split('.')[-1][:video_url.split('.')[-1].find('?')])
        sleep(10)

if __name__ == '__main__':
    eventloop()
