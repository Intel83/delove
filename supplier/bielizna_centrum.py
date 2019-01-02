import re
from .supplier import Supplier


class BC(Supplier):
    __RGX = {
        'id': re.compile(r'<id>(\d+)</id>'),
        'name': re.compile('<name>(.+)</name>'),
        'category': re.compile('<category>(.+)</category>'),
        'category_path': re.compile('<categoryPath>(.+)</categoryPath>'),
        'brutto': re.compile('<brutto>(.+)</brutto>'),
        'brutto_suggest': re.compile('<bruttosuggest>(.+)</bruttosuggest>'),
        'url': re.compile('<url>(.+)</url>'),
        'image_ok': re.compile('<imageOk>(.+)</imageOk>'),
        'image': re.compile('<image>(.+)</image>'),
        'manufacturer': re.compile('<manufacturer>(.+)</manufacturer>')
    }
    __RGX_description = re.compile('<description>(.+?)</description>')
    __RGX_multiline_description = [
        re.compile('<description>(.+)'),
        re.compile('(.+)</description>'),
        re.compile('(.+)(?!</attr>)')
    ]
    __RGX_attributes = re.compile('<attr>(.+)</attr>')
    __RGX_details = re.compile('color="(.+?)" rozmiar="(.+?)" onstock="(.+?)"')

    __RGX_neglect = {
        'header': re.compile(r'<\?xml version'),
        'footer': re.compile('</offers>')
    }
    __RGX_begin = re.compile('<offer>')
    __RGX_end = re.compile('</offer>')

    def __init__(self):
        Supplier.__init__(self)
        self._store = list()

    def load(self, input_file):
        with open(input_file, 'r') as data_file:
            new_product = None
            for line in data_file:
                property_found = False
                if self.__RGX_end.search(line) or any([other.search(line) for other in self.__RGX_neglect.values()]):
                    new_product = None
                    continue
                if self.__RGX_begin.search(line):
                    new_product = dict()
                    continue
                for product_property, property_value in self.__RGX.items():
                    match_object = property_value.search(line)
                    if not match_object:
                        continue
                    else:
                        new_product[product_property] = match_object.group(1)
                        property_found = True
                        continue
                if not property_found:
                    if self.__RGX_attributes.search(line):
                        for variant in self.__RGX_details.findall(line):
                            new_product['color'] = variant[0]
                            new_product['size'] = variant[1]
                            new_product['onstock'] = variant[2]
                            self._store.append(new_product)
                        new_product = None
                        continue
                    match_object = self.__RGX_description.search(line)
                    if match_object:
                        new_product['description'] = match_object.group(1)
                        continue
                    elif any([desc_line.search(line) for desc_line in self.__RGX_multiline_description]):
                        match_object = self.__RGX_multiline_description[0].search(line) or \
                                       self.__RGX_multiline_description[1].search(line) or \
                                       self.__RGX_multiline_description[2].search(line)
                        try:
                            new_product['description'] = "{0}{1}".format(
                                new_product['description'], match_object.group(1)
                            )
                        except KeyError:
                            new_product['description'] = match_object.group(1)
