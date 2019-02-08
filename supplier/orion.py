import re
from .supplier import Supplier
from .orion_excl import orion_exclusions as exclusions


class Orion(Supplier):
    __rgx = {
        "product-id": re.compile(r"product-id=\"(\d+)\""),
        "product-group-id": re.compile(r"product-group-id=\"(\d+)\""),
        "barcode": re.compile(
            r"<attribute name..barcode..attribute-type..string...value.default..1..(.+)</value...attribute."
        ),
        "name": re.compile(r"<name><!\[CDATA\[(.+?)\]\]></name>"),
        "selling-price": re.compile("<selling-price>(.+?)</selling-price>"),
        "dicount-prohibited": re.compile(r"<dicount-prohibited>(\d)</dicount-prohibited>"),
        "list-price": re.compile("<list-price>(.+?)</list-price>"),
        "ean-code": re.compile(r"<ean-code>(\d+)</ean-code>"),
        "availability": re.compile(r"<availability>(\d)</availability>"),
        "valid-from-date": re.compile(r"<valid-from-date>(\d+)</valid-from-date>"),
        "delivery_week": re.compile(
            r"<attribute name..delivery_week..attribute-type..string...value.default..1..(.+)</value...attribute."
        ),
        "weight": re.compile(
            r"<attribute name..weight..attribute-type..integer...value.default..1..(.+)</value...attribute."
        ),
        "full_text": re.compile(
            r"<attribute name..full_text..attribute-type..text.+?EN.><!\[CDATA\[(.+?)\]\]>", re.DOTALL
        ),
        "detailed_text": re.compile(
            r"<attribute name..detailed_text..attribute-type..text.+?EN.><!\[CDATA\[(.+?)\]\]>", re.DOTALL
        )
    }
    __rgx_attr = re.compile("<attribute name=\"(.+?)\" (.+?)</attribute>", re.DOTALL)
    __rgx_value = re.compile("<value </value>")
    _file_url = "https://www.orion-wholesale.com/assets/restricted/downloads/productdata_v4_02_01.xml?" \
                "download_token=180315-l3qhn5ggmpdtw8y8zijv88o45"
    _rgx_product = re.compile("<product (.*?)</product>", re.DOTALL)
    _conversion_map = (
        "product-id",
        "ean-code",
        "availability",
        "delivery_week",
        "name",
        "weight",
        "list-price",
        "full_text",
        "detailed_text",
        "barcode"
    )
    supplier_name = "orion"
    prefix_code = "10"

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
                for field, value in self.__rgx.items():
                    try:
                        new_product[field] = value.search(product).group(1)
                    except AttributeError:
                        err_out.write(
                            "EAN (barcode): {} nie ma pola: {}.\n".format(new_product["barcode"], field)
                        )
                barcode = new_product["barcode"]
                if barcode in exclusions:
                    print("EAN (barcode): {} został wykluczony.".format(barcode))
                    exclusions_applied += 1
                    continue
                if barcode not in self._store.keys():
                    self._store[barcode] = new_product
                else:
                    err_out.write("EAN (barcode): {} zdublowany.\n".format(barcode))
        print("Z pliku dostawcy wczytano {} produktów.".format(len(self._store)))
        print("Z pliku dostawcy wykluczono {} produktów.".format(exclusions_applied))
