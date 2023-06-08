from abc import ABC, abstractmethod
from model.urlmanager import Url


class Crawler(ABC):

    def __init__(self, indiz_id):

        self._urlmodel = Url(indiz_id)

    @abstractmethod
    def extract_data(self):
        pass

    @abstractmethod
    def _wrap_data(self, source, selector):
        pass

    @abstractmethod
    def _download_data(self, parser_type="html.parser"):
        pass
