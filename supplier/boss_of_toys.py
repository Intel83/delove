import re
from .supplier import Supplier


class Boss(Supplier):
    __RGX_PRODUCT = re.compile("<Record>(.*?)</Record>", re.DOTALL)
    __RGX_FIELD = re.compile(r"<(?P<name>[\w_]+)>(?P<value>.*?)</\1>", re.DOTALL)
    _supplier_name = "boss_of_toys"
    _file_url = "http://bossoftoys.pl/images/products/xml/5658fd03-869d-4fd8-bb5d-db680a7071ac.xml"
    prefix_code = ""

    def __init__(self):
        Supplier.__init__(self)

    def load(self, input_file):
        data = None
        try:
            with open(input_file, "r") as handle:
                data = handle.read()
        except IOError as e:
            print("I/O error({0}): {1}".format(e.errno, e.strerror))
        with open(self._errors_file.format(self._supplier_name), "w", encoding="UTF-8") as err_out:
            for product in self.__RGX_PRODUCT.findall(data):
                new_product = {}
                for field in self.__RGX_FIELD.findall(product):
                    field_name = field[0]
                    field_value = field[1]
                    if "gallery" not in field_value:
                        new_product[field_name] = field[1]
                ean = new_product["ean"]
                if ean not in self._store.keys():
                    self._store[ean] = new_product
                else:
                    err_out.write("EAN: {} zdublowany.\n".format(ean))
