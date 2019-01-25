import pymysql
from .re_structure import *
# from supplier.orion import Orion
from collections import OrderedDict
from datetime import datetime


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

    def __setitem__(self, key, value):
        assert value is not Product
        if key in self.__content:
            print("EAN: {} znajduje się w bazie. Zastępuję wpis w bazie wpisem z pliku dostawcy.".format(key))
            self.__content[key] = value
        else:
            if len(self):
                print("EAN: {} nie znajduje się w bazie. Dodaję do bazy nowych produktów".format(key))
            if key in self.__content_new:
                print("Wpis znajduje się już wśród nowych produktów. Zastępuję wpis świeższym.")
            self.__content_new[key] = value

    def __getitem__(self, item):
        return self.__content[item]

    def dump_store_to_xml(self, file_path, only_new_products=False):
        info = "Zrzucam plik magazynu - {}"
        content = self.__content
        if only_new_products:
            info = "Zrzucam nowe produkty do pliku - {}"
            content = self.__content_new
        print(info.format(file_path))
        with open(file_path, "w", encoding="UTF-8") as out:
            out.write(self.__tag_file)
            out.write("{}\n".format(Product.tag_open.format(self.__tag_main)))
            for entry in content.values():
                out.write("{}\n".format(entry.get_xml()))
            out.write("{}\n".format(Product.tag_close.format(self.__tag_main)))

    def load_supplier(self, supplier_store):
        if len(self):
            print("Własny magazyn nie jest pusty. Sprawdzam czy nie zawiera błędnych produktów")
            for ean in self.__content:
                if ean not in supplier_store.get_store():
                    print("EAN {} nie znajduje się w magazynie dostawcy. Zmieniam wpis we własnym magazynie.".format(
                        ean
                    ))
                    self.__content[ean].void_product()

        c_map = supplier_store.get_conv_map()
        entries = 0
        for prod_ean, prod_fields in supplier_store.get_store().items():
            code = "{}-{}".format(supplier_store.get_prefix(), prod_fields[c_map[0]])
            ean = prod_fields[c_map[1]]
            is_available = True if prod_fields[c_map[2]] == "1" else False
            quant = "100" if is_available else "0"
            avail = "Dostępny" if is_available else "Zapytaj o dostępność"
            try:
                date = "Do 7 dni" if is_available else "od {}".format(
                    str(datetime.strptime(prod_fields[c_map[3]] + "-1", "%W/%Y-%w"))[:10]
                )
            except KeyError:
                date = "Brak informacji"
                print("EAN: {}, dostępność: {}. Brak pola delivery_week. Używam \"{}\"".format(
                    ean,
                    prod_fields[c_map[2]],
                    date
                ))
            self[ean] = Product(code, ean, quant, avail, date)
            entries += 1
        print("Zaktualizowano {} produktów do magazynu.".format(entries))
        print("W magazynie znajduje się {} produktów".format(len(self)))
        print("W magazynie znajduje się {} nowych produktów".format(len(self.__content_new)))

    # def load_store_from_file(self, file_path):
    #     with open(file_path, "r", encoding="UTF-8") as source:
    #         entries_total = 0
    #         entries_non_orion = 0
    #         entries_added = 0
    #         entries_no_ean = 0
    #         entries_no_cat_no = 0
    #         entries_faulty = 0
    #         for product in PRODUCT.findall(source.read()):
    #             entries_total += 1
    #             try:
    #                 cat_no = CAT_NO.search(str(product)).group(1).strip()
    #                 if not re.search(r"{}-.+".format(Orion.prefix_code), cat_no):
    #                     entries_non_orion += 1
    #                     continue
    #             except AttributeError:
    #                 entries_no_cat_no += 1
    #                 # print("\nProdukt nie posiada nr katalogowego i jest pominięty {}".format(product))
    #                 continue
    #             try:
    #                 ean = EAN.search(str(product)).group(1).strip()
    #             except AttributeError:
    #                 entries_no_ean += 1
    #                 # print("\nProdukt nie posiada EAN i zostanie pominięty {}".format(product))
    #                 continue
    #             try:
    #                 self.__content[ean] = Product(
    #                     cat_no,
    #                     ean,
    #                     QUANTITY.search(str(product)).group(1),
    #                     AVAIL.search(str(product)).group(1),
    #                     POST_TIME.search(str(product)).group(1)
    #                 )
    #                 entries_added += 1
    #             except AttributeError:
    #                 # print("EAN: {} - błąd ładowania produktu. Sprawdź, czy posiada wymagane pola.".format(ean))
    #                 entries_faulty += 1
    #     print("Produktów pominiętych w ogóle - bez nr katalogowego: {}".format(entries_no_cat_no))
    #     print("Produktów pominiętych w ogóle - nie Orion: {}".format(entries_non_orion))
    #     print("Produktów pominiętych w ogóle - bez nr EAN: {}".format(entries_no_ean))
    #     print("Wpisów pominiętych w ogóle którym było czegoś brak: {}".format(entries_faulty))
    #     print("Do pamięci załadowano {} z {} produktów".format(entries_added, entries_total))

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
        except pymysql.err:
            print("Błąd ładowania bazy danych.")
        self.__content = {product[1]:
                          Product(product[0], product[1], int(product[2]), product[3], product[4])
                          for product in cursor.fetchall() if product[1]}
        print(
            "Pomijam produkty nie posiadające EAN lub nr katalogowego cechy\nZaładowano {} produktów.".format(len(self))
        )
        db.close()

    def void_main_store(self):
        self.__content.clear()
        self.__content_new.clear()
        print("Wyzerowano główny magazyn.")
