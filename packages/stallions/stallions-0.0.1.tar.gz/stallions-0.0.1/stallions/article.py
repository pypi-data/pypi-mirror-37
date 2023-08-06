class Article(object):
    def __init__(self):
        self.url_domain = ""
        self.meta_description = ""
        self.meta_keywords = ""
        self.title = ""
        self.h1 = ""
        self.content = ""
        self.raw_html = ""
        self.url_list = []

        # the lxml Document object
        self.doc = None

    @property
    def infos(self):
        data = {
            "meta_description": self.meta_description,
            "meta_keywords": self.meta_keywords,
            "title": self.title,
            "h1": self.h1,
            "content": self.content,
            "url_list": self.url_list
        }
        return data
