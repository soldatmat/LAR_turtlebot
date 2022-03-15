from __future__ import print_function
from robolab_turtlebot import Turtlebot, Rate
import numpy as np
import cv2
from camera import *

turtle = Turtlebot(rgb=True, pc=True, depth=True)


def button_cb(msg):
    print('button cb')
    if msg.state == 0:
        rgb = turtle.get_rgb_image()
        hsv = rgb_to_hsv(rgb)
        print("HSV")
        print(hsv[int(hsv.shape[0]/2),int(hsv.shape[1]/2),:])
        # print("RGB")
        # print(rgb[int(rgb.shape[0]/2),int(rgb.shape[1]/2),:])
        img_threshold(hsv)


def main():
    turtle.register_button_event_cb(button_cb)

    rate = Rate(10)
    window_rgb = Window("rgb")
    window_bool = Window("bool")

    while not turtle.is_shutting_down():
        rate.sleep()

        rgb = turtle.get_rgb_image()
        hsv = rgb_to_hsv(rgb)
        img = bool_to_rgb(img_threshold(hsv))
        window_rgb.show(rgb)
        window_bool.show(img)


if __name__ == '__main__':
    main()
