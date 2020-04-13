from datetime import datetime, date
import re
from threading import Thread
from turnipbot.offer import Offer
from praw.models import Submission
from queue import Queue
from turnipbot.submissionserver.submissionServerInterface import SubmissionServerInterface


class SubmissionProcessor(Thread):
    """
        The SubmissionProcessor collects submissions from different Subreddits in it's queue, processes them and sends them further to different Servers (as in to serve to something)
    """
    def __init__(self, config, proc_queue: Queue, *submissionServer: SubmissionServerInterface):
        super().__init__()
        self.config = config
        self.proc_queue = proc_queue
        self.server = list(submissionServer)

    def add_server(self, subServ: SubmissionServerInterface):
        self.server.append(subServ)

    def process_submission(self, subm: Submission):
        offer = Offer(subm)

        subreddit = subm.subreddit.display_name
        for ig_str in self.config['subs'][subreddit]['ignore']:
            if ig_str in offer.title:
                pass

        if datetime.combine(date.today(), datetime.min.time()).timestamp() > subm.created_utc:
            return

        for buy_str in self.config['subs'][subreddit]['buying']:
            if buy_str in offer.title:
                offer.buy = True

        for sell_str in self.config['subs'][subreddit]['selling']:
            if sell_str in offer.title:
                offer.sell = True

        if offer.buy == offer.sell:
            return

        if offer.sell:
            b = re.findall('\d{3}', offer.title)
        else:
            b = re.findall('\d{2}', offer.title)

        if len(b) > 0:
            offer.bells = int(b[0])
            for serv in self.server:
                serv.serve_submission(offer)

    def run(self) -> None:
        while True:
            self.process_submission(self.proc_queue.get())