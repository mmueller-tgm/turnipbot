import logging
from datetime import datetime, timedelta
import re
import json
from threading import Thread
from turnipbot.offer import Offer
from praw.models import Submission
from queue import Queue
from turnipbot.offerserver.offerServerInterface import OfferServerInterface

logger = logging.getLogger('submissionProcessorLogger')

class SubmissionProcessor(Thread):
    def __init__(self, config, *offerServer: OfferServerInterface):
        super().__init__()
        self.config = config
        self.server = list(offerServer)
        self.proc_queue = Queue()

    def put_submission(self, sub):
        self.proc_queue.put(sub)

    def add_server(self, offerServ: OfferServerInterface) -> int:
        self.server.append(offerServ)
        return len(self.server) - 1

    def process_submission(self, submission: Submission):
        offer = Offer(submission)
        subreddit = submission.subreddit.display_name

        for ig_str in self.config['subs'][subreddit]['ignore']:
            if ig_str in offer.title:
                logger.info(f"Ignored Submission '{submission}' due to ignore-string '{ig_str}'")
                return

        for buy_str in self.config['subs'][subreddit]['buying']:
            if buy_str in offer.title:
                offer.buy = True

        for sell_str in self.config['subs'][subreddit]['selling']:
            if sell_str in offer.title:
                offer.sell = True

        if offer.buy == offer.sell:
            logger.info(f"Ignored submission '{submission}' due to confusing title {json.dumps(submission.title)}")
            return

        if offer.sell:
            b = re.findall('\d{3}', offer.title)
            if len(b) > 0:
                offer.bells = int(b[0])
                if offer.bells < self.config['general']['sell-setprice']:
                    logger.info(f"Ignored submission '{submission}' due to low sell-price ({offer.bells}B)")
                    return
            else:
                return
        else:
            b = re.findall('\d{2}', offer.title)
            if len(b) > 0:
                offer.bells = int(b[0])
                if offer.bells > self.config['general']['buy-setprice']:
                    logger.info(f"Ignored submission '{submission}' due to high buy-price ({offer.bells}B)")
                    return
            else:
                logger.info(f"Ignored submission '{submission}' due to confusing title {json.dumps(submission.title)}")
                return

        if (datetime.now()-timedelta(hours=1)).timestamp() > submission.created_utc:
            logger.info(f"Ignored submission '{submission}' due to age {datetime.now()-datetime.fromtimestamp(submission.created_utc)}")
            return

        logger.info(f"serving offer {submission}")
        for serv in self.server:
            serv.serve_offer(offer)

    def run(self) -> None:
        logger.info("Started Submission Processor")
        while True:
            try:
                self.process_submission(self.proc_queue.get())
            except:
                logger.exception("Unexpected Exception was raised")