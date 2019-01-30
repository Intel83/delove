import re
import urllib.request
from time import strftime, localtime
from .supplier import Supplier


class Orion(Supplier):
    __rgx_product = re.compile("<product (.*?)</product>", re.DOTALL)
    __rgx = {
        "product-id": re.compile(r"product-id=\"(\d+)\""),
        "product-group-id": re.compile(r"product-group-id=\"(\d+)\""),
        "name": re.compile(r"<name><!\[CDATA\[(.+?)\]\]></name>"),
        "selling-price": re.compile("<selling-price>(.+?)</selling-price>"),
        "dicount-prohibited": re.compile(r"<dicount-prohibited>(\d)</dicount-prohibited>"),
        "list-price": re.compile("<list-price>(.+?)</list-price>"),
        "ean-code": re.compile(r"<ean-code>(\d+)</ean-code>"),
        "availability": re.compile(r"<availability>(\d)</availability>"),
        "valid-from-date": re.compile(r"<valid-from-date>(\d+)</valid-from-date>"),
        "delivery_week": re.compile(
            r"<attribute name..delivery_week..attribute-type..string...value.default..1..(.+)</value...attribute."
        ),
        "weight": re.compile(
            r"<attribute name..weight..attribute-type..integer...value.default..1..(.+)</value...attribute."
        ),
        "full_text": re.compile(
            r"<attribute name..full_text..attribute-type..text.+?EN<!\[CDATA\[(.+?)\]\]>", re.DOTALL
        ),
        "detailed_text": re.compile(
            r"<attribute name..detailed_text..attribute-type..text.+?EN<!\[CDATA\[(.+?)\]\]>", re.DOTALL
        ),
    }
    __rgx_attr = re.compile("<attribute name=\"(.+?)\" (.+?)</attribute>", re.DOTALL)
    __rgx_value = re.compile("<value </value>")
    __file_url = "https://www.orion-wholesale.com/assets/restricted/downloads/productdata_v4_02_01.xml?" \
                 "download_token=180315-l3qhn5ggmpdtw8y8zijv88o45"
    _conversion_map = (
        "product-id",
        "ean-code",
        "availability",
        "delivery_week",
        "name",
        "weight",
        "list-price",
        "full_text",
        "detailed_text"
    )
    prefix_code = "10"

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
        product_entities = self.__rgx_product.findall(data)
        with open("bledy_ladowania_produktow.txt", "w", encoding="UTF-8") as err_out:
            for product in product_entities:
                new_product = {}
                for field, value in self.__rgx.items():
                    try:
                        new_product[field] = value.search(product).group(1)
                    except AttributeError:
                        err_out.write("Produkt {} nie ma pola: {}\n".format(new_product["ean-code"], field))
                ean = new_product["ean-code"]
                if ean not in self._store.keys():
                    self._store[ean] = new_product
                else:
                    err_out.write("EAN zdublowany: {}\n".format(ean))
        print("Z pliku dostawcy wczytano {} produktów.".format(len(self._store)))

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

    def download_store_xml(self):
        timestamp = strftime("%Y_%m_%d_%H_%M_%S", localtime())
        file = "orion_{}.xml".format(timestamp)
        print("Rozpoczynam pobieranie magazynu. To potrwa około minuty.")
        urllib.request.urlretrieve(self.__file_url, file)
        print("Pobieranie zakończone do pliku: {}".format(file))
