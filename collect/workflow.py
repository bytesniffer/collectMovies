import urllib
import time
import logging
import Queue
from parser.dbzyz.page import Page
from parser.dbzyz.vod import Vod

from xmljson import yahoo
from xml.etree.ElementTree import fromstring
from json import dumps
import json


class Workflow:
    def __init__(self, config):
        self.__config = config
        self.__log_config = config['log']
        self.__apis = config['apis']
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
        self.__workQueue = Queue.Queue(10)

    def run(self, page):
        self.__logger.info('config as following: '+str(self.__config))
        self.__logger.info('start to iterate movie resource')
        self.__loop_resource(page)

    def __page(self, url_template, page=1):
        current_pg_url = url_template.format(pg=page)
        return self.__load_resource(current_pg_url)

    def __load_resource(self, url):
        self.__logger.info('load url:'+url)
        response = urllib.request.urlopen(url, data=None, timeout=100)
        data = response.read().decode()
        if data is not None:
            json_data = self.__xml_to_json(data)
            self.__logger.info(json_data)
            return json_data

    def __xml_to_json(self, xml):
        self.__logger.info(xml)
        repsonse_json_str = dumps(yahoo.data(fromstring(xml)))
        return json.loads(repsonse_json_str)

    def __loop_resource(self, page=1, breakup_time=1):
        api = self.__apis[0]
        total_load =0
        start_sec= time.time()
        while True:
            try:
                page_data = self.__page(api['url'], page)
                rss = page_data['rss']['list']
                self.__logger.info(str(page_data['rss']))
                if rss is not None:
                      page_model = Page(rss)
                      self.__logger.info("""
                                          page {page}
                                          page size {size}
                                          total page {pg_total}
                                          total records {total}
                                          videos:{videos}""".
                                         format(page=page_model.page(),
                                                pg_total=page_model.total_page(),
                                                size=page_model.size(),
                                                total=page_model.total_record(),
                                                videos=self.__vod_format(page_model.content())))
                      total_load += int(page_model.size())
                      if page >= int(page_model.total_page()):
                          self.__logger.info("finish resource scan, total {}!".format(total_load))
                          break
                page += 1
                if page % 50 == 0:
                    self.__logger.info("parsed total {},elapsed {} sec!".format(total_load,time.time()-start_sec))
                    time.sleep(breakup_time)
            except Exception as e:
                page += 1
                self.__logger.error(e)

    def __vod_format(self, vods):
        vods_format =''
        for vod_dict in vods:
            vod = Vod(vod_dict)
            vods_format += """
                 name: {name}
                 id  :　{id}
                 tid : {tid}
                 year: {year}
                 type: {type}
                 director: {director}
                 actor:{actor}
                 lang: {lang}
                 des : {des}
                 pic : {pic}
                 note: {note}
                 stat: {stat}
                 udpate : {update}
                 content:{content}
                 flag： {flag}
                 ------------
                 """.format(
                    name=vod.name(),
                    id=vod.id(),
                    tid=vod.tid(),
                    year=vod.year(),
                    type=vod.type(),
                    director=vod.director(),
                    actor=vod.actor(),
                    lang=vod.lang(),
                    des=vod.des(),
                    pic=vod.pic(),
                    note=vod.note(),
                    stat=vod.state(),
                    update=vod.last_update(),
                    content=vod.content(),
                    flag=vod.content_flag())
        return vods_format