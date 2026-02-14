from PyQt6.QtWidgets import QApplication, QMainWindow
import sys
import requests
from io import BytesIO
from PyQt6.QtGui import QPixmap
from PyQt6 import uic
from PIL import Image
from PyQt6.QtCore import Qt


class MapWindow(QMainWindow):
    """ MAIN WINDOW """

    def __init__(self):
        super().__init__()

        uic.loadUi("map.ui", self)

        self.delta = 0.05
        self.lon = 37.619073
        self.lat = 55.745794
        self.coords = f"{self.lon},{self.lat}"

        self.address.setText(self.coords)
        self.map.setPixmap(QPixmap("map.png"))

        self.address.returnPressed.connect(self.update_pixmap_from_input)
        self.setFocusPolicy(Qt.FocusPolicy.StrongFocus)
        self.setFocus()
        self.update_pixmap()

    def update_coords(self, delta_x: float, delta_y: float):
        """Обновление координат с проверкой границ"""
        new_lon = self.lon + delta_x
        new_lat = self.lat + delta_y
        self.lon = max(-180, min(180, new_lon))
        self.lat = max(-85, min(85, new_lat))
        self.coords = f"{self.lon:.6f},{self.lat:.6f}"
        self.setWindowTitle(self.coords)
        self.address.setText(self.coords)
        self.update_pixmap()

    def update_pixmap_from_input(self):
        """Обновление карты из поля ввода"""
        try:
            input_text = self.address.text()
            if input_text:
                new_coords = input_text.split(',')
                if len(new_coords) == 2:
                    new_lon = float(new_coords[0].strip())
                    new_lat = float(new_coords[1].strip())
                    if -180 <= new_lon <= 180 and -85 <= new_lat <= 85:
                        self.lon = new_lon
                        self.lat = new_lat
                        self.coords = f"{self.lon:.6f},{self.lat:.6f}"
                    else:
                        self.address.setText(self.coords)
                else:
                    self.address.setText(self.coords)
        except ValueError:
            self.address.setText(self.coords)

        self.address.clearFocus()
        self.update_pixmap()

    def update_pixmap(self):
        params = {
            "ll": f"{self.lon},{self.lat}",
            "spn": f"{self.delta},{self.delta}",
            "size": "650,450",
            "l": "map"
        }

        try:

            response = requests.get("https://static-maps.yandex.ru/1.x/", params)

            if response.status_code == 200:
                img = Image.open(BytesIO(response.content))
                img.save('map.png')
                self.map.setPixmap(QPixmap("map.png"))
            else:
                print(f"Ошибка API: {response.status_code}")
                print(f"URL: {response.url}")
        except Exception as e:
            print(f"Ошибка при загрузке карты: {e}")

    def keyPressEvent(self, event):
        key = event.key()
        if key == Qt.Key.Key_PageUp:
            self.delta = min(self.delta + 0.005, 90.0)
            self.update_pixmap()
            print(f"Масштаб увеличен: {self.delta}")
        elif key == Qt.Key.Key_PageDown:
            self.delta = max(self.delta - 0.005, 0.001)
            self.update_pixmap()
            print(f"Масштаб уменьшен: {self.delta}")
        elif key == Qt.Key.Key_Up:
            self.update_coords(0, self.delta)
        elif key == Qt.Key.Key_Down:
            self.update_coords(0, -self.delta)
        elif key == Qt.Key.Key_Right:
            self.update_coords(self.delta, 0)
        elif key == Qt.Key.Key_Left:
            self.update_coords(-self.delta, 0)


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