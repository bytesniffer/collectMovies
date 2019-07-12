
class Vod:
    def __init__(self, vod):
        self.__vod = vod

    def vod(self):
        return self.__vod

    def actor(self):
        return self.__vod['actor']

    def area(self):
        return self.__vod['area']

    def director(self):
        return self.__vod['director']

    def content(self):
        return self.__vod['dl']['dd']['content']

    def content_flag(self):
        return self.__vod['dl']['dd']['flag']

    def id(self):
        return self.__vod['id']

    def lang(self):
        return self.__vod['lang']

    def last_update(self):
        return self.__vod['last']

    def des(self):
        return self.__vod['des']

    def name(self):
        return self.__vod['name']

    def note(self):
        return self.__vod['note']

    def pic(self):
        return self.__vod['pic']

    def state(self):
        return self.__vod['state']

    def tid(self):
        return self.__vod['tid']

    def type(self):
        return self.__vod['type']

    def year(self):
        return self.__vod['year']