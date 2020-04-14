import json
import logging
import sys

from turnipbot.offerserver.textIOStreamServer import TextIOStreamServer
from turnipbot.subredditObserver import SubListener
from turnipbot.submissionprocessor.simpleSubmissionProcessor import SimpleSubmissionProcessor


def usage():
    pass


def main(argv):
    logging.basicConfig(handlers=[logging.FileHandler(filename="turnip-bot.log"), logging.StreamHandler(sys.stderr)],
                        level=logging.INFO,
                        format='[%(asctime)s] %(levelname)s {%(filename)s:%(lineno)d} - %(message)s')

    with open("reddit-settings.json", 'r') as config_file:
        with open("telegram-credentials.json", 'r') as t_conf_file:
            config = json.loads(config_file.read())
            t_conf = json.loads(t_conf_file.read())

            # available Servers: TextIOStreamServer, NotificationServer, TelegramBotServer, FileWriterServer
            servers = [TextIOStreamServer()]#, TelegramBotServer(t_conf['bot_token'], t_conf'chat_id'])]

            processor = SimpleSubmissionProcessor(config, *servers)
            t_list = list([processor])

            # Running multiple instances can be done like this:
            # t_list.append(processor.__class__(config, *processor.server, queue=processor.proc_queue))
            # Offer Servers have to be thread safe. When they are not, each processor needs it's own instance of a Server

            for sub in config['subs']:
                t_list.append(SubListener(sub, processor))

            try:
                for t in t_list:
                    t.start()
                for t in t_list:
                    t.join()
            except KeyboardInterrupt as e:
                pass


if __name__ == "__main__":
    main(sys.argv[1:])
