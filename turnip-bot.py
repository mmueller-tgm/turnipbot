import json
import queue
from SubListener import SubListener
from SubmissionProcessor import SubmissionProcessor
from SubmissionServer import *

if __name__ == "__main__":
    with open("reddit-settings.json", 'r') as config_file:
        config = json.loads(config_file.read())

        proc_queue = queue.Queue()

        sP = SubmissionProcessor(config, proc_queue, ConsoleLogger)
        sP.start()

        for sub in config['subs']:
            sl = SubListener(sub, sP)
            sl.start()
