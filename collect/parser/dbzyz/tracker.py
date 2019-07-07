import logging
import threading
import thread

class MovieTracker:

        def __init__(self, config, threads, task_queue):
            self.__config = config
            self.__queue = task_queue
            self.__stop = threading.Event
            self.__threads = threads
            self.__log_config = config['log']
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

        def start(self):
            self.__logger.info('started')
            for tid in self.__threads:
                self.__logger.info('starting tacker {}!'.format(tid))
                thread.start_new_thread(self.__run(),tid)

        def __run(self, tid):
            while not self.__stop:
                    vod_event = self.__queue.get()
                    self.__process(tid, vod_event)
            self.__logger.info("movie tracker {} stopped !".format(tid))

        def stop(self):
            self.__stop.set()

        def __process(self, tid, vod_event):
            self.__logger.info('{} process {}'.format(tid, vod_event))
            print(vod_event)


if __name__ == '__main__':
    tracker = MovieTracker






