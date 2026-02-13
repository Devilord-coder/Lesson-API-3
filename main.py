from PyQt6.QtWidgets import QApplication, QMainWindow
import sys
import requests
from io import BytesIO
from PyQt6.QtGui import QPixmap
from PyQt6 import uic
from PIL import Image


class MapWindow(QMainWindow):
    """ MAIN WINDOW """
    
    def __init__(self):
        super().__init__()
        
        uic.loadUi("map.ui", self)
        
        self.map.setPixmap(QPixmap("map.png"))
        
        self.address.returnPressed.connect(self.update_pixmap)
    
    def update_pixmap(self):
        """ Обновление картинки карты """
        
        params = {
            "apikey": "f3a0fe3a-b07e-4840-a1da-06f18b2ddf13",
            "ll": self.address.text(),
            "spn": "0.05,0.05"
        }
        
        if not self.address.text:
            params["ll"] = "37.619073,55.745794"
        
        response = requests.get("https://static-maps.yandex.ru/v1", params)
        if not response:
            return
        else:
            img = Image.open(BytesIO(response.content))
            img.save('map.png')
            self.map.setPixmap(QPixmap("map.png"))
    

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