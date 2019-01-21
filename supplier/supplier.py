from collections import OrderedDict


class Supplier:
    FILETYPE = "xml"
    _CONVERSION_MAP = tuple()
    PREFIX_CODE = ""

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

    def get_conv_map(self):
        return self._CONVERSION_MAP

    def get_prefix(self):
        return self.PREFIX_CODE
