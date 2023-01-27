import requests
from pprint import pprint
import math


def lonlat_distance(a, b):
	degree_to_meters_factor = 111 * 1000  # 111 километров в метрах
	a_lon, a_lat = a
	b_lon, b_lat = b
	radians_lattitude = math.radians((a_lat + b_lat) / 2.)
	lat_lon_factor = math.cos(radians_lattitude)
	dx = abs(a_lon - b_lon) * degree_to_meters_factor * lat_lon_factor
	dy = abs(a_lat - b_lat) * degree_to_meters_factor
	distance = math.sqrt(dx * dx + dy * dy)
	return distance


def get_organisation(name, coord):
	search_api_server = "https://search-maps.yandex.ru/v1/"
	api_key = "dda3ddba-c9ea-4ead-9010-f43fbc15c6e3"

	address_ll = coord

	search_params = {
		"apikey": api_key,
		"text": name,
		"lang": "ru_RU",
		"ll": address_ll,
		"type": "biz",
		'results': 1
	}

	response = requests.get(search_api_server, params=search_params)
	data = response.json()['features'][0]
	ret_data = {}
	if lonlat_distance(list(map(float, coord.split(','))), data['geometry']['coordinates']) < 50:
		ret_data['point'] = data['geometry']['coordinates']
		ret_data['text'] = data['properties']['description'] + '\n' + data['properties']['CompanyMetaData']['Categories'][0]['name'] + \
		'.' + data['properties']['name'] + '.\n' + 'График работы: ' + data['properties']['CompanyMetaData']['Hours']['text']
		return ret_data
