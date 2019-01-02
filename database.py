import csv


class Database:
    def __init__(self, file):
        self.__nrows = 0
        self.__ncols = 0
        self.__store = list()
        with open(file, 'r') as data_file:
            reader = csv.reader(data_file, delimiter=';', quotechar='"')
            data_pending = False
            keys = []
            for row in reader:
                if data_pending:
                    self.__store.append({
                        keys[idx]: row[idx]
                        for idx in range(0, self.__ncols)
                    })
                else:
                    self.__ncols = len(row)
                    keys = row
                    data_pending = True
                self.__nrows = self.__nrows + 1

    def get_store(self):
        return self.__store
