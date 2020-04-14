from datetime import date
from turnipbot.offer import Offer
from turnipbot.offerserver.offerServerInterface import OfferServerInterface


class FileWriterServer(OfferServerInterface):
    @staticmethod
    def write_line(line: str, sell = True):
        with open(f"{'sell' if sell else 'buy'}-turnips-{date.today().strftime('%Y-%m-%d')}.csv", 'a+') as file:
            file.write(line)
            file.close()

    def serve_offer(self, offer: Offer) -> None:
        line = f"{offer.datetime},{offer.author},{offer.bells},{offer.url}\n"
        FileWriterServer.write_line(line, offer.sell)

