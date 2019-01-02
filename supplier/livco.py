import re
from .supplier import Supplier


class Livco(Supplier):
    __RGX_PRODUCT = re.compile("<produkt>(.*?)</produkt>", re.DOTALL)
    __RGX_VARIANT = re.compile("<wariant>(.*?)</wariant>", re.DOTALL)
    __RGX_PRODUCT_ID = re.compile(r"<id>(\d+?)</id>")
    __RGX_MAIN_FIELD = re.compile(r"<(.+?)><!\[CDATA\[(.*?)]]></\1>")
    __RGX_VARIANT_FIELD = re.compile(r"<(.+?)>(.*?)</\1>")

    __FIELD_EXCLUSIONS = [
        "zdjecie",
        "zdjecia",
        "warianty"
    ]

    def __init__(self):
        Supplier.__init__(self)
        self.__counter = 0

    def load(self, input_file):
        data = None
        try:
            with open(input_file, 'r') as stream:
                data = stream.read()
        except IOError as e:
            print("I/O error({0}): {1}".format(e.errno, e.strerror))
        for product in self.__RGX_PRODUCT.findall(data):
            new_product = dict()
            new_product["id"] = self.__RGX_PRODUCT_ID.search(product).group(1)
            for main_field in self.__RGX_MAIN_FIELD.findall(product):
                name = main_field[0]
                if any([exclusion for exclusion in self.__FIELD_EXCLUSIONS if exclusion in name]):
                    continue
                value = main_field[1]
                new_product[name] = value
            new_product["warianty"] = {}
            for variant in self.__RGX_VARIANT.findall(product):
                new_variant = {}
                for variant_field in self.__RGX_VARIANT_FIELD.findall(variant):
                    new_variant[variant_field[0]] = variant_field[1]
                new_product["warianty"][new_variant["id"]] = new_variant
                self.__counter += 1
            self._store[new_product["id"]] = new_product

    def test_store(self):
        print("Wykryto {} produktow w {} wariantach".format(len(self._store), self.__counter))
