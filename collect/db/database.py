import MySQLdb


class Database:
    def __init__(self, dbconfig):
        self.__dbconfig = dbconfig
        self.__db = MySQLdb.connect(self.__dbconfig['host'],
                                    self.__dbconfig['user'],
                                    self.__dbconfig['passwd'],
                                    self.__dbconfig['db'],
                                    charset='utf8')

    def __insert(self, sql):
        print(sql)

    def __update(self, sql):
      print(sql)

    def __delete(self, sql):
      print(sql)

    def __query(self, sql):
      print(sql)


