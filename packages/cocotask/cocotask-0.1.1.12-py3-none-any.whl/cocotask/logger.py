# -*- coding: utf-8 -*-
import logging
import sys
import os


def init(name, logfile, level=logging.DEBUG, with_console=True):
    global logger
    logger = logging.getLogger(name)
    logger.setLevel(level)

    formatter = logging.Formatter("[%(levelname)-7s][%(asctime)s][%(filename)s:%(lineno)3d] %(message)s",
                                  "%Y/%m/%d %H:%M:%S")

    if with_console:
        h1 = logging.StreamHandler(sys.stdout)
        h1.setFormatter(formatter)
        logger.addHandler(h1)

    d = os.path.dirname(logfile)
    if d != "" and not os.path.exists(d):
        try:
            os.makedirs(os.path.dirname(logfile))
        except OSError as e:
            logger.warning("Unable to create log file at %s, Exp -> %s" % (logfile, repr(e)))
            return logger

    h2 = logging.FileHandler(logfile)
    h2.setFormatter(formatter)
    logger.addHandler(h2)

    return logger


logger = init(__name__, os.getenv("COCOTASK_LOG", "cocotask.log"))
