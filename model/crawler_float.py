import re
from bs4 import BeautifulSoup
import requests
from model.crawler import Crawler


class CrawlerFloat(Crawler):

    def __init__(self, indizid):
        super().__init__(indizid)
        self._rule = r"\d*(,|\.)\d{3}(\.|,)\d*"

    def extract_data(self):

        float_number = None
        float_numbers = []
        item_dict = self._download_data()

        if isinstance(item_dict, str):
            return item_dict

        contents = self._wrap_data(item_dict['source'], item_dict['selector'])

        for tag in contents:
            string_content = str(tag)

            if re.search(self._rule, string_content):
                match = re.search(self._rule, string_content)
                index_tuple = match.span()
                preresult = string_content[index_tuple[0]:index_tuple[1]]
                float_number = float(preresult.replace(".", "_").replace(",", "."))
                float_numbers.append(float_number)

        return float_number

    def _download_data(self, parser_type="html.parser"):

        """Return page source content from module requests or en errorstring."""

        error_string = ""
        items = self._urlmodel.get_url_active_items()

        for item in items:

            try:
                page_source = requests.get(item[0])
            except requests.exceptions.RequestException as request_error:
                error_string += str(request_error)
                continue
            else:
                if not 200 <= page_source.status_code < 299:
                    error_string += str(page_source.status_code)
                    continue

                content = page_source.content
                return {"source": content, "selector": item[1]}

        return error_string

    def _wrap_data(self, source, selector):

        soup = BeautifulSoup(source, "html.parser")
        peace = soup.select(selector)

        return peace

    """def __validate_with_time(self, source_items):

        cleaned_items = []
        actual_timestamp = int(datetime.now().timestamp())

        for item in source_items:
            beginning_today_timestamp = int(datetime.strptime(datetime.now().strftime("%Y-%m-%d ") + str(item[2]),
                                                              "%Y-%m-%d %H:%M:%S").timestamp())
            ending_today_timestamp = int(datetime.strptime(datetime.now().strftime("%Y-%m-%d ") + str(item[3]),
                                                           "%Y-%m-%d %H:%M:%S").timestamp())

            if beginning_today_timestamp < actual_timestamp < ending_today_timestamp:
                cleaned_items.append(item)

        if len(cleaned_items) == 0:
            raise TimeoutError('Out of Time')

        return cleaned_items
"""