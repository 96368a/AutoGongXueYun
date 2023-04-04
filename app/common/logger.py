import logging
from logging.handlers import TimedRotatingFileHandler
import os
import sys

os.makedirs('./logs', exist_ok=True)
logger = logging.getLogger()  
if len(logger.handlers) == 0: #避免重复
    level = logging.DEBUG if sys.gettrace() else logging.INFO
    filename = './logs/default.log'
    format = '%(asctime)s %(levelname)s %(module)s.%(funcName)s Line:%(lineno)d %(message)s'
    hdlr = TimedRotatingFileHandler(filename,"M",1,3)
    def namer(name):
        return name + ".log"
    hdlr.namer = namer
    fmt = logging.Formatter(format)
    hdlr.setFormatter(fmt)
    logger.addHandler(hdlr)
    logger.setLevel(level)