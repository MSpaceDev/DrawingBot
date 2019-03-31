import threading
import time


class Updater(threading.Thread):
    is_active = False

    def __init__(self, name):
        Updater.is_active = True
        threading.Thread.__init__(self, name=name)
        self.drawing_GUI = None

    def set_drawing_GUI(self, drawing_GUI):
        self.drawing_GUI = drawing_GUI
        self.drawing_GUI.update_values()

    def run(self):
        while(True):
            self.drawing_GUI.update_values()
            # self.drawing_GUI.display_curve()
            break
            time.sleep(1)
