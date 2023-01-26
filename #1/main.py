import sys
import json
import pygame
import os
from get_obj import get_obj
import requests
from PIL import Image

PATH = 'data/img.png'


def save_map(adress, path):
    obj_coodrinates, d_x, d_y = get_obj(adress)
    x, y = obj_coodrinates.split(" ")
    map_params = {
        "ll": ",".join([x, y]),
        "spn": ",".join([str(d_x), str(d_y)]),
        "l": "map",
        "pt": f"{','.join(obj_coodrinates.split())},pm2dgl"
    }
    map_api_server = "http://static-maps.yandex.ru/1.x/"
    response = requests.get(map_api_server, params=map_params)
    with open(path, 'wb') as f:
        f.write(response.content)


if __name__ == '__main__':
    pygame.init()
    save_map('Бутлерова, Казань', PATH)
    screen = pygame.display.set_mode((600, 450))
    screen.blit(pygame.image.load(PATH), (0, 0))
    pygame.display.flip()
    f = True
    while f:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                f = False
    pygame.quit()
    os.remove(PATH)

