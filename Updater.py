import threading
import time

class Updater(threading.Thread):
    old_parameters = None
    def __init__(self, drawing_gui):
        threading.Thread.__init__(self, name = "Updater thread")
        self.parameters = drawing_gui.gui_parameters
        self.drawing_gui = drawing_gui


    def run(self):
        print (threading.active_count())
        u = Updater(self.drawing_gui)
        while not self.is_value_changed():
            print("no")
            time.sleep(0.1)
        u.start()
        self.drawing_gui.update()

    def is_value_changed(self):
        if Updater.old_parameters is None:
            Updater.old_parameters = self.parameters.clone()
            return True

        if not self.parameters.is_equal(Updater.old_parameters):
            Updater.old_parameters = self.parameters.clone()
            return True
        else:
            return False


class GUIParameterUpdater(threading.Thread):
    def __init__(self, drawing_gui):
        threading.Thread.__init__(self, name = "GUI Updater thread")
        self.drawing_gui = drawing_gui

    def run(self):
        while True:
            time.sleep(0.1)
            self.drawing_gui.gui_parameters.set_values(self.drawing_gui)
            print (self.drawing_gui.gui_parameters.graphSizeInt)
