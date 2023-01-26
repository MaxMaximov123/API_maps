import sys
import json
import pygame as pg
import os
from get_obj import get_obj
import requests
from functools import partial
from PIL import Image
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import Qt
from PyQt5 import uic
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QMainWindow

SCREEN_SIZE = [600, 450]


class Example(QMainWindow):
    def __init__(self):
        super().__init__()
        self.pixmap = None
        self.show_point = False
        uic.loadUi('main.ui', self)
        self.path = 'img.png'
        self.slices = ['map', 'sat', 'skl', 'trf']
        self.slice_ind = 0
        self.adress = 'Бутлерова, Казань'
        self.current_pos, D_X, D_Y = get_obj(self.adress)
        self.current_pos = list(map(float, self.current_pos.split(' ')))
        self.delta = 1
        self.step = 1.3
        self.initUI()
        self.save_map()


    def save_map(self, point=False):
        adress = self.lineEdit.text()
        if point and adress:
            self.show_point = True
            self.current_pos, D_X, D_Y = get_obj(adress)
            self.current_pos = list(map(float, self.current_pos.split(' ')))
            self.delta = min(D_X, D_Y)
        print(adress)
        obj_coodrinates, d_x, d_y = get_obj(f'{self.current_pos[0]},{self.current_pos[1]}')
        x, y = obj_coodrinates.split(" ")
        map_params = {
            "ll": ",".join([x, y]),
            "spn": ",".join([str(self.delta), str(self.delta)]),
            "l": self.slices[self.slice_ind % len(self.slices)],
        }
        if self.show_point:
            map_params['pt'] = f"{self.current_pos[0]},{self.current_pos[1]},pm2dgl"
        map_api_server = "http://static-maps.yandex.ru/1.x/"
        response = requests.get(map_api_server, params=map_params)
        with open(self.path, 'wb') as img:
            img.write(response.content)
        self.pixmap = QPixmap(self.path)
        self.image.setPixmap(self.pixmap)


    def initUI(self):
        self.setGeometry(200, 200, *SCREEN_SIZE)
        self.setWindowTitle('Карты')
        self.image.resize(600, 450)
        self.pixmap = QPixmap(self.path)
        self.image.setPixmap(self.pixmap)
        self.pushButton.clicked.connect(partial(self.save_map, point=True))

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_PageUp:
            if self.delta * self.step <= 90:
                self.delta *= self.step
        if event.key() == Qt.Key_PageDown:
            if self.delta / self.step > 0:
                self.delta /= self.step
        if event.key() == Qt.Key_Right:
            self.current_pos[0] = (self.current_pos[0] + self.delta) % 180
        if event.key() == Qt.Key_Left:
            self.current_pos[0] = (self.current_pos[0] - self.delta) % 180
        if event.key() == Qt.Key_Up:
            self.current_pos[1] += self.delta / 2
            if self.current_pos[1] > 85:
                self.current_pos[1] = -85 + (self.current_pos[1] - 85)
        if event.key() == Qt.Key_Down:
            self.current_pos[1] -= self.delta / 2
            if self.current_pos[1] < -85:
                self.current_pos[1] = -85 + abs(self.current_pos[1]) - 85
        if event.key() == Qt.Key_Shift:
            self.slice_ind += 1
        self.save_map()

    def closeEvent(self, event):
        os.remove(self.path)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Example()
    ex.show()
    sys.exit(app.exec())