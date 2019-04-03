from json import dumps
from copy import deepcopy


class GUIParameters:
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
        self.stored_bezier_points = []

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
        self.stored_bezier_points = []
        for i in range(len(drawing_gui.bezier_points)):
            self.stored_bezier_points.append([drawing_gui.bezier_points[i].x_pos, drawing_gui.bezier_points[i].y_pos])

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
            self.is_equal_point_objects(other)

    def is_equal_point_objects(self, other):
        if other is None:
            return False

        if len(other.stored_bezier_points) != len(self.stored_bezier_points):
            return False

        for i in range(len(self.stored_bezier_points)):
            cur_point = self.stored_bezier_points[i]
            other_point = other.stored_bezier_points[i]
            if cur_point[0] != other_point[0] or cur_point[1] != other_point[1]:
                return False

        return True

    def clone(self):
        return deepcopy(self)
