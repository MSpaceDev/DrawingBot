from json import dumps
from copy import deepcopy

class GUIParameters():
    def __init__(self):
        # Properties #
        self.graphSizeInt = 0
        self.amplitudeMinInt = 0
        self.amplitudeMaxInt = 0
        self.amplitudeLerpSpeedInt = 0
        self.xSquishInt = 0
        self.ySquishInt = 0
        self.bezierCurveVisibilityBool = False
        self.invertColorBool = False
        self.constantIncreaseBool = False
        self.animateBool = False
        self.frequencyFloat = 0
        self.point_objects = None

    def set_values(self, drawing_gui):
        self.graphSizeInt = int(drawing_gui.graphSize.get_value())
        self.amplitudeMinInt = float(drawing_gui.amplitudeMinText.get_value())
        self.amplitudeMaxInt = float(drawing_gui.amplitudeMaxText.get_value())
        self.amplitudeLerpSpeedInt = float(drawing_gui.amplitudeLerpSpeed.get_value())
        self.xSquishInt = int(drawing_gui.xSquish.get_value())
        self.ySquishInt = int(drawing_gui.ySquish.get_value())
        self.bezierCurveVisibilityBool = bool(drawing_gui.bezierCurveVisibility.isChecked.get())
        self.invertColorBool = bool(drawing_gui.invertColor.isChecked.get())
        self.constantIncreaseBool = bool(drawing_gui.constantIncrease.isChecked.get())
        self.animateBool = bool(drawing_gui.isDrawingInstant.isChecked.get())
        self.frequencyFloat = float(drawing_gui.frequency.get_value())

    def save(self, drawing_gui):
        self.set_values(drawing_gui)

        config = \
            {
                "size": self.graphSizeInt,
                "amp_min": self.amplitudeMinInt,
                "amp_max": self.amplitudeMaxInt,
                "amp_lerp_speed": self.amplitudeLerpSpeedInt,
                "x_squish": self.xSquishInt,
                "y_squish": self.ySquishInt,
                "bezier_visibility": self.bezierCurveVisibilityBool,
                "invert_color": self.invertColorBool,
                "constant_increase": self.constantIncreaseBool,
                "is_drawing_instant": self.animateBool,
                "frequency": self.frequencyFloat
            }

        with open("data/config.json", "w+") as f:
            f.write(dumps(config, indent=4))

    def is_equal(self, other):
        return self.graphSizeInt == other.graphSizeInt and \
            self.amplitudeMinInt == other.amplitudeMinInt and \
            self.amplitudeMaxInt == other.amplitudeMaxInt and \
            self.amplitudeLerpSpeedInt == other.amplitudeLerpSpeedInt and \
            self.xSquishInt == other.xSquishInt and \
            self.ySquishInt == other.ySquishInt and \
            self.bezierCurveVisibilityBool == other.bezierCurveVisibilityBool and \
            self.invertColorBool == other.invertColorBool and \
            self.constantIncreaseBool == other.constantIncreaseBool and \
            self.animateBool == other.animateBool and \
            self.frequencyFloat == other.frequencyFloat and \
            self.is_equal_point_objects(other.point_objects)

    def is_equal_point_objects(self, other):
        print (self.point_objects)
        return True
        # if other is None:
        #     other = deepcopy(self.point_objects)
        #     return False
        #
        # if len(other) != len(self.point_objects):
        #     return False
        #
        # for point in self.point_objects:
        #     for _point in other:
        #         if not (point[0] == _point[0] and point[1] == _point[1]):
        #             return False
        #
        # return True


    def clone(self):
        return deepcopy(self)
