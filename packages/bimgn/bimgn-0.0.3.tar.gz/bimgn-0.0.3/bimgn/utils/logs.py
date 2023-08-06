import logging
import coloredlogs
import graypy
import os


class Log:

    def __init__(self):
        self.mode = os.environ['MODE']

    @staticmethod
    def set_mode(args):
        if args.d is True:
            mode = 'Debug'
        else:
            mode = 'Production'

        return mode

    @staticmethod
    def set_log(name, dirs=[]):

        log = logging.getLogger(name)
        log.setLevel(logging.DEBUG)

        for d in dirs:
            # create a file handler
            handler = logging.FileHandler(d)
            handler.setLevel(logging.DEBUG)
            formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
            handler.setFormatter(formatter)

            log.addHandler(handler)

        # Create stream handler
        coloredlogs.install(level='INFO', logger=log)

        log_ip = os.getenv('LOGIP')
        if log_ip is not None:
            handler_gp = graypy.GELFHandler(log_ip, 12201)
            log.addHandler(handler_gp)

        return log
