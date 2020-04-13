from turnipbot.offer import Offer


class OfferServerInterface:
    def serve_offer(self, offer: Offer) -> None:
        pass
