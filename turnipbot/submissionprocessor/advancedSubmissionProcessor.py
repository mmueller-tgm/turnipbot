import logging
import re
from word2number import w2n
from turnipbot.offer import Offer
from praw.models import Submission
from turnipbot.submissionprocessor.submissionProcessorInterface import SubmissionProcessorInterface

logger = logging.getLogger('submissionProcessorLogger')


class AdvancedSubmissionProcessor(SubmissionProcessorInterface):
    def process_submission(self, submission: Submission):
        offer = Offer(submission)
        subreddit = submission.subreddit.display_name

        for ig_str in self.config['subs'][subreddit]['ignore']:
            if ig_str in offer.title:
                logger.info(f"Ignored Submission '{submission}' due to ignore-string '{ig_str}'")
                return

        try:
            number = w2n.word_to_num(offer.title)

            logger.info(number)
        except ValueError:
            pass
        # logger.info(f"serving offer {submission}")
        # for serv in self.server:
        #     serv.serve_offer(offer)
