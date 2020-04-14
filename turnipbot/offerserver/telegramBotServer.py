import requests
from turnipbot.offer import Offer
from turnipbot.offerserver.offerServerInterface import OfferServerInterface


class TelegramBotServer(OfferServerInterface):
    def __init__(self, bot_token: str, chat_id: str):
        self.bot_token = bot_token
        self.chat_id = chat_id

    def serve_offer(self, offer: Offer):
        text = f"{'Buy' if offer.buy else 'Sell'} [{offer.datetime}] {offer.bells}B @{offer.author}\n" \
               f"URL:{offer.url}"
        requests.get(f"https://api.telegram.org/bot{self.bot_token}/sendMessage",
                     params={"chat_id": self.chat_id, "text": text})
