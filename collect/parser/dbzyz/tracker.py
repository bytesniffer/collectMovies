import logging
import _thread
import threading
from db.database import MacVod
import time
import sys

class MovieTracker:

        def __init__(self, config, threads, task_queue):
            self.__config = config
            self.__task_queue = task_queue
            self.__stop = threading.Event()
            self.__threads = threads
            self.__log_config = config['log']
            self.__mac_vod_db = MacVod(config['log'], config['dbzyzmactype'], config['database'])
            self.__movie_id_set = self.__all_movie_ids()
            self.__tv_stats=self.__all_tv_id_stat()
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
            for tid in range(self.__threads):
                self.__logger.info('starting tacker {}!'.format(tid))
                _thread.start_new_thread(self.run, (tid,))

        def run(self, tid):
            while not self.__stop.is_set():
                vod_event = self.__task_queue.get()
                self.__process(tid, vod_event)
            self.__logger.info("movie tracker {} stopped !".format(tid))

        def __process(self, tid, vod_event):
            self.__logger.info('{} process {}'.format(tid, vod_event))
            vod_id = int(vod_event.id())
            if vod_id in self.__movie_id_set:
                # update
                note = str(vod_event.note())
                stat = int(vod_event.state())
                # feedback result stat not sync with note
                if stat == 0 and note.isdigit() and int(note) > 0:
                    stat = int(note)
                    vod_event.vod()['state'] = vod_event.note()
                old_stat = int(self.__tv_stats.get(vod_id, sys.maxsize))
                if stat > 0 and old_stat < stat:
                    self.__logger.info('update tv id {},name {}'.format(vod_id,vod_event.name()))
                    self.__mac_vod_db.update_mac_vod(vod_event)
                else:
                    self.__logger.info('ignore update {} {}'.format(vod_id, vod_event.name()))

            else:
                self.__mac_vod_db.insert_mac_vod(vod_event)
                self.__logger.info('new vod id:{},name:{}'.format(vod_id, vod_event.name()))
            self.__movie_id_set.add(int(vod_id))

        def stop(self):
            # wait vod event consume finish
            while len(self.__queue) > 0:
                 time.sleep(5)
            self.__stop.set()
            self.__logger.info('event queue is empty')
            self.__mac_vod_db.close()

        def process(tid, vod_event):


            print(vod_event)

        def __all_movie_ids(self):
            columns = 'vod_id'
            id_tuples = self.__mac_vod_db.select('mac_vod', None, columns)
            id_set = set()
            for id_t in id_tuples:
                id_set.add(id_t[0])
            return id_set

        def __all_tv_id_stat(self):
            columns = 'vod_id,vod_state'
            condition = 'type_id_1 in(2,3,4)'
            vod_stat = self.__mac_vod_db.select('mac_vod', condition, columns)
            stat_map = {}
            for stat in vod_stat:
                stat_map[stat[0]] = stat[1]
            return stat_map




if __name__ == '__main__':
    tracker = MovieTracker






