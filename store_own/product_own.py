from collections import OrderedDict


class Product:
    __string_value = "<![CDATA[{}]]>"
    __xml_form = ""
    tag_main = "Produkt"
    tag_open = "<{}>"
    tag_close = "</{}>"
    props = (
       "Nr_katalogowy_cechy",
       "Kod_ean_cechy",
       "Ilosc_produktow",
       "Dostepnosc",
       "Termin_wysylki",
    )
    __content = OrderedDict({key: "" for key in props})

    def __init__(self, cat_no, ean, quantity, availability, date):
        self.__content[self.props[0]] = cat_no
        self.__content[self.props[1]] = ean
        self.__content[self.props[2]] = quantity
        self.__content[self.props[3]] = availability
        self.__content[self.props[4]] = date
        self.__build_xml()

    def __build_xml(self):
        content = "\t\t{}\n".format(self.tag_open.format(self.tag_main))
        for prop, value in self.__content.items():
            content += "\t\t\t"
            content += self.tag_open.format(prop)
            content += self.__string_value.format(value) if prop != self.props[2] else "{}.00".format(value)
            content += self.tag_close.format(prop)
            content += "\n"
        content += "\t\t{}\n".format(self.tag_close.format(self.tag_main))
        self.__xml_form = content

    def get_xml(self):
        return self.__xml_form

    def void_product(self):
        self.__content[self.props[2]] = "0"
        self.__content[self.props[3]] = "Niedostępny"
        self.__content[self.props[4]] = "BRAK"
