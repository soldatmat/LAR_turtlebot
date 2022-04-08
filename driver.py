import CONST
import numpy as np
from camera import *

INFO = True


class Driver:

    def __init__(self, turtle):
        self.turtle = turtle
        self.busy = True
        self.main = MainActivity(self, self)
        self.counter = 0

        self.color = CONST.BLUE

    def drive(self):
        if not self.busy:
            return None  #TODO

        if INFO: print()

        self.counter += 1
        self.main.perform()
        self.turtle.keep_speed()


# Abstract Activity
class Activity:

    def __init__(self, parent, driver):
        self.parent = parent
        self.driver = driver
        self.turtle = driver.turtle

        self.activity = None
        self.busy = False
        self.ret = None

        self._first = True

    def start(self):
        return None

    def perform_init(self):
        if INFO:
            print(str(self.driver.counter) + ": " + str(type(self)) + " perform")

        if self._first:
            self._first = False
            self.start()

    # def perform(self)

    def do(self, activity):
        self.activity = activity
        self.busy = True
        activity.perform()

    def end(self):
        self.parent.busy = False


class MainActivity(Activity):

    def __init__(self, parent, driver):
        Activity.__init__(self, parent, driver)

        self.overshoot = 0.2

    def perform(self):
        Activity.perform_init(self)
        if self.busy:
            return self.activity.perform()

        if self.activity is None or isinstance(self.activity, Forward):
            return self.do(FindTwoSticks(self, self.driver, window=False))

        if isinstance(self.activity, FindTwoSticks):
            # TODO
            dist = 0.2
            return self.do(Forward(self, self.driver, dist))

        self.end()


class FindTwoSticks(Activity):

    def __init__(self, parent, driver, speed=np.pi/12, center_limit=20, window=False):
        Activity.__init__(self, parent, driver)
        self.speed = speed
        self.center_limit = center_limit # in pixels
        self.window = window

        if window:
            self.w_bin = Window("FindTwoSticks")

    def perform(self):
        Activity.perform_init(self)
        if self.busy:
            return self.activity.perform()

        hsv = self.turtle.get_hsv_image()
        bin_img = img_threshold(hsv, self.driver.color)
        sticks = self.driver.turtle.get_segments(self.driver.color, bin_img=bin_img)

        # Testing window
        if self.window:
            self.w_bin.show(bin_to_rgb(bin_img))

        if sticks.count < 2:
            self.turtle.set_speed(0, self.speed)
            return

        print(sticks.count)
        print(np.shape(sticks.areas))
        print(np.shape(sticks.centroids))
        args = np.argsort(sticks.areas)
        center = (sticks.centroids[args[0]] + sticks.centroids[args[1]]) / 2

        diff = center[1] - (np.shape(bin_img)[1] / 2)
        if abs(diff) > self.center_limit:
            if diff < 0:
                self.turtle.set_speed(0, -self.speed)
            else:
                self.turtle.set_speed(0, self.speed)
            return

        self.turtle.stop()
        self.end()


class Forward(Activity):

    def __init__(self, parent, driver, dist, speed=0.2):
        Activity.__init__(self, parent, driver)
        self.dist = dist
        self.speed = speed
        self.turtle.reset_odometry()

    def start(self):
        self.turtle.set_speed(self.speed, 0)

    def perform(self):
        Activity.perform_init(self)
        if self.busy:
            return self.activity.perform()

        odometry = self.turtle.get_odometry()
        if self.dist - odometry[0] < self.speed * (CONST.SLEEP / 1000) / 2:
            self.turtle.stop()
            self.end()


# class Goto(Activity):
#
#     def __init__(self, parent, driver, target):
#         Activity.__init__(self, parent, driver)
#
#         x = target[0]
#         z = target[2]
#         self.dist = np.sqrt(x ** 2 + z ** 2)
#         self.alpha = np.arccos(z / self.dist)
#
#     def perform(self):
#         Activity.perform_init(self)
#         if self.busy:
#             return self.activity.perform()
#
#         if self.activity is None:
#             return self.do(Turn(self, self.driver, self.alpha))
#
#         # if isinstance(self.activity, Turn): TODO
#         #     return self.do(Forward(self, self.driver, self.dist))
#
#         self.end()


# class Turn(Activity):
#
#     def __init__(self, parent, driver, degree, speed=np.pi/12):
#         Activity.__init__(self, parent, driver)
#         self.speed = speed
#         self.turn_for = degree / speed
#         self.start_time = time.perf_counter()
#
#     def start(self):
#         self.turtle.set_speed(0, self.speed)
#
#     def perform(self):
#         Activity.perform_init(self)
#         if self.busy:
#             return self.activity.perform()
#
#         if 1000 * (self.turn_for - (time.perf_counter() - self.start_time)) < CONST.SLEEP / 2:
#             self.turtle.stop()
#             self.end()
