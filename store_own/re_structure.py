"""
< Produkt >
< Nr_katalogowy_cechy > <![CDATA[10 - 26405381021]] > < / Nr_katalogowy_cechy > // klucz główny
< Kod_ean_cechy > <![CDATA[4024144130061]] > < / Kod_ean_cechy >                // klucz główny(Boss)
< Ilosc_produktow > 100.00 < / Ilosc_produktow >
< Dostepnosc > <![CDATA[AUTOMATYCZNY]] > < / Dostepnosc >
< Termin_wysylki > <![CDATA[do 7 dni]] > < / Termin_wysylki >
< / Produkt >
"""
import re
from .product_update import ProductUpdate
string_pattern = r"<\s?{tag}\s?>\s?...CDATA.(.+)...\s?<\s?/\s?{tag}\s?>"
int_pattern = r"<\s?{tag}\s?>\s?(.+)\s?<\s?/\s?{tag}\s?>"

PRODUCT = re.compile(r"<\s?Produkt\s?>(.+?)<\s?/\s?\s?Produkt\s?>", re.MULTILINE | re.DOTALL)
CAT_NO = re.compile(string_pattern.format(tag=ProductUpdate.props[0]))
EAN = re.compile(string_pattern.format(tag=ProductUpdate.props[1]))
QUANTITY = re.compile(int_pattern.format(tag=ProductUpdate.props[2]))
AVAIL = re.compile(string_pattern.format(tag=ProductUpdate.props[3]))
POST_TIME = re.compile(string_pattern.format(tag=ProductUpdate.props[4]))
