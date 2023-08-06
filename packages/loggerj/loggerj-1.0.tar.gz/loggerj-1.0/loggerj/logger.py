import logging

DEBUG = 0
INFO = 1
WARNING = 2
ERROR = 3

class Logger():
    def __init__(self, file_name):
        self._FORMAT = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
        logging.basicConfig(filename = file_name + ".log", format = self._FORMAT)
    
    def _create_logger(self, current_file_name = None, current_line_number = None):
        self.logger = logging.getLogger("(path: " + repr(current_file_name) + ", line number (approximate): " + repr(current_line_number) + ")")
        self.logger.setLevel(logging.DEBUG)
        
        console_handler = logging.StreamHandler()
        console_handler.setLevel(logging.DEBUG)
    
        formatter = logging.Formatter(self._FORMAT)
        console_handler.setFormatter(formatter)
    
        self.logger.addHandler(console_handler)
    
    def generate(self, message, current_file_name, current_line_number, type_logger):
        if(type_logger is DEBUG):
            self._debug(message, current_file_name, current_line_number)
        elif(type_logger is INFO):
            self._info(message, current_file_name, current_line_number)
        elif(type_logger is WARNING):
            self._warning(message, current_file_name, current_line_number)
        elif(type_logger is ERROR):
            self._error(message, current_file_name, current_line_number)
        elif(type_logger is CRITICAL):
            self._critical(message, current_file_name, current_line_number)

    def _debug(self, message, current_file_name, current_line_number):
        self._create_logger(current_file_name, current_line_number)
        self.logger.debug(message)

    def _info(self, message, current_file_name, current_line_number):
        self._create_logger(current_file_name, current_line_number)
        self.logger.info(message)

    def _warning(self, message, current_file_name, current_line_number):
        self._create_logger(current_file_name, current_line_number)
        self.logger.warning(message)

    def _error(self, message, current_file_name, current_line_number):
        self._create_logger(current_file_name, current_line_number)
        self.logger.error(message)

    def _critical(self, message, current_file_name, current_line_number):
        self._create_logger(current_file_name, current_line_number)
        self.logger.critical(message)
