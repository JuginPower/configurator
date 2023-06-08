from model.datalayer_mysql_main import Datamanager


class Url(Datamanager):

    def __init__(self, indiz_id):
        super().__init__()
        self.fk_id = indiz_id
        self._url = [row[0] for row in self.select(f"SELECT url FROM indiz_url WHERE indiz_id={self.fk_id} AND active=1")]

    def get_url(self):
        return self._url

    def get_url_active_items(self):
        return [list(row) for row in self.select(f"SELECT url, selector FROM indiz_url WHERE indiz_id={self.fk_id} AND active=1")]
