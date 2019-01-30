from collections import OrderedDict


class ProductUpdate:
    __string_value = "<![CDATA[{}]]>"
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

    def __init__(self):
        self._properties = OrderedDict()
        self._xml_form = ""

    def _build_xml(self):
        content = "\t\t{}\n".format(self.tag_open.format(self.tag_main))
        for prop, value in self._properties.items():
            content += "\t\t\t"
            content += self.tag_open.format(prop)
            content += self.__string_value.format(value) if prop != self.props[2] else "{}.00".format(str(value))
            content += self.tag_close.format(prop)
            content += "\n"
        content += "\t\t{}\n".format(self.tag_close.format(self.tag_main))
        self._xml_form = content

    def set_props(self, product_tuple):
        self._properties[self.props[0]] = product_tuple[0]
        self._properties[self.props[1]] = product_tuple[1]
        self._properties[self.props[2]] = int(product_tuple[2])
        self._properties[self.props[3]] = product_tuple[3]
        self._properties[self.props[4]] = product_tuple[4]
        self._build_xml()

    def get_props(self):
        return self._properties

    def get_ean(self):
        return self._properties[self.props[1]]

    def get_sku(self):
        return self._properties[self.props[0]]

    def get_xml(self):
        return self._xml_form

    def void_product(self):
        self._properties[self.props[2]] = 0
        self._properties[self.props[3]] = "Niedostępny"
        self._properties[self.props[4]] = "BRAK"
        self._build_xml()
