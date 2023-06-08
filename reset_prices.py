from stockmodels import Datamanager
from datetime import datetime


create_table_string = """CREATE TABLE indiz_price{0} (
    id int(255) PRIMARY KEY NOT NULL AUTO_INCREMENT,
    indiz_id int(11) NOT NULL,
    price double(10,3) NOT NULL,
    zeit datetime NOT NULL,
    FOREIGN KEY(indiz_id)
    REFERENCES indiz(id)
    );"""

dm = Datamanager()
prev_year = datetime.now().year-1
indiz_price_prev = dm.select(f"select indiz_id, price, zeit from indiz_price where year(zeit)={prev_year}")
affected = 0

if len(indiz_price_prev) > 0:

    affected += dm.query(create_table_string.format("_" + str(prev_year)))
    affected += dm.query(f"insert into indiz_price_{prev_year} (indiz_id, price, zeit) values (%s, %s, %s);", indiz_price_prev)

    affected += dm.query(f"delete from indiz_price where year(zeit)={prev_year}")
    indiz_price = dm.select("select indiz_id, price, zeit from indiz_price")
    affected += dm.query("truncate indiz_price")
    affected += dm.query("insert into indiz_price (indiz_id, price, zeit) values (%s, %s, %s);", indiz_price)

print(f"Affected Rows by Transporting and resetting prices: {affected}\nPresent Time: {datetime.now()}")
