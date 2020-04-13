import notify2

from turnipbot.offer import Offer
from turnipbot.offerserver.offerServerInterface import OfferServerInterface


class NotificationServer(OfferServerInterface):
    def __init__(self):
        notify2.init("Turnip NotificationServer")

    def serve_offer(self, offer: Offer) -> None:
        notify2.Notification(f"{'Buying' if offer.sell else 'Selling'}@{offer.bells}Bells", f"{offer.url}").show()
