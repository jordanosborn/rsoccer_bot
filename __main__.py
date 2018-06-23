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

def string_contains(string, values):
    valid = False
    for v in values:
        if string.find(v) != -1:
            valid = True
            break
    print(valid)
    return valid


def download_file(url, output):
    r = requests.get(url, stream=True)
    with open(output, 'wb') as f:
        for chunk in r.iter_content(chunk_size=1024):
            if chunk:
                f.write(chunk)

def parse_page(string):
    soup = bs4.BeautifulSoup(string, 'lxml')
    videos = soup.find_all('source')
    for video in videos:
        return video['src']

def eventloop():
    while True:
        for submission in subreddits['soccer'].stream.submissions():
            if string_contains(submission.url, valid_urls):
                title = submission.title
                print(title)
                submissions.add(submission.id)
                video_url = parse_page(requests.get(submission.url).text)
                if video_url is not None:
                    download_file(video_url, title + '.' + video_url.split('.')[-1])
            sleep(2)
        sleep(10)

if __name__ == '__main__':
    eventloop()
