import requests
from pprint import pprint

def get_obj(req):
    geocoder_api_server = "http://geocode-maps.yandex.ru/1.x/"
    geocoder_params = {
        "apikey": "40d1649f-0493-4b70-98ba-98533de7710b",
        "geocode": req,
        "format": "json"}

    r = requests.get(geocoder_api_server, params=geocoder_params)
    json_response = r.json()
    toponym = json_response["response"]["GeoObjectCollection"][
        "featureMember"][0]["GeoObject"]
    delta_x = abs(
        float(toponym['boundedBy']['Envelope']['lowerCorner'].split()[0]) -
        float(toponym['boundedBy']['Envelope']['upperCorner'].split()[0]))
    delta_y = abs(
        float(toponym['boundedBy']['Envelope']['lowerCorner'].split()[1]) -
        float(toponym['boundedBy']['Envelope']['upperCorner'].split()[1]))

    address = toponym['metaDataProperty']['GeocoderMetaData']['AddressDetails']['Country']['AddressLine']
    coords = toponym["Point"]["pos"]

    return coords, delta_x, delta_y, address

