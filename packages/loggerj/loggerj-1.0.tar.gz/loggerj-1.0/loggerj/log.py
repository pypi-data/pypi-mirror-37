import os
import inspect
from loggerj import logger

DEBUG = 0
INFO = 1
WARNING = 2
ERROR = 3
CRITICAL = 4

def create(filename, message, type_logger):
    # INFO: create instance of Logger
    log = logger.Logger(filename)

    previous_frame = inspect.currentframe().f_back
    (filename, line_number, 
     function_name, lines, index) = inspect.getframeinfo(previous_frame)

    log.generate(message, filename, line_number, type_logger)
