import pymysql
import time
import logging


class MacVod:
    def __init__(self,log_config ,mac_type_mapper, dbconfig):
        self.__dbconfig = dbconfig
        self.__log_config = log_config
        self.__db = pymysql.connect(self.__dbconfig['url'],
                                    self.__dbconfig['user'],
                                    self.__dbconfig['passwd'],
                                    self.__dbconfig['db'],
                                    charset='utf8')
        self.__cursor = self.__db.cursor()
        self.__mac_type_mapper = mac_type_mapper
        self.__mac_type_pid_mapper = self.__mac_type_pid_mapper()
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

    def insert_mac_vod(self, vod):

        insert_sql = """INSERT INTO mac_vod(vod_id,type_id,type_id_1,vod_name,vod_year,
                                          vod_pic,vod_actor,vod_director,vod_remarks,vod_state,
                                          vod_lang,vod_class,vod_area,vod_play_from,vod_content,vod_play_server,
                                          vod_play_url,vod_down_url,vod_time,vod_time_add,
                                          vod_status) values({})""".format(
                                          self.__format_values(vod))

        try:
            self.__cursor.execute(insert_sql)
            self.__db.commit()
        except:
            self.__db.rollback()

    def update_mac_vod(self, vod):
        filed_values = """
                        vod_remarks='{marks}',vod_state='{state}',vod_play_url='{play_url}'
                       """.format(marks=vod.note(),
                                  state=vod.state(),
                                  play_url=vod.content())
        condition = 'vod_id ={}'.format(vod.id())
        self.update('mac_vod', filed_values, condition)

    def __format_values(self, vod):
        type_id = self.__mac_type_mapper.get(int(vod.tid()), -1)
        vod_status = 1
        if type_id < 0:
            self.__logger.info('not found type id:{},{}'.format(vod.id(),
                                                                vod.type()))
            vod_status = -1
        values = """{vod_id},{type_id},{type_id_1},'{vod_name}',{vod_year},'{vod_pic}','{vod_actor}',\
          '{vod_director}','{vod_remarks}',{vod_state},'{vod_language}','{vod_class}','{vod_area}','{vod_play_from}',\
          '{vod_content}','{vod_play_server}','{vod_play_url}',' ',{vod_time},{vod_time_add},{vod_status}
        """.format(vod_id=vod.id(),
                   type_id=type_id,
                   type_id_1=self.__mac_type_pid_mapper[type_id],
                   vod_name=vod.name(),
                   vod_year=vod.year(),
                   vod_pic=vod.pic(),
                   vod_actor=vod.actor(),
                   vod_director=vod.director(),
                   vod_remarks=vod.note(),
                   vod_state=vod.state(),
                   vod_language=str(vod.lang()),
                   vod_class=vod.type(),
                   vod_area=vod.area(),
                   vod_play_from=vod.content_flag(),
                   vod_content=vod.des(),
                   vod_play_server='no',
                   vod_play_url=vod.content(),
                   vod_time=self.__date_timestamp(vod.last_update()),
                   vod_time_add=int(time.time()),
                   vod_status=vod_status)
        return values

    def __date_timestamp(self, d):
        timestamp = time.strptime(d, '%Y-%m-%d %H:%M:%S')
        return time.mktime(timestamp)

    def update(self, table, field_values, condition):
        update_sql = """
              update  {} set {}
               """.format(table, field_values)
        if condition is not None:
            update_sql += "where {}".format(condition)
        self.__cursor.execute(update_sql)

    def delete(self, sql):
        self.__cursor.execute(sql)

    def select(self, table, condition, columns):
        select_sql = """
              select {}
              from {} """.format(columns, table)
        if condition is not None:
            select_sql += "where {}".format(condition)
        self.__cursor.execute(select_sql)
        return self.__cursor.fetchall()

    def __mac_type_pid_mapper(self):
        columns = "type_id,type_pid"
        records = self.select('mac_type', None, columns)
        map = {}
        for r in records:
            map[r[0]] = r[1]
        return map

    def select_mac_columns(self):
        columns = """vod_id,type_id,type_id_1,vod_name,vod_year,vod_pic,vod_actor,
                   vod_director,vod_state,vod_language,vod_class,vod_area,vod_play_from,
                   vod_content,vod_play_note,vod_time,vod_time_add,vod_status"""
        return columns

    def close(self):
        self.__db.close()


