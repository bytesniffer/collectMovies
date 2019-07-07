

class Page:
    def __init__(self, page):
        self.__page = page

    def size(self):
        return self.__page['pagesize']

    def page(self):
        return self.__page['page']

    def total_page(self):
        return self.__page['pagecount']

    def total_record(self):
        return self.__page['recordcount']

    def content(self):
        return self.__page['video']