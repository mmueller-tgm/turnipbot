import praw
import threading
from SubmissionProcessor import SubmissionProcessor

default_ua = 'script:turnip-bot:v2.0.0 (by /u/maximus5113)'
default_sn = 'turnip-bot'


class SubListener(threading.Thread):
    def __init__(self, subreddit, submissionProcessor: SubmissionProcessor, user_agent=default_ua, site_name=default_sn):
        super().__init__()
        self.reddit = praw.Reddit(site_name=site_name, user_agent=user_agent)
        self.subreddit = subreddit
        self.sP = submissionProcessor

    def run(self) -> None:
        for submission in self.reddit.subreddit(self.subreddit).stream.submissions():
            self.sP.proc_queue.put(submission)
