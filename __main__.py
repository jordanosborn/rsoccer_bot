import praw
import json
from multiprocessing import Pool
import sys
import requests

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

def main():
    for submission in subreddits['soccer'].hot(limit=10):
        print(submission.title)  # Output: the submission's title
        print(submission.score)  # Output: the submission's score
        print(submission.id)     # Output: the submission's ID
        print(submission.url)    #

if __name__ == '__main__':
    main()