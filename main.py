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
        
        self.map.setPixmap(QPixmap("map.png"))
        
        self.address.setText(self.coords)
        self.address.returnPressed.connect(self.lineedit_pressed)
        self.theme.clicked.connect(self.change_theme)
        self.address.setFocusPolicy(Qt.FocusPolicy.ClickFocus)
        self.update_pixmap()
        self.setWindowTitle(self.coords)
    
    def update_coords(self, delta_x: float, delta_y: float):
        x, y = map(float, self.coords.split(','))
        x += delta_x
        y += delta_y
        self.coords = f"{x},{y}"
        self.setWindowTitle(self.coords)
        self.address.setText(self.coords)
        self.update_pixmap()
    
    def lineedit_pressed(self):
        self.coords = self.address.text()
        self.address.clearFocus()
        self.update_pixmap()
    
    def update_pixmap(self):
        """Обновление картинки карты"""

        params = {
            "apikey": "f3a0fe3a-b07e-4840-a1da-06f18b2ddf13",
            "ll": self.address.text(),
            "spn": f"{self.delta},{self.delta}",
        }

        if self.theme_style == "dark":
            params["style"] = "stylers.opacity:0.2"
        
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
