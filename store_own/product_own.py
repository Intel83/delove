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
        self.__build_xml()

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

    def void_product(self):
        self.__content["Ilosc_produktow"] = "0"
        self.__content["Dostepnosc"] = "Niedostępny"
        self.__content["Termin_wysylki"] = "BRAK"
