import sys
import json
import pygame as pg
import os
from get_obj import get_obj
import requests
from PIL import Image

PATH = 'img.png'
delta = 10
STEP = 1.3
ADRESS = 'Бутлерова, Казань'


def save_map(adress, path, delta0=delta):
    obj_coodrinates, d_x, d_y = get_obj(adress)
    x, y = obj_coodrinates.split(" ")
    map_params = {
        "ll": ",".join([x, y]),
        "spn": ",".join([str(delta), str(delta * 3 / 4)]),
        "l": "map",
        "pt": f"{','.join(obj_coodrinates.split())},pm2dgl"
    }
    map_api_server = "http://static-maps.yandex.ru/1.x/"
    response = requests.get(map_api_server, params=map_params)
    with open(path, 'wb') as f:
        f.write(response.content)


if __name__ == '__main__':
    pg.init()
    save_map(ADRESS, PATH)
    screen = pg.display.set_mode((600, 450))
    screen.blit(pg.image.load(PATH), (0, 0))
    pg.display.flip()
    f = True
    while f:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                f = False
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_UP:
                    if delta * STEP <= 45:
                        delta *= STEP
                        save_map(ADRESS, PATH, delta0=delta)
                        screen.blit(pg.image.load(PATH), (0, 0))
                        pg.display.flip()
                if event.key == pg.K_DOWN:
                    if delta / STEP > 0:
                        delta /= STEP
                        save_map(ADRESS, PATH, delta0=delta)
                        screen.blit(pg.image.load(PATH), (0, 0))
                        pg.display.flip()
    pg.quit()
    os.remove(PATH)

