from PyQt6.QtWidgets import QApplication, QMainWindow
import sys
import requests
from io import BytesIO
from PyQt6.QtGui import QPixmap
from PyQt6 import uic
from PIL import Image
from PyQt6.QtCore import Qt


class MapWindow(QMainWindow):
    """MAIN WINDOW"""

    def __init__(self):
        super().__init__()
        self.theme_style = "light"

        uic.loadUi("map.ui", self)

        self.delta = 0.05
        self.coords = "37.619073,55.745794"
        self.mark_coords = ""
        self.set_mark = False

        self.map.setPixmap(QPixmap("map.png"))

        self.address.setText(self.coords)
        self.address.returnPressed.connect(self.coords_address_update)
        self.address_mark.returnPressed.connect(self.lineedit_pressed)
        self.theme.clicked.connect(self.change_theme)
        self.address.setFocusPolicy(Qt.FocusPolicy.ClickFocus)
        self.address_mark.setFocusPolicy(Qt.FocusPolicy.ClickFocus)
        self.update_pixmap()
        self.setWindowTitle(self.coords)

    def update_coords(self, delta_x: float, delta_y: float):
        x, y = map(float, self.coords.split(","))
        x += delta_x
        y += delta_y
        self.coords = f"{x},{y}"
        self.setWindowTitle(self.coords)
        self.address.setText(self.coords)
        self.update_pixmap()

    def coords_address_update(self):
        """Обновление карты по координтам"""
        self.address_mark.setText("")  # Отчистка адресса в поле ввода
        self.lineedit_pressed()

    def lineedit_pressed(self):
        self.set_mark = False
        self.address_mark.setStyleSheet("")
        self.coords = self.address.text()
        self.mark = self.address_mark.text()
        if self.mark:
            self.get_mark_coords()
        self.address.clearFocus()
        self.address_mark.clearFocus()
        self.update_pixmap()

    def get_mark_coords(self):
        """Обновление координат по метке"""
        server_address = "https://geocode-maps.yandex.ru/1.x/?"

        params = {
            "apikey": "8013b162-6b42-4997-9691-77b7074026e0",
            "geocode": self.mark,
            "format": "json",
        }

        response = requests.get(server_address, params)
        if response.status_code == 200:
            self.set_mark = True
            data = response.json()
            coords = data["response"]["GeoObjectCollection"]["featureMember"][0][
                "GeoObject"
            ]["Point"]["pos"].split()
            coords = ",".join(coords)
            self.coords = coords
            self.mark_coords = coords
            self.address.setText(self.coords)

        else:
            self.address_mark.setStyleSheet('background-color: "red"')

    def update_pixmap(self):
        """Обновление картинки карты"""
        params = {
            "apikey": "f3a0fe3a-b07e-4840-a1da-06f18b2ddf13",
            "ll": self.coords,
            "spn": f"{self.delta},{self.delta}",
        }

        if self.theme_style == "dark":
            params["theme"] = "dark"

        if self.set_mark:
            params["pt"] = self.mark_coords

        if not self.coords:
            params["ll"] = "37.619073,55.745794"

        response = requests.get("https://static-maps.yandex.ru/v1", params)
        if not response:
            self.address.setStyleSheet('background-color: "red"')
        else:
            self.address.setStyleSheet("")
            img = Image.open(BytesIO(response.content))
            img.save("map.png")
            self.map.setPixmap(QPixmap("map.png"))
            self.setWindowTitle(self.address.text())

    def change_theme(self):
        if self.theme_style == "light":
            self.theme_style = "dark"
        else:
            self.theme_style = "light"
        self.update_pixmap()

    def keyPressEvent(self, event):
        key = event.key()
        if key == Qt.Key.Key_PageUp:
            self.delta += 0.005
            self.update_pixmap()
        elif key == Qt.Key.Key_PageDown:
            self.delta -= 0.005
            self.update_pixmap()
        elif key == Qt.Key.Key_Up:
            self.update_coords(0, 0.005)
        elif key == Qt.Key.Key_Down:
            self.update_coords(0, -0.005)
        elif key == Qt.Key.Key_Right:
            self.update_coords(0.005, 0)
        elif key == Qt.Key.Key_Left:
            self.update_coords(-0.005, 0)


def except_hook(cls, exception, traceback):
    sys.__excepthook__(cls, exception, traceback)


def main():
    app = QApplication(sys.argv)
    window = MapWindow()
    window.show()
    sys.excepthook = except_hook
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
