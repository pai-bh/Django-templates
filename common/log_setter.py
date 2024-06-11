import os
import time
import logging
from logging.handlers import TimedRotatingFileHandler
from django.conf import settings


class ReTimedRotatingFileHandler(TimedRotatingFileHandler):
    def __init__(self, filename, when='h', interval=1, backupCount=0, encoding=None, delay=False, utc=False):
        super().__init__(filename, when, interval, backupCount, encoding, delay, utc)

    def doRollover(self):
        if self.stream:
            self.stream.close()
            self.stream = None

        current_time = int(time.time())
        dst_now = time.localtime(current_time)[-1]
        t = self.rolloverAt - self.interval
        if self.utc:
            time_tuple = time.gmtime(t)
        else:
            time_tuple = time.localtime(t)
            dst_then = time_tuple[-1]
            if dst_now != dst_then:
                if dst_now:
                    addend = 3600
                else:
                    addend = -3600
                time_tuple = time.localtime(t + addend)
        dfn = self.baseFilename + "." + time.strftime(self.suffix, time_tuple)

        if not os.path.exists(dfn) and os.path.exists(self.baseFilename):
            os.rename(self.baseFilename, dfn)
        if self.backupCount > 0:
            for s in self.getFilesToDelete():
                os.remove(s)
        if not self.delay:
            self.mode = "a"
            self.stream = self._open()
        new_rollover_at = self.computeRollover(current_time)
        while new_rollover_at <= current_time:
            new_rollover_at = new_rollover_at + self.interval
        if (self.when == 'MIDNIGHT' or self.when.startswith('W')) and not self.utc:
            dst_at_rollover = time.localtime(new_rollover_at)[-1]
            if dst_now != dst_at_rollover:
                if not dst_now:
                    addend = -3600
                else:
                    addend = 3600
                new_rollover_at += addend
        self.rolloverAt = new_rollover_at


def getLogger(name=None):
    logger = logging.getLogger(name)
    logger.setLevel(settings.LOG_LEVEL)

    formatter = logging.Formatter("%(asctime)s - [%(levelname)s] - [%(name)s:%(filename)s:%(lineno)d] - %(message)s")

    log_directory = "./logs"
    if not os.path.exists(log_directory):
        os.makedirs(log_directory)

    console = logging.StreamHandler()
    console.setFormatter(formatter)
    console.setLevel(settings.LOG_LEVEL)

    file_handler_info = TimedRotatingFileHandler(
        filename=os.path.join(log_directory, f"{name}_info.log"),
        when="midnight", interval=1, encoding="utf-8", backupCount=30)
    file_handler_info.setFormatter(formatter)
    file_handler_info.setLevel(settings.LOG_LEVEL)

    file_handler_error = TimedRotatingFileHandler(
        filename=os.path.join(log_directory, f"{name}_error.log"),
        when="midnight", interval=1, encoding="utf-8", backupCount=30)
    file_handler_error.setFormatter(formatter)
    file_handler_error.setLevel(logging.ERROR)

    if not logger.hasHandlers():
        logger.addHandler(console)
        logger.addHandler(file_handler_info)
        logger.addHandler(file_handler_error)

    return logger
