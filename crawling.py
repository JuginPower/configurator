from stockmodels import Indiz, CrawlerFloat, Price


indiz_object = Indiz()
ids = indiz_object.get_ids()

for id in ids:

    crawler = CrawlerFloat(id)
    float_number = crawler.extract_data()

    if isinstance(float_number, str):
        print(float_number)
    else:
        price_object = Price(id)
        rows_affected = price_object + float_number
