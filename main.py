from QT5 import init as init_qt5
from PyQt5 import QtWidgets
from api import ws_run as run_api
from threading import Thread
from event_bus import message_event
import sys

if __name__ == "__main__":
    api_thread = Thread(target=run_api)
    qt5_thread = Thread(target=lambda: init_qt5())

    # Empezar los hilos
    api_thread.start()
    qt5_thread.start()

    try:
        # Wait for the threads to complete
        api_thread.join()
        qt5_thread.join()
    except KeyboardInterrupt:
        print("Interrupt received, stopping threads...")
        QtWidgets.QApplication.quit()  # Stop the PyQt5 application
        sys.exit(0)  # Exit the program with status code 0 (success)