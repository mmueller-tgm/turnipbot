from turnipbot.submissionserver.submissionServerInterface import SubmissionServerInterface
from datetime import date
from turnipbot.offer import Offer


class FilePrinter(SubmissionServerInterface):
    @staticmethod
    def write_line(line: str, sell = True):
        with open(f"{'sell' if sell else 'buy'}-turnips-{date.today().strftime('%Y-%m-%d')}.csv", 'a+') as file:
            file.write(line)
            file.close()

    def serve_submission(self, offer: Offer) -> None:
        line = f"{offer.datetime},{offer.author},{offer.bells},{offer.url}\n"
        FilePrinter.write_line(line)

