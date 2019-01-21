from .re_structure import *
from supplier.orion import Orion
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
            if len(self):
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
            for entry in self.__content.values():
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

    def load_supplier(self, supplier_store):
        if len(self):
            print("Własny magazyn nie jest pusty. Sprawdzam czy nie zawiera błędnych produktów")
            for ean in self.__content:
                if ean not in supplier_store.get_store():
                    print("EAN {} nie znajduje się w magazynie dostawcy. Zmieniam wpis we własnym magazynie.")
                    self.__content[ean].void_product()

        c_map = supplier_store.get_conv_map()
        entries = 0
        for prod_ean, prod_fields in supplier_store.get_store().items():
            code = "{}-{}".format(supplier_store.get_prefix(), prod_fields[c_map[0]])
            ean = prod_fields[c_map[1]]
            is_available = True if prod_fields[c_map[2]] == "1" else False
            quant = "100" if is_available else "0"
            avail = "Dostępny" if is_available else "Zapytaj o dostępność"
            date = "Do 7 dni" if is_available else "Brak informacji"
            self[ean] = Product(code, ean, quant, avail, date)
            entries += 1
        print("Zaktualizowano {} produktów do magazynu.".format(entries))
        print("W magazynie znajduje się {} produktów".format(len(self)))
        print("W magazynie znajduje się {} nowych produktów".format(len(self.__content_new)))

    def load_store_from_file(self, file_path):
        with open(file_path, "r", encoding="UTF-8") as source:
            entries_total = 0
            entries_non_orion = 0
            entries_added = 0
            entries_no_ean = 0
            entries_no_cat_no = 0
            entries_faulty = 0
            for product in PRODUCT.findall(source.read()):
                entries_total += 1
                try:
                    cat_no = CAT_NO.search(str(product)).group(1).strip()
                    if not re.search(r"{}-.+".format(Orion.PREFIX_CODE), cat_no):
                        entries_non_orion += 1
                        continue
                except AttributeError:
                    entries_no_cat_no += 1
                    # print("\nProdukt nie posiada nr katalogowego i jest pominięty {}".format(product))
                    continue
                try:
                    ean = EAN.search(str(product)).group(1).strip()
                except AttributeError:
                    entries_no_ean += 1
                    # print("\nProdukt nie posiada EAN i zostanie pominięty {}".format(product))
                    continue
                try:
                    self.__content[ean] = Product(
                        cat_no,
                        ean,
                        QUANTITY.search(str(product)).group(1),
                        AVAIL.search(str(product)).group(1),
                        POST_TIME.search(str(product)).group(1)
                    )
                    entries_added += 1
                except AttributeError:
                    # print("EAN: {} - błąd ładowania produktu. Sprawdź, czy posiada wymagane pola.".format(ean))
                    entries_faulty += 1
        print("Produktów pominiętych w ogóle - bez nr katalogowego: {}".format(entries_no_cat_no))
        print("Produktów pominiętych w ogóle - nie Orion: {}".format(entries_non_orion))
        print("Produktów pominiętych w ogóle - bez nr EAN: {}".format(entries_no_ean))
        print("Wpisów pominiętych w ogóle którym było czegoś brak: {}".format(entries_faulty))
        print("Do pamięci załadowano {} z {} produktów".format(entries_added, entries_total))
