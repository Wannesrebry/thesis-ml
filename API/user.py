import json
from collections import namedtuple

class GoogleUser:

    def __init__(self, google_response):
        response_object = json.loads(google_response.content.decode())
        for key in dict(response_object).keys():
            self.__dict__[key] = response_object[key]

    def json(self):
        return json.dumps(self.__dict__)
