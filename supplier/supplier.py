import urllib.request
from time import strftime, localtime
from collections import OrderedDict
from store_own.product_update import ProductUpdate


class Supplier:
    _conversion_map = tuple()
    _supplier_name = ""
    _errors_file = "bledy_ladowania_produktow_{}.txt"
    _file_url = ""
    filetype = "xml"
    prefix_code = ""

    def __init__(self):
        self._store = OrderedDict()

    def __len__(self):
        return len(self._store)

    def void_store(self):
        self._store.clear()
        print("Magazyn dostawcy został wyzerowany.")

    def load(self, input_file):
        pass

    def get_store(self):
        return self._store

    def test_store(self):
        print("Wykryto {} wpisów.".format(len(self._store)))
        return True

    def download_store_xml(self):
        timestamp = strftime("%Y_%m_%d_%H_%M_%S", localtime())
        file = "{}_{}.xml".format(self._supplier_name, timestamp)
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

