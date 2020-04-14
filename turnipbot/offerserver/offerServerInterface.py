from abc import ABC, abstractmethod

from turnipbot.offer import Offer


class OfferServerInterface(ABC):
    @abstractmethod
    def serve_offer(self, offer: Offer) -> None:
        pass
