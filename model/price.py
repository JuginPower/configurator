from datetime import datetime
from model.datalayer_mysql_main import Datamanager
from mysql.connector.errors import ProgrammingError


class Price(Datamanager):

    def __init__(self, indiz_id):
        super().__init__()
        self.fk_id = indiz_id

    def __get_previous(self, column):

        all_data = []

        for y in range(datetime.now().year-1, datetime.now().year-100, -1):
            try:
                data = self.select(f"SELECT {column} FROM indiz_price_{str(y)} WHERE indiz_id={self.fk_id}")
            except ProgrammingError:
                break
            else:
                all_data[:0] = data

        return [row[0] for row in all_data]

    def get_dates(self, amount=None):
        column = "zeit"

        if amount:
            return [row[0] for row in self.select(f"SELECT {column} FROM indiz_price WHERE indiz_id={self.fk_id} ORDER BY id DESC limit {amount}")]
        else:
            pre_data = self.__get_previous(column)
            current_data = [row[0] for row in self.select(f"SELECT {column} FROM indiz_price WHERE indiz_id={self.fk_id}")]
            pre_data.extend(current_data)
            return pre_data

    def get_closes(self, amount=None):
        column = "price"

        if amount:
            return [row[0] for row in self.select(f"SELECT {column} FROM indiz_price WHERE indiz_id={self.fk_id} ORDER BY id DESC limit {amount}")]
        else:
            pre_data = self.__get_previous(column)
            current_data = [row[0] for row in
                            self.select(f"SELECT {column} FROM indiz_price WHERE indiz_id={self.fk_id}")]
            pre_data.extend(current_data)
            return pre_data

    def __add__(self, other):
        try:
            orig_float = self.select(f"SELECT price FROM `indiz_price` WHERE indiz_id={self.fk_id} ORDER BY id DESC LIMIT 1;")[0][0]
        except IndexError as indexerr:
            print(str(indexerr))
            rows_affected = self.query(f"INSERT INTO indiz_price (indiz_id, price, zeit) VALUES (%s, %s, %s)",
                                       (self.fk_id, other, datetime.now().strftime("%Y-%m-%d %H:%M:%S")))
            return rows_affected
        
        else:
            if other == orig_float:
                return 0
            else:
                rows_affected = self.query(f"INSERT INTO indiz_price (indiz_id, price, zeit) VALUES (%s, %s, %s)",
                                        (self.fk_id, other, datetime.now().strftime("%Y-%m-%d %H:%M:%S")))
                return rows_affected
