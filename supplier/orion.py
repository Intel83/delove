import re
from .supplier import Supplier


class Orion(Supplier):
    __RGX_PRODUCT = re.compile("<product (.*?)</product>", re.DOTALL)
    __RGX = {
        "product-id": re.compile(r"product-id=\"(\d+)\""),
        "product-group-id": re.compile(r"product-group-id=\"(\d+)\""),
        "name": re.compile(r"<name><!\[CDATA\[(.+?)\]\]></name>"),
        "selling-price": re.compile("<selling-price>(.+?)</selling-price>"),
        "dicount-prohibited": re.compile(r"<dicount-prohibited>(\d)</dicount-prohibited>"),
        "list-price": re.compile("<list-price>(.+?)</list-price>"),
        "ean-code": re.compile(r"<ean-code>(\d+)</ean-code>"),
        "availability": re.compile(r"<availability>(\d)</availability>"),
        "valid-from-date": re.compile(r"<valid-from-date>(\d+)</valid-from-date>")
    }
    __RGX_ATTR = re.compile("<attribute name=\"(.+?)\" (.+?)</attribute>", re.DOTALL)
    __RGX_VALUE = re.compile("<value </value>")
    _PREFIX_CODE = "10"
    _CONVERSION_MAP = (
        "product-id",
        "ean-code",
        "availability"
    )

    def __init__(self):
        Supplier.__init__(self)

    def load(self, input_file):
        data = None
        try:
            with open(
                    input_file,
                    "r",
                    encoding="utf8"
            ) as handle:
                data = handle.read()
        except IOError as e:
            print("I/O error({0}): {1}".format(e.errno, e.strerror))
        assert data is not None
        product_entities = self.__RGX_PRODUCT.findall(data)
        for product in product_entities:
            new_product = {}
            for field, value in self.__RGX.items():
                new_product[field] = value.search(product).group(1)
            ean = new_product["ean-code"]
            if ean not in self._store.keys():
                self._store[ean] = new_product
            else:
                print("EAN zdublowany: {}".format(ean))

    def test_store(self):
        counter = 0
        try:
            for ean, fields in self._store.items():
                counter += 1
                if ean == "" or any([field for field in fields if field == ""]):
                    print("zly wpis dla EAN: {}".format(ean))
            return True
        except KeyError:
            print("zly wpis {}".format(counter))
            return False
        finally:
            print("Sprawdzono {} wpisow".format(counter))
