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
		self.point = None
		uic.loadUi('main.ui', self)
		self.path = 'img.png'
		self.slices = ['map', 'sat', 'skl', 'trf']
		self.slice_ind = 0
		self.address = 'Бутлерова, Казань'
		self.current_pos, D_X, D_Y, address_obg, post_code = get_obj(self.address)
		self.current_pos = list(map(float, self.current_pos.split(' ')))
		self.delta = 1
		self.step = 1.3
		self.initUI()
		self.save_map()

	def save_map(self, point=False):
		address = self.lineEdit.text()
		if point and address:
			self.current_pos, D_X, D_Y, address_obg, post_code = get_obj(address)
			self.current_pos = list(map(float, self.current_pos.split(' ')))
			self.delta = min(D_X, D_Y)
			self.point = f'{self.current_pos[0]},{self.current_pos[1]}'
			if self.checkBox.isChecked() and post_code:
				address_obg += '\n' + f'Почтовый индекс: {post_code}'
			self.textEdit.clear()
			self.textEdit.insertPlainText(address_obg)
		obj_coodrinates, d_x, d_y, address_obg, post_code = get_obj(f'{self.current_pos[0]},{self.current_pos[1]}')
		x, y = obj_coodrinates.split(" ")
		map_params = {
			"ll": ",".join([x, y]),
			"spn": ",".join([str(self.delta), str(self.delta)]),
			"l": self.slices[self.slice_ind % len(self.slices)],
		}
		if self.point:
			map_params['pt'] = f"{self.point},pm2dgl"
		map_api_server = "http://static-maps.yandex.ru/1.x/"
		response = requests.get(map_api_server, params=map_params)
		with open(self.path, 'wb') as img:
			img.write(response.content)
		self.pixmap = QPixmap(self.path)
		self.image.setPixmap(self.pixmap)

	def initUI(self):
		self.setWindowTitle('Карты')
		self.image.resize(600, 450)
		self.pixmap = QPixmap(self.path)
		self.image.setPixmap(self.pixmap)
		self.pushButton.clicked.connect(partial(self.save_map, point=True))
		self.pushButton_2.clicked.connect(self.clear)
		self.checkBox.stateChanged.connect(self.show_post_code)

	def show_post_code(self):
		address = self.lineEdit.text()
		if address:
			self.current_pos, D_X, D_Y, address_obg, post_code = get_obj(address)
			self.current_pos = list(map(float, self.current_pos.split(' ')))
			self.delta = min(D_X, D_Y)
			self.point = f'{self.current_pos[0]},{self.current_pos[1]}'
			if self.checkBox.isChecked() and post_code:
				address_obg += '\n' + f'Почтовый индекс: {post_code}'
			self.textEdit.clear()
			self.textEdit.insertPlainText(address_obg)

	def keyPressEvent(self, event):
		if event.key() == Qt.Key_PageUp:
			if self.delta * self.step <= 90:
				self.delta *= self.step
			self.save_map()
		if event.key() == Qt.Key_PageDown:
			if self.delta / self.step > 0:
				self.delta /= self.step
			self.save_map()
		if event.key() == Qt.Key_Right:
			self.current_pos[0] = (self.current_pos[0] + self.delta) % 180
			self.save_map()
		if event.key() == Qt.Key_Left:
			self.current_pos[0] = (self.current_pos[0] - self.delta) % 180
			self.save_map()
		if event.key() == Qt.Key_Up:
			self.current_pos[1] += self.delta / 2
			if self.current_pos[1] > 85:
				self.current_pos[1] = -85 + (self.current_pos[1] - 85)
			self.save_map()
		if event.key() == Qt.Key_Down:
			self.current_pos[1] -= self.delta / 2
			if self.current_pos[1] < -85:
				self.current_pos[1] = -85 + abs(self.current_pos[1]) - 85
			self.save_map()
		if event.key() == Qt.Key_F1:
			self.slice_ind += 1
			self.save_map()

	def closeEvent(self, event):
		os.remove(self.path)

	def keyReleaseEvent(self, event):
		if self.focusWidget().objectName() == 'lineEdit':
			if event.key() == Qt.Key_Right:
				self.current_pos[0] = (self.current_pos[0] + self.delta) % 180
				self.save_map()
			if event.key() == Qt.Key_Left:
				self.current_pos[0] = (self.current_pos[0] - self.delta) % 180
				self.save_map()
		else:
			super().keyPressEvent(event)

	def clear(self):
		self.point = None
		self.save_map()
		self.lineEdit.setText('')
		self.textEdit.clear()


def except_hook(cls, exception, traceback):
	sys.__excepthook__(cls, exception, traceback)


if __name__ == '__main__':
	app = QApplication(sys.argv)
	sys.excepthook = except_hook
	ex = Example()
	ex.show()
	sys.exit(app.exec())
