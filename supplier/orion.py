import re
from datetime import datetime
from .supplier import Supplier
from .orion_excl import orion_exclusions as exclusions
from store_own.product_new import NewProduct
from store_own.product_update import ProductUpdate


class Orion(Supplier):
    __eur_to_pln_rate = 4.4
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
    __token = "download_token=180315-l3qhn5ggmpdtw8y8zijv88o45"
    _file_url = "https://www.orion-wholesale.com/assets/restricted/downloads/productdata_v4_02_01.xml?{}".format(
        __token
    )
    # _file_url = "https://www.orion-grosshandel.de/assets/restricted/downloads/productdata_v4_03_02.xml\\?{}".format(
    #     __token
    # )
    _rgx_product = re.compile("<product (.*?)</product>", re.DOTALL)
    _conversion_map = (
        "product-id",
        "availability",
        "delivery_week",
        "name",
        "weight",
        "list-price",
        "full_text",
        "detailed_text",
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

    def update_own_store(self, own_store_dict, new_products_dict):
        supplier_products_in_own_store = len(
            {product for product in own_store_dict.values() if self.is_supplying(product)}
        )
        for product in own_store_dict.values():
            if self.is_supplying(product):
                ean = product.get_ean()
                if ean not in self._store:
                    print(
                        "EAN: {} nie znajduje się w magazynie dostawcy. Zmieniam wpis we własnym magazynie."
                        .format(ean)
                    )
                    product.void_product()

        for prod_ean, prod_fields in self._store.items():
            if prod_ean in own_store_dict:
                print(
                    "EAN: {} znajduje się w bazie delove. Zastępuję wpis w bazie wpisem z pliku dostawcy.".format(
                        prod_ean
                    )
                )
                own_store_dict[prod_ean] = ProductUpdate()
                sku = "{}-{}".format(self.get_prefix(), prod_fields[self._conversion_map[0]])
                is_available = True if prod_fields[self._conversion_map[1]] == "1" else False
                quant = "100" if is_available else "0"
                avail = "Dostępny" if is_available else "Zapytaj o dostępność"
                try:
                    date = "Do 7 dni" if is_available else "od {}".format(
                        str(datetime.strptime(prod_fields[self._conversion_map[2]] + "-1", "%W/%Y-%w"))[:10]
                    )
                except KeyError:
                    date = "Brak informacji"
                    print("EAN: {} dostępność: {}. Brak pola delivery_week. Używam \"{}\".".format(
                        prod_ean,
                        prod_fields[self._conversion_map[1]],
                        date
                    ))
                own_store_dict[prod_ean].set_props((sku, prod_ean, quant, avail, date))
            else:
                print("EAN: {} nie znajduje się w bazie delove. Dodaję do spisu nowych produktów.".format(prod_ean))
                new_products_dict[prod_ean] = NewProduct()
                full_text = detailed_text = ""
                try:
                    full_text = prod_fields[self._conversion_map[6]]
                except KeyError:
                    print("Produkt {} nie ma angielskiego opisu. Zostawiam puste.".format(prod_ean))
                try:
                    detailed_text = prod_fields[self._conversion_map[7]]
                except KeyError:
                    print("Produkt {} nie ma angielskiego opisu skróconego. Zostawiam puste.".format(prod_ean))
                sku = prod_fields[self._conversion_map[0]]
                new_products_dict[prod_ean].set_props((
                    "23",
                    "Orion",
                    prod_fields[self._conversion_map[3]],
                    prod_fields[self._conversion_map[4]],
                    float(prod_fields[self._conversion_map[5]]) * 1.19 * 2 * self.__eur_to_pln_rate,
                    full_text,
                    detailed_text,
                    sku[:7] if sku[0] != "0" else sku[1:7],
                ))

        print("W bazie delove jest {} produktów tego dostawcy.".format(supplier_products_in_own_store))
        print("W magazynie dostawcy znaleziono {} nowych produktów.".format(len(new_products_dict)))
