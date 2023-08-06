from lxml import etree


class Parser(object):
    @staticmethod
    def raw_to_document(raw_html):
        return etree.HTML(raw_html)

    @staticmethod
    def xpathSelect(selector, xpath_lan):
        return selector.xpath(xpath_lan)
