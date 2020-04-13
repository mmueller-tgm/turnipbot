import json
import logging
import sys

from turnipbot.offerserver.notificationServer import NotificationServer
from turnipbot.subredditObserver import SubListener
from turnipbot.submissionProcessor import SubmissionProcessor
from turnipbot.offerserver.consoleLogger import ConsoleLogger
from turnipbot.offerserver.filePrinter import FilePrinter
from turnipbot.offerserver.telebot.telegramBot import TelegramBot



def usage():
    pass


def main(argv):

    logging.basicConfig(handlers=[logging.FileHandler(filename="turnip-bot.log"), logging.StreamHandler(sys.stderr)],
                        level=logging.INFO, format='[%(asctime)s] %(levelname)s {%(filename)s:%(lineno)d} - %(message)s')

    with open("reddit-settings.json", 'r') as config_file:
        config = json.loads(config_file.read())

        sP = SubmissionProcessor(config, TelegramBot())#, ConsoleLogger(), FilePrinter(), NotificationServer())
        sP.start()

        for sub in config['subs']:
            SubListener(sub, sP).start()


if __name__ == "__main__":
    main(sys.argv[1:])
