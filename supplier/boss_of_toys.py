import re
from .supplier import Supplier


class Boss(Supplier):
    __RGX_PRODUCT = re.compile("<Record>(.*?)</Record>", re.DOTALL)
    __RGX_FIELD = re.compile(r"<(?P<name>[\w_]+)>(?P<value>.*?)</\1>", re.DOTALL)

    def __init__(self):
        Supplier.__init__(self)

    def load(self, input_file):
        data = None
        try:
            with open(input_file, "r") as handle:
                data = handle.read()
        except IOError as e:
            print("I/O error({0}): {1}".format(e.errno, e.strerror))
        for product in self.__RGX_PRODUCT.findall(data):
            new_product = {}
            for field in self.__RGX_FIELD.findall(product):
                field_name = field[0]
                field_value = field[1]
                if "gallery" not in field_value:
                    new_product[field_name] = field[1]
            code = new_product["kod"]
            ean = new_product["ean"]
            if (code, ean) not in self._store.keys():
                self._store[(code, ean)] = new_product
            else:
                print("Zdublowany kod: {}".format((code, ean)))
