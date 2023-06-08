from model.datalayer_mysql_main import Datamanager


class Indiz(Datamanager):

    def __init__(self):
        super().__init__()

    def get_one_name(self, id):
        return self.select(f"SELECT name FROM indiz WHERE id={id}")[0][0]

    def get_one_id(self, name):
        return self.select(f"SELECT id FROM indiz WHERE name='{name}'")[0][0]

    def get_names(self):
        return [row[0] for row in self.select("SELECT name FROM indiz")]

    def get_ids(self):
        return [row[0] for row in self.select("SELECT id FROM indiz")]
