from collections import OrderedDict
from store_own.product_update import ProductUpdate


class Supplier:
    _conversion_map = tuple()
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
        print("Wykryto {} wpisow".format(len(self._store)))
        return True

    def download_store_xml(self):
        pass

    def get_conv_map(self):
        return self._conversion_map

    def get_prefix(self):
        return self.prefix_code

    def is_supplying(self, product):
        assert product is not ProductUpdate()
        return product.get_props()[product.props[0]][:2] == self.prefix_code

