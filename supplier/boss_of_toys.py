import re
from datetime import datetime
from .supplier import Supplier
from .boss_of_toys_excl import boss_of_toys_exclusions as exclusions
from store_own.product_new import NewProduct
from store_own.product_update import ProductUpdate


class Boss(Supplier):
    __rgx_field = re.compile(r"<(?P<name>[\w_]+)>(?P<value>.*?)</\1>", re.DOTALL)
    # __orion_prefices = {
    #     "40",
    #     "42",
    #     "48"
    # }
    __code_prefixes = {
        "Obsessive": "49-",
        "Orion": "42-",
    }
    _file_url = "http://bossoftoys.pl/images/products/xml/5658fd03-869d-4fd8-bb5d-db680a7071ac.xml"
    _rgx_product = re.compile("<Record>(.*?)</Record>", re.DOTALL)
    _conversion_map = (
        "kod",  # valid
        "ean",  # valid
        "availability",
        "delivery_week",
        "nazwa",    # valid
        "package_weight",   # valid
        "cena_netto",   # valid
        "description",  # valid
        "detailed_text",    # valid
        "ean",   # valid
        "supplier"
    )
    supplier_name = "boss_of_toys"
    # prefix_code = "42"

    def __init__(self):
        Supplier.__init__(self)

    def load(self, input_file):
        with open(self._errors_file.format(self.supplier_name), "w", encoding="UTF-8") as err_out:
            try:
                self._read_supplier_file_into_products(input_file)
            except AssertionError:
                err_out.write("Błąd ładownia pliku dostawcy.")
            exclusions_applied = 0
            for product in self._products:
                new_product = {}
                for field in self.__rgx_field.findall(product):
                    field_name = field[0]
                    field_value = field[1]
                    if "gallery" not in field_value:
                        new_product[field_name] = field[1]
                try:
                    code = new_product["kod"]
                    # if not any([code.startswith(prefix) for prefix in self.__code_prefixes.values()]):
                    #     print(
                    #         "Produkt \"code\": {} nie jest z Orion i Obsessive. Pomijam.".format(str(code)))
                    #     continue
                except KeyError:
                    err_out.write("Produkt nie ma pola \"code\": {}\n".format(str(product)))
                    code = ""
                try:
                    ean = new_product["ean"]
                except KeyError:
                    print("Produkt nie ma pola \"ean\": {}. Pomijam.".format(str(code)))
                    continue
                complex_key = (code, ean)
                if ean in exclusions:
                    print("EAN: {} został wykluczony.".format(ean))
                    exclusions_applied += 1
                    continue
                if complex_key not in self._store.keys():
                    # TEST
                    new_product["supplier"] = "default"
                    for supplier, prefix in self.__code_prefixes.items():
                        if prefix in code:
                            new_product["supplier"] = supplier
                            break
                    self._store[complex_key] = new_product
                else:
                    err_out.write("Klucz: {} zdublowany.\n".format(complex_key))
        print("Z pliku dostawcy wczytano {} produktów.".format(len(self._store)))
        print("Z pliku dostawcy wykluczono {} produktów.".format(exclusions_applied))

    def update_own_store(self, own_store_dict, new_products_dict):
        for complex_key, prod_fields in self._store.items():
            prod_ean = complex_key[1]
            if prod_ean in own_store_dict:
                print(
                    "EAN: {} znajduje się w bazie delove. Aktualizuję wpis w bazie wpisem z pliku dostawcy.".format(
                        prod_ean
                    )
                )
                # own_store_dict[prod_ean] = ProductUpdate()
                # sku = "{}-{}".format(self.get_prefix(), prod_fields[self._conversion_map[0]])
                # is_available = True if prod_fields[self._conversion_map[1]] == "1" else False
                # quant = "100" if is_available else "0"
                # avail = "Dostępny" if is_available else "Zapytaj o dostępność"
                # try:
                #     date = "Do 7 dni" if is_available else "od {}".format(
                #         str(datetime.strptime(prod_fields[self._conversion_map[2]] + "-1", "%W/%Y-%w"))[:10]
                #     )
                # except KeyError:
                #     date = "Brak informacji"
                #     print("EAN: {} dostępność: {}. Brak pola delivery_week. Używam \"{}\"".format(
                #         prod_ean,
                #         prod_fields[self._conversion_map[1]],
                #         date
                #     ))
                # own_store_dict[prod_ean].set_props((sku, prod_ean, quant, avail, date))
            else:
                if self.__code_prefixes["Orion"] in prod_fields[self._conversion_map[0]]:
                    print(
                        "EAN: {} nie znajduje się w bazie delove. Pomijam gdyż jest to produkt Orion.".format(prod_ean)
                    )
                    continue
                print("EAN: {} nie znajduje się w bazie delove. Dodaję do spisu nowych produktów.".format(prod_ean))
                new_products_dict[prod_ean] = NewProduct()
                full_text = detailed_text = ""
                try:
                    full_text = prod_fields[self._conversion_map[7]]
                except KeyError:
                    print("Produkt {} nie ma angielskiego opisu. Zostawiam puste.".format(prod_ean))
                try:
                    detailed_text = prod_fields[self._conversion_map[8]]
                except KeyError:
                    print("Produkt {} nie ma angielskiego opisu skróconego. Zostawiam puste.".format(prod_ean))
                try:
                    code_suffix = prod_fields[self._conversion_map[0]].split("-")[1]
                except IndexError:
                    code_suffix = prod_fields[self._conversion_map[0]]
                new_products_dict[prod_ean].set_props((
                    prod_fields[self._conversion_map[10]],
                    prod_fields[self._conversion_map[4]],
                    "500",
                    float(prod_fields[self._conversion_map[6]]) * 1.19 * 2,
                    full_text,
                    detailed_text,
                    "{}{}".format(
                        "OB" if self.__code_prefixes["Obsessive"] in prod_fields[self._conversion_map[0]] else "BO",
                        code_suffix
                    ),
                ))
        print("W magazynie dostawcy znaleziono {} nowych produktów.".format(len(new_products_dict)))
