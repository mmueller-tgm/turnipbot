from turnipbot.submissionserver.submissionServerInterface import SubmissionServerInterface
from turnipbot.offer import Offer


class ConsoleLogger(SubmissionServerInterface):
    def serve_submission(self, offer: Offer) -> None:
        line = f"{offer.datetime},{offer.author},{offer.bells},{offer.url}\n"
        print(f"{'B' if offer.buy else 'S'} {line}", end="")
