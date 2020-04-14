import sys
from typing import TextIO

from turnipbot.offerserver.offerServerInterface import OfferServerInterface
from turnipbot.offer import Offer


class TextIOStreamServer(OfferServerInterface):
    def __init__(self, stream: TextIO = sys.stdout):
        self.stream = stream

    def serve_offer(self, offer: Offer) -> None:
        line = f"{'B' if offer.buy else 'S'} {offer.datetime},{offer.author},{offer.bells},{offer.url}\n"
        self.stream.write(line)
