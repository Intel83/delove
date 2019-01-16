class Supplier:
    FILETYPE = "xml"
    _CONVERSION_MAP = tuple()
    _PREFIX_CODE = ""

    def __init__(self):
        self._store = {}

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
        return self._PREFIX_CODE
