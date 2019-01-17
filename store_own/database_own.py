import re
from .product_own import Product
from .re_structure import *
from collections import OrderedDict


class Store:
    __tag_file = "<?xml version=\"1.0\" encoding=\"UTF-8\"?>\n"
    __tag_main = "Produkty"
    __content = None
    __content_new = None

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
            print("EAN: {} nie znajduje się w bazie. Dodaję do bazy nowych produktów".format(key))
            if key in self.__content_new:
                print("Wpis znajduje się już wśród nowych produktów. Zastępuję wpis świeższym.")
            self.__content_new[key] = value

    def __getitem__(self, item):
        return self.__content[item]

    def dump_store_to_xml(self, file_path):
        print("Zrzucam plik magazynu - {}".format(file_path))
        with open(file_path, "w", encoding="UTF-8") as out:
            out.write(self.__tag_file)
            out.write("{}\n".format(Product.tag_open.format(self.__tag_main)))
            for entry in self.__content:
                out.write("{}\n".format(entry.get_xml()))
            out.write("{}\n".format(Product.tag_close.format(self.__tag_main)))
        n_file_path = file_path.replace(".xml", "_nowe.xml")
        print("Zrzucam plik nowości - {}".format(n_file_path))
        with open(n_file_path, "w", encoding="UTF-8") as out:
            out.write(self.__tag_file)
            out.write("{}\n".format(Product.tag_open.format(self.__tag_main)))
            for entry in self.__content_new.values():
                out.write("{}\n".format(entry.get_xml()))
            out.write("{}\n".format(Product.tag_close.format(self.__tag_main)))

    def load_store_from_file(self, file_path):
        if len(self.__content):
            print("Czyszczę magazyn z pamięci")
            self.__content = OrderedDict()
        with open(file_path, "r", encoding="UTF-8") as source:
            entries_total = entries_added = 0
            for product in PRODUCT.findall(source.read()):
                entries_total += 1
                try:
                    ean = EAN.search(str(product)).group(1)
                except AttributeError:
                    print("\nProdukt nie posiada EAN i nie zostanie załadowany {}".format(product))
                try:
                    self.__content[ean] = Product(
                        CAT_NO.search(str(product)).group(1),
                        ean,
                        QUANTITY.search(str(product)).group(1),
                        AVAIL.search(str(product)).group(1),
                        POST_TIME.search(str(product)).group(1)
                    )
                    entries_added += 1
                except AttributeError:
                    print("EAN: {} - błąd ładowania produktu. Sprawdź, czy posiada wymagane pola.".format(ean))
        print("Do pamięci załadowano {} z {} produktów".format(entries_added, entries_total))

    def new_entries_amount(self):
        return len(self.__content_new)
