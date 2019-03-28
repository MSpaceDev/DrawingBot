class BezierCurve:
    def __init__(self):
        pass

    @staticmethod
    def get_points_from_file(path):
        """
        :param path: Path to file containing points
        :type path: str
        :return: (2D Array) All Points in specified path with format "x,y"
        """
        pts = []

        with open(path, "r+") as f:
            new_points = []
            pts_raw = f.readlines()
            for pt in pts_raw:
                pt = pt.replace("\n", "")
                new_points.append(pt)

            for l in new_points:
                x, y = l.split(",")
                pts.append([int(x), int(y)])

        return pts

    def get_bezier_points(self, points, step=0.05):
        """
        :param points: (2D Array) Points in order. Start point, Control Points, End Point.
        :type points: list
        :param step: The step from 0 to 1. Lower values means a smoother curve
        :type step: float
        :return: (2D Array) All points in the bezier curve using step
        """

        bezier_points = []

        curve_points = self.get_curve_points(points)

        for i in range(len(curve_points) - 2):
            pos = -step
            while pos < 1:
                pos += step

                if pos > 1:     # Makes sure 1.0 is used as step
                    pos = 1

                    if i % 2 == 0:
                        p0 = self.lerp(pos, curve_points[i + 0], curve_points[i + 1])
                        p1 = self.lerp(pos, curve_points[i + 1], curve_points[i + 2])
                        bezier_points.append(self.lerp(pos, p0, p1))
                    break

                if i % 2 == 0:
                    p0 = self.lerp(pos, curve_points[i + 0], curve_points[i + 1])
                    p1 = self.lerp(pos, curve_points[i + 1], curve_points[i + 2])
                    bezier_points.append(self.lerp(pos, p0, p1))

        if len(curve_points) == 2:
            pos = -step
            while pos < 1:
                pos += step

                if pos > 1:  # Makes sure 1.0 is used as step
                    pos = 1
                    bezier_points.append(self.lerp(pos, curve_points[0], curve_points[1]))

                bezier_points.append(self.lerp(pos, curve_points[0], curve_points[1]))

        return self.clean_points(bezier_points)

    @staticmethod
    def clean_points(points):
        for i in range(len(points)-2):
            try:
                if points[i] == points[i+1]:
                    points.pop(i)
            except IndexError:
                pass

        return points

    def get_curve_points(self, points):
        curve_points = []

        if len(points) >= 4:
            curve_points.append(points[0])
            curve_points.append(points[1])

            for i in range(0, len(points) - 3):
                curve_points.append(self.get_midpoint(points[i+1], points[i+2]))
                curve_points.append(points[i+2])

            curve_points.append(points[len(points) - 1])
        else:
            curve_points = points

        return curve_points

    @staticmethod
    def lerp(step, p0, p1):
        x = (step * p1[0]) + ((1 - step) * p0[0])
        y = (step * p1[1]) + ((1 - step) * p0[1])
        return [x, y]

    @staticmethod
    def get_midpoint(p0, p1):
        x_mid = (p0[0] + p1[0]) / 2
        y_mid = (p0[1] + p1[1]) / 2

        return [x_mid, y_mid]
