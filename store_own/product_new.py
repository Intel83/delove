from .product_update import ProductUpdate


class NewProduct(ProductUpdate):
    __content_pattern = """<Produkt>
    <Kategoria><![CDATA[Nowe]]></Kategoria>
    <Ilosc_produktow>0</Ilosc_produktow>
    <Kod_ean><![CDATA[brak]]></Kod_ean>
    <Podatek_Vat>{}</Podatek_Vat>
    <Nowosc>tak</Nowosc>
    <Do_porownywarek>tak</Do_porownywarek>
    <Negocjacja>tak</Negocjacja>
    <Kontrola_magazynu>tak</Kontrola_magazynu>
    <Status>nie</Status>
    <Jednostka_miary><![CDATA[szt.]]></Jednostka_miary>
    <Termin_wysylki><![CDATA[do 7 dni]]></Termin_wysylki>
    <Stan_produktu><![CDATA[Nowy]]></Stan_produktu>
    <Dostepnosc><![CDATA[AUTOMATYCZNY]]></Dostepnosc>
    <Producent><![CDATA[{}]]></Producent>
    <Gabaryt>nie</Gabaryt>
    <Nazwa_produktu><![CDATA[{}]]></Nazwa_produktu>
    <Waga>{:.2f}</Waga>
    <Cena_brutto>{:.2f}</Cena_brutto>
    <Opis><![CDATA[{}]]></Opis>
    <Opis_krotki><![CDATA[{}]]></Opis_krotki>
    <Nr_katalogowy>{}</Nr_katalogowy>
</Produkt>"""

    def __init__(self):
        super(NewProduct, self).__init__()
        self.props = (
            "Podatek_Vat",
            "Producent",
            "Nazwa_produktu",
            "Waga",
            "Cena_brutto",
            "Opis",
            "Opis_krotki",
            "Nr_katalogowy",
        )

    def _build_xml(self):
        content = self.__content_pattern.format(
            self._properties[self.props[0]],
            self._properties[self.props[1]],
            self._properties[self.props[2]],
            self._properties[self.props[3]],
            self._properties[self.props[4]],
            self._properties[self.props[5]],
            self._properties[self.props[6]],
            self._properties[self.props[7]],
        )
        self._xml_form = content

    def set_props(self, product_tuple):
        self._properties[self.props[0]] = product_tuple[0]
        self._properties[self.props[1]] = product_tuple[1]
        self._properties[self.props[2]] = product_tuple[2]
        self._properties[self.props[3]] = float(product_tuple[3]) / 1000
        self._properties[self.props[4]] = product_tuple[4]
        self._properties[self.props[5]] = product_tuple[5]
        self._properties[self.props[6]] = product_tuple[6]
        self._properties[self.props[7]] = product_tuple[7]
        self._build_xml()

    def void_product(self):
        pass
