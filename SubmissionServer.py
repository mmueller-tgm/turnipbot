import threading
from datetime import date
from Offer import Offer


class SubmissionServerInterface:
    def serve_submission(self, offer: Offer) -> None:
        pass


class FilePrinter(SubmissionServerInterface):
    @staticmethod
    def write_line(line: str, sell = True):
        with open(f"{'sell' if sell else 'buy'}-turnips-{date.today().strftime('%Y-%m-%d')}.csv", 'a+') as file:
            file.write(line)
            file.close()

    def serve_submission(self, offer: Offer) -> None:
        line = f"{offer.datetime},{offer.author},{offer.bells},{offer.url}\n"
        FilePrinter.write_line(line)


class ConsoleLogger(SubmissionServerInterface):
    def serve_submission(self, offer: Offer) -> None:
        line = f"{offer.datetime},{offer.author},{offer.bells},{offer.url}\n"
        print(f"{'B' if offer.buy else 'S'} {line}", end="")
