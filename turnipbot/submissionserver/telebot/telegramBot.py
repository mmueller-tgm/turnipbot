import requests
from turnipbot.offer import Offer
from turnipbot.submissionserver.submissionServerInterface import SubmissionServerInterface
from turnipbot.submissionserver.telebot.credentials import *


class TelegramBot(SubmissionServerInterface):

    def serve_submission(self, offer: Offer):
        text = f"{'Buy' if offer.buy else 'Sell'} [{offer.datetime}] {offer.bells}B @{offer.author}\n" \
               f"URL:{offer.url}"
        requests.get(f"https://api.telegram.org/bot{bot_token}/sendMessage", params={"chat_id":chat_id, "text":text})

