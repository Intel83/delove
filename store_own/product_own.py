"""
< Produkt >
< Nr_katalogowy_cechy > <![CDATA[10 - 26405381021]] > < / Nr_katalogowy_cechy > // klucz główny
< Kod_ean_cechy > <![CDATA[4024144130061]] > < / Kod_ean_cechy >                // klucz główny(Boss)
< Ilosc_produktow > 100.00 < / Ilosc_produktow >
< Dostepnosc > <![CDATA[AUTOMATYCZNY]] > < / Dostepnosc >
< Termin_wysylki > <![CDATA[do 7 dni]] > < / Termin_wysylki >
< / Produkt >
"""
from collections import OrderedDict


class Product:
    tag_main = "Produkt"
    tag_open = "<{}>"
    tag_close = "</{}>"
    __string_value = "<![CDATA[{}]]>"
    props = (
       "Nr_katalogowy_cechy",
       "Kod_ean_cechy",
       "Ilosc_produktow",
       "Dostepnosc",
       "Termin_wysylki",
    )
    __content = OrderedDict({key: "" for key in props})
    __xml_form = ""

    def __init__(self, cat_no, ean, quantity, availability, date):
        self.__content["Nr_katalogowy_cechy"] = cat_no
        self.__content["Kod_ean_cechy"] = ean
        self.__content["Ilosc_produktow"] = quantity
        self.__content["Dostepnosc"] = availability
        self.__content["Termin_wysylki"] = date

    def __build_xml(self):
        content = "\t\t{}\n".format(self.tag_open.format(self.tag_main))
        for prop, value in self.__content.items():
            content += "\t\t\t"
            content += self.tag_open.format(prop)
            content += self.__string_value.format(value) if prop != "Ilosc_produktow" else "{}.00".format(value)
            content += self.tag_close.format(prop)
            content += "\n"
        content += "\t\t{}\n".format(self.tag_close.format(self.tag_main))
        self.__xml_form = content

    def get_xml(self):
        return self.__xml_form
