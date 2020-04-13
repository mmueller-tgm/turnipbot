import json
import queue

from turnipbot.submissionserver.telebot.telegramBot import TelegramBot
from turnipbot.subredditListener import SubListener
from turnipbot.submissionProcessor import SubmissionProcessor
from turnipbot.submissionserver.consoleLogger import ConsoleLogger
from turnipbot.submissionserver.filePrinter import FilePrinter

if __name__ == "__main__":
    with open("reddit-settings.json", 'r') as config_file:
        config = json.loads(config_file.read())

        proc_queue = queue.Queue()

        sP = SubmissionProcessor(config, proc_queue, ConsoleLogger(), FilePrinter(), TelegramBot())
        sP.start()

        for sub in config['subs']:
            sl = SubListener(sub, sP)
            sl.start()
