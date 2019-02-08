import re
import urllib.request
from time import strftime, localtime
from collections import OrderedDict
from store_own.product_update import ProductUpdate


class Supplier:
    _rgx_product = re.compile("")
    _conversion_map = tuple()
    _errors_file = "bledy_ladowania_produktow_{}.txt"
    _file_url = ""
    _products = []
    filetype = "xml"
    supplier_name = ""
    prefix_code = ""

    def __init__(self):
        self._store = OrderedDict()

    def __len__(self):
        return len(self._store)

    def _read_supplier_file_into_products(self, input_file):
        raw_data = ""
        try:
            with open(
                    input_file,
                    "r",
                    encoding="UTF-8"
            ) as handle:
                raw_data = handle.read()
        except IOError as e:
            print("I/O error({0}): {1}".format(e.errno, e.strerror))
        assert self._products is not None
        self._products = self._rgx_product.findall(raw_data)

    def void_store(self):
        self._store.clear()
        print("Magazyn dostawcy został wyzerowany.")

    def load(self, input_file):
        pass

    def get_store(self):
        return self._store

    def test_store(self):
        counter = 0
        try:
            for ean, fields in self._store.items():
                counter += 1
                if ean == "" or any([field for field in fields if field == ""]):
                    print("Zły wpis dla EAN/barcode: {}.".format(ean))
            return True
        except KeyError:
            print("Zły wpis {}.".format(counter))
            return False
        finally:
            print("Sprawdzono {} wpisow. Nie ma pustych pól.".format(counter))

    def download_store_xml(self):
        timestamp = strftime("%Y_%m_%d_%H_%M_%S", localtime())
        file = "{}_{}.xml".format(self.supplier_name, timestamp)
        print("Rozpoczynam pobieranie magazynu. To potrwa około minuty.")
        urllib.request.urlretrieve(self._file_url, file)
        print("Pobieranie zakończone do pliku: {}".format(file))

    def get_conv_map(self):
        return self._conversion_map

    def get_prefix(self):
        return self.prefix_code

    def is_supplying(self, product):
        assert product is not ProductUpdate()
        return product.get_props()[product.props[0]][:2] == self.prefix_code

