
import logging


class MovieUpdator:

    def __init__(self, log_config, tid, task_queue, stop):
        # .Thread.__init__(self)
        self.__log_config=log_config
        self.__tid = tid
        self.__task_queue = task_queue
        self.__stop = stop
        self.__logger = logging.getLogger(__name__)
        self.__logger.setLevel(logging.INFO)
        fhandler = logging.FileHandler(self.__log_config['file'])
        fhandler.setLevel(logging.INFO)
        formatter = logging.Formatter(self.__log_config['pattern'])
        fhandler.setFormatter(formatter)
        console = logging.StreamHandler()
        console.setLevel(logging.INFO)
        self.__logger.addHandler(console)
        self.__logger.addHandler(fhandler)

