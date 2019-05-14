import pymysql
from .re_structure import *
from collections import OrderedDict


class Store:
    __tag_file = "<?xml version=\"1.0\" encoding=\"UTF-8\"?>\n"
    __tag_main = "Produkty"
    __content = None
    __content_new = None
    __db_url = "mn26.webd.pl"
    __db_name = "delove2_shopgold_sklep_delove"
    __db_user = "delove2_gold2"
    __db_pass = "Delove123!"

    def __init__(self):
        self.__content = OrderedDict()
        self.__content_new = OrderedDict()

    def __len__(self):
        return len(self.__content)

    def dump_store_to_xml(self, file_path, only_new_products=False):
        info = "Zrzucam plik magazynu - {}."
        content = self.__content
        if only_new_products:
            info = "Zrzucam nowe produkty do pliku - {}."
            content = self.__content_new
        print(info.format(file_path))
        with open(file_path, "w", encoding="UTF-8") as out:
            out.write(self.__tag_file)
            out.write("{}\n".format(ProductUpdate.tag_open.format(self.__tag_main)))
            for entry in content.values():
                out.write("{}\n".format(entry.get_xml()))
            out.write("{}\n".format(ProductUpdate.tag_close.format(self.__tag_main)))

    def get_own_store_dict(self):
        return self.__content

    def get_new_products_dict(self):
        return self.__content

    def download_own_store(self):
        db = None
        try:
            print("Ładuję magazyn z bazy danych delove.")
            db = pymysql.connect(
                self.__db_url,
                self.__db_user,
                self.__db_pass,
                self.__db_name
            )
        except pymysql.err:
            print("Błąd ładowania bazy danych.")
        cursor = db.cursor()
        query = """
SELECT products_stock_model, products_stock_ean, 
products_stock_quantity, products_availability_name, products_shipping_time_name
FROM products_stock, products_availability_description, products_shipping_time_description
WHERE
products_stock.products_stock_availability_id = products_availability_description.products_availability_id AND
products_stock.products_stock_shipping_time_id = products_shipping_time_description.products_shipping_time_id AND
products_shipping_time_description.language_id = 1 AND
products_availability_description.language_id = 1 AND
products_stock_model != '' AND products_stock_ean != ''
;
            """
        cursor.execute(query)
        remote_store = cursor.fetchall()
        db.close()
        self.__content = {product[1]: ProductUpdate() for product in remote_store}
        for product in remote_store:
            ean = product[1]
            self.__content[ean].set_props(product)
        print("Z bazy danych delove wczytano {} produktów.".format(len(self)))

    def void_main_store(self):
        self.__content.clear()
        self.__content_new.clear()
        print("Wymazano główny magazyn z pamięci.")
