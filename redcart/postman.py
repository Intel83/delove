import simplejson as json
import urllib.parse
import urllib.request


class Postman:
    def __init__(self):
        self.__request_address = "http://api2.redcart.pl/?input=json"
        self.__artur_key = "e7c443e1d1154bcea3b17e233e58bdfa"
        self.__view_type = 'json'
        self.__result = None

    def __send(self, content):
        content['key'] = self.__artur_key
        content['viewType'] = self.__view_type
        json_data = {self.__view_type: json.dumps(content)}
        post_data = urllib.parse.urlencode(json_data)
        req = urllib.request.Request(self.__request_address, post_data)
        opener = urllib.request.build_opener()
        f = opener.open(req)
        self.__result = json.load(f)
