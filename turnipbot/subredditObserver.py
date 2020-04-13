import praw
import threading
import logging
import json
from prawcore.exceptions import ServerError
from turnipbot.submissionProcessor import SubmissionProcessor

default_ua = 'script:turnip-bot:v2.0.0'
default_sn = 'turnip-bot'

logger = logging.getLogger('observerLogger')


class SubListener(threading.Thread):
    def __init__(self, subreddit, submissionProcessor: SubmissionProcessor, user_agent=default_ua,
                 site_name=default_sn):
        super().__init__()
        self.reddit = praw.Reddit(site_name=site_name, user_agent=user_agent)
        self.subreddit = subreddit
        self.sP = submissionProcessor

    def run(self) -> None:
        logger.info(f"Started Subreddit Listener for /r/{self.subreddit}")
        while True:
            try:
                for submission in self.reddit.subreddit(self.subreddit).stream.submissions():
                    self.sP.put_submission(submission)
                    logger.info(f"Found Submission '{submission}' by /u/{submission.author} with the title {json.dumps(submission.title)}")
            except ServerError:
                logger.info("Tempoary Serverside Issiue", exc_info=True)
            except:
                logger.exception("Unexprcted error in praw occured")
