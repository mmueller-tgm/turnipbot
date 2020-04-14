import logging
from datetime import datetime, timedelta
import re
import json
from turnipbot.offer import Offer
from praw.models import Submission
from turnipbot.submissionprocessor.submissionProcessorInterface import SubmissionProcessorInterface

logger = logging.getLogger('SimpleSubmissionProcessorLogger')


class SimpleSubmissionProcessor(SubmissionProcessorInterface):
    """ This Submission Processor assumes all buy/sell offers are well formed and are not trying to defeat bots """
    def form_offer(self, submission) -> Offer:
        offer = Offer(submission)
        subreddit = submission.subreddit.display_name

        for ig_str in self.config['subs'][subreddit]['ignore']:
            if ig_str in offer.title:
                logger.info(f"Ignored Submission '{submission}' due to ignore-string '{ig_str}'")
                raise ValueError

        for buy_str in self.config['subs'][subreddit]['buying']:
            if buy_str in offer.title:
                offer.buy = True

        for sell_str in self.config['subs'][subreddit]['selling']:
            if sell_str in offer.title:
                offer.sell = True

        if offer.buy == offer.sell:
            logger.info(f"Ignored submission '{submission}' due to confusing title {json.dumps(submission.title)}")
            raise ValueError

        if offer.sell:
            b = re.findall('\d{3}', offer.title) # []
            if len(b) > 0:
                offer.bells = int(b[0])
                if offer.bells < self.config['general']['sell-setprice']:
                    logger.info(f"Ignored submission '{submission}' due to low sell-price ({offer.bells}B)")
                    raise ValueError
            else:
                logger.info(f"Ignored submission '{submission}' due to confusing title {json.dumps(submission.title)}")
                raise ValueError
        else:
            b = re.findall('\d{2}', offer.title)
            if len(b) > 0:
                offer.bells = int(b[0])
                if offer.bells > self.config['general']['buy-setprice']:
                    logger.info(f"Ignored submission '{submission}' due to high buy-price ({offer.bells}B)")
                    raise ValueError
            else:
                logger.info(f"Ignored submission '{submission}' due to confusing title {json.dumps(submission.title)}")
                raise ValueError

        if (datetime.now()-timedelta(hours=1)).timestamp() > submission.created_utc:
            logger.info(f"Ignored submission '{submission}' due to age {datetime.now()-datetime.fromtimestamp(submission.created_utc)}")
            raise ValueError

        return offer
