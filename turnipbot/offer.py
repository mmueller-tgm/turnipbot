from datetime import datetime
from praw.models import Submission


class Offer:
    author: str
    title: str
    url: str
    datetime: datetime
    bells: int
    buy: bool
    sell: bool

    def __init__(self, submission:Submission):
        self.title = submission.title.lower()
        self.author = submission.author
        self.url = f"https://reddit.com{submission.permalink}"
        self.datetime = datetime.fromtimestamp(submission.created_utc)
        self.buy = False
        self.sell = False

    def __str__(self):
        return f"{'B' if self.buy else 'S'} [{self.datetime}] /u/{self.author} {self.bells}Bells {self.url}"