from turnipbot.offerserver.offerServerInterface import OfferServerInterface
from turnipbot.offer import Offer


class ConsoleLogger(OfferServerInterface):
    def serve_offer(self, offer: Offer) -> None:
        line = f"{offer.datetime},{offer.author},{offer.bells},{offer.url}\n"
        print(f"{'B' if offer.buy else 'S'} {line}", end="")
