from PyQt6.QtWidgets import QApplication, QMainWindow
import sys
import requests


class MapWindow(QMainWindow):
    """ MAIN WINDOW """
    
    def __init__(self):
        super().__init__()
        
        ...
    
    def update_pixmap(self):
        """ Обновление картинки карты """
        
        response = requests.get("")
    

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