import sys
from PyQt5 import QtWidgets
from python_event_bus import EventBus
from . import first_screen_ui
import signal

signal.signal(signal.SIGINT, signal.SIG_DFL)

main_window=None

class MainWindow(QtWidgets.QMainWindow, first_screen_ui.Ui_MainWindow):
    def __init__(self, *args, **kwargs):
        QtWidgets.QMainWindow.__init__(self, *args, **kwargs)
        self.setupUi(self)
        self.label.setText("Haz clic en el botón")
        self.pushButton.setText("Presióname")
        
        self.pushButton.clicked.connect(self.update)

    def update(self):
        self.label.setText("¡Acabas de hacer clic en el botón!")
        EventBus.call("qt5_message", "I'm using qt5")
        EventBus.call("message", "Click en QT5")

    def ws_message(self,message):
        self.label.setText(f"{message}")

@EventBus.on("ws_message")
def ws_message(message):
    main_window.ws_message(message)

def init_main_window():
    global main_window
    main_app = QtWidgets.QApplication([])
    main_window = MainWindow()
    main_window.show()
    main_app.exec_()
    
if __name__=="__main__":
    init_main_window()