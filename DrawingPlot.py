import matplotlib.pyplot as plt
from matplotlib.text import *
import matplotlib.animation as animation
import BezierCurve
import threading


class DrawingPlot(threading.Thread):
    def __init__(self,
                 size,
                 amplitude_min,
                 amplitude_max,
                 amplitude_lerp_speed,
                 x_squish,
                 y_squish,
                 bezier_visibility,
                 invert_color,
                 constant_increase,
                 is_drawing_instant,
                 frequency
                 ):
        threading.Thread.__init__(self, name = "Drawing Plot Tread")
        self.size = size
        self.amplitude_min = amplitude_min
        self.amplitude_max = amplitude_max
        self.amplitude_lerp_speed = amplitude_lerp_speed
        self.x_squish = x_squish
        self.y_squish = y_squish
        self.bezier_visibility = bezier_visibility
        self.constant_increase = constant_increase
        self.is_drawing_instant = is_drawing_instant

        self.amplitude = self.amplitude_min
        self.frequency = frequency

        self.is_first_cycle = True
        self.points_exist = True

        self.xar = []
        self.yar = []

        self.move_speed = 100
        self._frequency = 0.5
        self.phase = 0.0

        self.ax = None
        self.ani = None
        self.is_increasing = False

        if invert_color:
            self.line_color = 'white'
            self.bg_color = '#2f3136'
        else:
            self.line_color = '#2f3136'
            self.bg_color = 'white'

        # THE BEZIER CURVE SECTION #
        self.bezier_curve = BezierCurve.BezierCurve()
        self.points_file = self.bezier_curve.get_points_from_file("data/points.txt")

        self.bezier_points = self.bezier_curve.get_bezier_points(self.points_file, 0.01)

        self.index = 0
        self.initial_bezier_point = []
        self.target_bezier_point = self.bezier_points[0]

        self.bezier_x = []
        self.bezier_y = []

        for points in self.bezier_points:
            self.bezier_x.append(points[0])
            self.bezier_y.append(points[1])

    def run(self):
        fig = plt.figure(1, facecolor=self.bg_color, figsize=(2, 2), dpi=400)
        self.ax = fig.add_subplot(111)

        self.ax.set_frame_on(False)
        self.ax.axes.get_yaxis().set_visible(False)
        self.ax.axes.get_xaxis().set_visible(False)

        if self.is_drawing_instant:
            i = 0
            self.animate(i)
            while self.points_exist:
                self.animate(i)
                i += 1

            self.render_points()
        else:
            self.ani = animation.FuncAnimation(fig, self.animate, interval=1)

        plt.show()

    def animate(self, i):
        if self.is_first_cycle:
            self.is_first_cycle = False
            return

        t = (i / 5)

        if not self.constant_increase:
            self.amplitude = self.lerp_loop(t, self.amplitude_min, self.amplitude_max, self.amplitude_lerp_speed)
        else:
            self.amplitude = self.lerp_to_max(self.amplitude, self.amplitude_lerp_speed)

        if self.frequency is not self._frequency:
            self.calc_new_freq(t)

        transform_point = self.get_bezier_transform(t, self.move_speed)

        if transform_point is None:
            return

        x = self.x_squish * self.amplitude * math.sin(t * self._frequency + self.phase) + transform_point[0]
        y = self.y_squish * self.amplitude * math.cos(t * self._frequency + self.phase) - self.amplitude + transform_point[1]

        self.xar.append(x)
        self.yar.append(y)

        if not self.is_drawing_instant:
            self.render_points()

    def render_points(self):
        self.ax.clear()
        self.ax.scatter([-self.size - 2, self.size], [-self.size - 2, self.size], alpha=0)

        self.ax.plot(self.xar, self.yar, linewidth=0.1, color=self.line_color)

        # Bezier Section
        if self.bezier_visibility:
            self.ax.plot(self.bezier_x, self.bezier_y, 'c--', linewidth=0.3)

            for points in self.points_file:
                self.ax.plot(points[0], points[1], 'x', markersize=0.5, color='cyan')

    def stop_animation(self):
        if self.ani:
            self.ani.event_source.stop()

    def get_bezier_transform(self, time, lerp_speed):
        lerp_speed = 1 / lerp_speed * 1000
        pos = (time % lerp_speed) / lerp_speed
        if pos == 0:
            self.initial_bezier_point = self.target_bezier_point
            self.index += 1
            try:
                self.target_bezier_point = self.bezier_points[self.index]
            except IndexError:
                self.stop_animation()
                self.points_exist = False
                return None

        return BezierCurve.BezierCurve.lerp(pos, self.initial_bezier_point, self.target_bezier_point)

    def calc_new_freq(self, time):
        curr_freq = (time * self._frequency + self.phase) % (2 * math.pi)
        next_freq = (time * self.frequency) % (2 * math.pi)
        self.phase = curr_freq - next_freq
        self._frequency = self.frequency

    def lerp_to_max(self, current, step):
        step = step / 10000
        return current + step

    @staticmethod
    def lerp(time, a, b, lerp_speed):
        lerp_speed = 1 / lerp_speed * 1000
        pos = (time % lerp_speed) / lerp_speed
        return (pos * b) + ((1 - pos) * a)

    def lerp_loop(self, time, a, b, lerp_speed):
        lerp_speed = 1 / lerp_speed * 1000
        pos = (time % lerp_speed) / lerp_speed

        if pos == 0:
            self.is_increasing = not self.is_increasing

        if not self.is_increasing:
            pos = 1 - pos

        return (pos * b) + ((1 - pos) * a)
