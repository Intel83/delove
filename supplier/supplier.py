class Supplier:
    FILETYPE = "xml"

    def __init__(self):
        self._store = {}

    def load(self, input_file):
        pass

    def get_store(self):
        return self._store

    def test_store(self):
        print("Wykryto {} wpisow".format(len(self._store)))
        return True
