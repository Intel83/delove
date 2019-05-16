import re
from .supplier import Supplier
from .boss_of_toys_excl import boss_of_toys_exclusions as exclusions
from store_own.product_new import NewProduct
from store_own.product_update import ProductUpdate


class Boss(Supplier):
    __rgx_field = re.compile(r"<(?P<name>[\w_]+)>(?P<value>.*?)</\1>", re.DOTALL)
    __code_prefixes = {
        "Obsessive": "49-",
        "Orion": "42-",
    }
    _file_url = "http://bossoftoys.pl/images/products/xml/5658fd03-869d-4fd8-bb5d-db680a7071ac.xml"
    _rgx_product = re.compile("<Record>(.*?)</Record>", re.DOTALL)
    _conversion_map = (
        "kod",
        "ean",
        "availability",
        "delivery_week",
        "nazwa",
        "package_weight",
        "cena_netto",
        "description",
        "detailed_text",
        "ean",
        "supplier",
        "stan_boss",
        "stawka_vat"
    )
    supplier_name = "boss_of_toys"

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
                    new_product["supplier"] = "Nowy"
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
                quantity = int(float(prod_fields[self._conversion_map[11]]))
                if prod_fields[self._conversion_map[10]] == "Orion":
                    avail = own_store_dict[prod_ean].get_avail()
                    date = "24h" if quantity > 0 else own_store_dict[prod_ean].get_date()
                    quantity += own_store_dict[prod_ean].get_quant()
                else:
                    if quantity > 0:
                        avail = "Dostępny"
                        date = "24h"
                    else:
                        avail = "Niedostępny"
                        date = "BRAK"
                sku = own_store_dict[prod_ean].get_sku()
                own_store_dict[prod_ean] = ProductUpdate()
                own_store_dict[prod_ean].set_props((sku, prod_ean, quantity, avail, date))
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
                if self.__code_prefixes["Obsessive"] in prod_fields[self._conversion_map[0]]:
                    try:
                        code_suffix = prod_fields[self._conversion_map[0]].split("-")[1]
                    except IndexError:
                        code_suffix = prod_fields[self._conversion_map[0]]
                else:
                    code_suffix = prod_fields[self._conversion_map[0]]
                new_products_dict[prod_ean].set_props((
                    int(float(prod_fields[self._conversion_map[11]])),
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
