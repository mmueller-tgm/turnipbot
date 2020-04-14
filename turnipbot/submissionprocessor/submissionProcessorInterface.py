import logging
import threading
from queue import Queue
from abc import abstractmethod, ABC

from praw.models import Submission

from turnipbot.offer import Offer
from turnipbot.offerserver.offerServerInterface import OfferServerInterface

logger = logging.getLogger('submissionProcessorLogger')


class SubmissionProcessorInterface(threading.Thread, ABC):
    """ A submission Processor takes an Reddit submission from a queue, decides if it is a valid offer and extracts
    the required Data """
    def __init__(self, config, *offerServer: OfferServerInterface, queue: Queue = Queue()):
        super().__init__()
        self.config = config
        self.proc_queue = queue
        self.server = list(offerServer)
        self.daemon = True

    def put_submission(self, submission):
        """ Adds a submission to the queue """
        self.proc_queue.put(submission)

    def add_server(self, offerServer: OfferServerInterface) -> int:
        """ Adds Server instance to return valid offers to """
        self.server.append(offerServer)
        return len(self.server) - 1

    def process_submission(self, submission: Submission):
        """  """
        logger.info(f"serving offer {submission}")
        try:
            offer = self.form_offer(submission)
            for serv in self.server:
                serv.serve_offer(offer)
        except ValueError:
            pass

    @abstractmethod
    def form_offer(self, submission) -> Offer:
        pass

    def run(self) -> None:
        logger.info("Started Submission Processor")
        while True:
            try:
                self.process_submission(self.proc_queue.get())
            except Exception:
                logger.exception("Unexpected Exception was raised")
