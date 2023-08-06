import re


class OutputFormatter(object):
    @staticmethod
    def clean_content(content):
        """streamline \r\n\ space"""
        # content = re.sub(r'[^\u4e00-\u9fa5]+', ' ', content) # Eliminate Chinese characters
        return re.sub('[\r\n\t ]+', ' ', content).replace('\xa0', '').strip()


class StandardOutputFormatter(OutputFormatter):
    pass


class EliminateScript:
    @staticmethod
    def delete_all_tag(html_raw):
        # <!--done-->  style script
        html_raw = EliminateScript.delete_notes(html_raw)
        html_raw = EliminateScript.delete_tags(html_raw, "style")
        return EliminateScript.delete_tags(html_raw, "script")

    @staticmethod
    def delete_tags(html_raw, tags):
        html_list = html_raw.split("<{0}".format(tags))
        fresh_html = ""
        if html_raw.startswith("<{0}".format(tags)):
            for i, htm in enumerate(html_list):
                if "</{0}>".format(tags) not in htm:
                    continue
                fresh_html += htm.split("</{0}>".format(tags))[-1]
        else:
            for i, htm in enumerate(html_list):
                if i == 0:
                    fresh_html += htm
                    continue
                if "</{0}>".format(tags) not in htm:
                    continue
                fresh_html += htm.split("</{0}>".format(tags))[-1]
        # for htm in html_list:
        #     if "</{0}>".format(tags) not in htm:
        #         fresh_html += htm
        #         continue
        #     fresh_html += htm.split("</{0}>".format(tags))[-1]
        return fresh_html

    @staticmethod
    def delete_notes(html_raw):
        # delete note
        html_list = html_raw.split("<!--")
        fresh_html = ""
        if html_raw.startswith("<!--"):
            for i, htm in enumerate(html_list):
                if "-->" not in htm:
                    continue
                fresh_html += htm.split("-->")[-1]
        else:
            for i, htm in enumerate(html_list):
                if i == 0:
                    fresh_html += htm
                    continue
                if "-->" not in htm:
                    continue
                fresh_html += htm.split("-->")[-1]
        return fresh_html
