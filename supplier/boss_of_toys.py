import re
from .supplier import Supplier
from .boss_of_toys_excl import boss_of_toys_exclusions as exclusions


class Boss(Supplier):
    __rgx_field = re.compile(r"<(?P<name>[\w_]+)>(?P<value>.*?)</\1>", re.DOTALL)
    __orion_prefices = {
        "40",
        "42",
        "48"
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
        "ean"   # valid
    )
    supplier_name = "boss_of_toys"
    prefix_code = "42"

    def __init__(self):
        Supplier.__init__(self)

    def load(self, input_file):
        with open(self._errors_file.format(self.supplier_name), "w", encoding="UTF-8") as err_out:
            try:
                self._read_supplier_file_into_products(input_file)
            except AssertionError:
                err_out.write("Błąd ładownia pliku dostawcy")
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
                    err_out.write("Produkt nie ma pola \"ean\": {}\n".format(str(code)))
                    ean = ""
                complex_key = (code, ean)
                if ean in exclusions:
                    print("EAN: {} został wykluczony.".format(ean))
                    exclusions_applied += 1
                    continue
                if complex_key not in self._store.keys():
                    self._store[complex_key] = new_product
                else:
                    err_out.write("Klucz: {} zdublowany.\n".format(complex_key))
        print("Z pliku dostawcy wczytano {} produktów.".format(len(self._store)))
        print("Z pliku dostawcy wykluczono {} produktów.".format(exclusions_applied))
