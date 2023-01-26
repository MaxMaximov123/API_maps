import sys
import json
import pygame as pg
import os
from get_obj import get_obj
import requests
from PIL import Image

PATH = 'img.png'
delta = 1
STEP = 1.3
ADRESS = 'Бутлерова, Казань'
current_pos, D_X, D_Y = get_obj(ADRESS)
current_pos = list(map(float, current_pos.split(' ')))
SLICES = ['map', 'sat', 'skl', 'trf']
slice_ind = 0


def save_map(adress, path, delta0=delta):
    obj_coodrinates, d_x, d_y = get_obj(adress)
    x, y = obj_coodrinates.split(" ")
    map_params = {
        "ll": ",".join([x, y]),
        "spn": ",".join([str(delta), str(delta)]),
        "l": SLICES[slice_ind % len(SLICES)],
    }
    map_api_server = "http://static-maps.yandex.ru/1.x/"
    response = requests.get(map_api_server, params=map_params)
    with open(path, 'wb') as f:
        f.write(response.content)
    screen.blit(pg.image.load(PATH), (0, 0))
    pg.display.flip()


if __name__ == '__main__':
    pg.init()
    screen = pg.display.set_mode((600, 450))
    save_map(f'{current_pos[0]},{current_pos[1]}', PATH)
    f = True
    while f:
        screen.fill((0, 0, 0))
        for event in pg.event.get():
            if event.type == pg.QUIT:
                f = False
            if event.type == pg.KEYDOWN:
                print(current_pos)
                if event.key == pg.K_PAGEUP:
                    if delta * STEP <= 90:
                        delta *= STEP
                        save_map(f'{current_pos[0]},{current_pos[1]}', PATH, delta0=delta)
                if event.key == pg.K_PAGEDOWN:
                    if delta / STEP > 0:
                        delta /= STEP
                        save_map(f'{current_pos[0]},{current_pos[1]}', PATH, delta0=delta)
                if event.key == pg.K_LEFT:
                    current_pos[0] = (current_pos[0] + delta * 2) % 180
                    save_map(f'{current_pos[0]},{current_pos[1]}', PATH, delta0=delta)
                if event.key == pg.K_RIGHT:
                    current_pos[0] = (current_pos[0] - delta * 2) % 180
                    save_map(f'{current_pos[0]},{current_pos[1]}', PATH, delta0=delta)
                if event.key == pg.K_UP:
                    current_pos[1] += delta * 2
                    if current_pos[1] > 85:
                        current_pos[1] = -85 + (current_pos[1] - 85)
                    save_map(f'{current_pos[0]},{current_pos[1]}', PATH, delta0=delta)
                if event.key == pg.K_DOWN:
                    current_pos[1] -= delta * 2
                    if current_pos[1] < -85:
                        current_pos[1] = -85 + abs(current_pos[1]) - 85
                    save_map(f'{current_pos[0]},{current_pos[1]}', PATH, delta0=delta)
                if event.key == pg.K_TAB:
                    slice_ind += 1
                    save_map(f'{current_pos[0]},{current_pos[1]}', PATH, delta0=delta)
    pg.quit()
    os.remove(PATH)

