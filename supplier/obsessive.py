import re
import xlrd
from supplier import Supplier


class Obsessive(Supplier):
    FILETYPE = "xls"
    __CODEPAGE = "utf-8"
    __LP_RGX = re.compile('.*Lp\..*', re.I)

    def __init__(self):
        Supplier.__init__(self)
        self._store = list()

    def load(self, input_file):
        try:
            workbook = xlrd.open_workbook(input_file, encoding_override=self.__CODEPAGE)
        except UnicodeDecodeError:
            print "Unicode decoding error caught"
            # sys.exit(1)
        except:
            print "Nie mozna odczytac XLS"
        sheet = workbook.sheet_by_index(0)
        data_pending = False
        key_row_idx = None
        for row_idx in range(0, sheet.nrows - 1):
            if not data_pending and self.__LP_RGX.match(str(sheet.cell(row_idx, 0))):
                key_row_idx = row_idx
                data_pending = True
                continue
            if data_pending:
                self._store.append({
                    sheet.cell(key_row_idx, col_idx): sheet.cell(row_idx, col_idx)
                    for col_idx in range(0, sheet.ncols)
                })
