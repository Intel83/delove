from . import postman as pm


class Product:
    __Module = 'products'

    def __init__(self):
        self.__result = None
        self.__query_handler = pm.Postman()

    def __send_query(self, q):
        self.__query_handler.__send(q)
        self.__result = self.__query_handler.__result

    def count(self):
        query = {
            'module': self.__Module,
            'method': 'count',
            'parameters': {}
        }
        self.__send_query(query)

    def get_products(self, offset=0, limit=10):
        query = {
            'module': self.__Module,
            'method': 'select',
            'parameters': {},
            'options': {
                'offset': offset,
                'limit': limit
            }
        }
        self.__send_query(query)
