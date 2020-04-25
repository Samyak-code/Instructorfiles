"""
Copyright Harvey Mudd College
MIT License
Fall 2019

Lab 3 - Depth Camera
"""

################################################################################
# Imports
################################################################################

import sys

sys.path.insert(0, "../../library")
from racecar_core import *
import racecar_utils as rc_utils

rospy.init_node("racecar")
import cv2 as cv
import numpy as np


################################################################################
# Global variables
################################################################################

rc = Racecar()

# >> Variables
speed = 0.0  # The current speed of the car
angle = 0.0  # The current angle of the car's wheels
driving_forward = True  # Used when wall parking to denote current driving direction

# >> Constants (must be tuned)
# 1. Safety stop constants
STOP_DISTANCE = 500  # Stop if the car is this close to the wall (in mm)

# 2. Cone park constants
MIN_CONTOUR_SIZE = 30  # The smallest contour we will recognize as a valid contour
ORANGE = ((20, 50, 50), (60, 255, 255))  # The HSV range for the color orange
CONE_DISTANCE = 500  # Distance to stop away from the cone (in mm)

# 3. Wall park constants
# The left and right orientation points used to align the car with the wall
LEFT_POINT = (round(rc.camera.get_width() * 0.35), rc.camera.get_height() // 2)
RIGHT_POINT = (round(rc.camera.get_width() * 0.65), rc.camera.get_height() // 2)
WALL_DISTANCE = 500  # Distance to park away from the wall
MAX_DIF_PERCENT = 10  # Maximum allowed % difference between reference point distances
ALIGN_SPEED = 0.4  # Speed to use when aligning


################################################################################
# Functions
################################################################################


def start():
    """
    This function is run once every time the start button is pressed
    """
    global speed
    global angle

    # Initialize variables
    speed = 0
    angle = 0

    # Set initial driving speed and angle
    rc.drive.set_speed_angle(speed, angle)

    # Set update_slow to refresh every half second
    rc.set_update_slow_time(0.5)

    # Print start message
    print(
        ">> Lab 3 - Depth Camera\n"
        "\n"
        "Controlls:\n"
        "   Right trigger = accelerate forward\n"
        "   Left trigger = accelerate backward\n"
        "   Left joystick = turn front wheels\n"
        "   A button = print current speed and angle\n"
        "   B button = print contour center and area"
    )


def update():
    """
    After start() is run, this function is run every frame until the back button
    is pressed
    """
    global speed
    global angle

    if rc.controller.is_down(rc.controller.Button.LB):
        cone_park()
    elif rc.controller.is_down(rc.controller.Button.RB):
        wall_park()
    else:
        # Use the triggers to control the car's speed
        forwardSpeed = rc.controller.get_trigger(rc.controller.Trigger.RIGHT)
        backSpeed = rc.controller.get_trigger(rc.controller.Trigger.LEFT)
        speed = forwardSpeed - backSpeed

        # Calculate center distance
        depth_image = rc.camera.get_depth_image()
        center_distance = rc_utils.get_center_distance(depth_image)

        # Stop if the car is about to hit something
        if center_distance < STOP_DISTANCE and speed > 0:
            speed = 0

        # Use the left joystick to control the angle of the front wheels
        angle = rc.controller.get_joystick(rc.controller.Joystick.LEFT)[0]

    rc.drive.set_speed_angle(speed, angle)

    # Print the current speed and angle when the A button is held down
    if rc.controller.was_pressed(rc.controller.Button.A):
        print("Speed:", speed, "Angle:", angle)

    # TODO: When the left bumper (LB) is pressed, drive up to the closest cone
    # and stop six inches in front of it.  Your approach should use both color
    # and depth information and should work with cones of varying size.  You may
    # wish to reference lab 2.

    # TODO: When the right bumper (RB) is pressed, slalom through a line of cones
    # using color and/or depth images.


def update_slow():
    """
    After start() is run, this function is run at a constant rate that is slower
    than update().  By default, update_slow() is run once per second
    """
    # To help debug, update_slow does the following:
    # 1. Prints a line of ascii text to the console denoting the area of the
    #    contour and where the car sees the line
    # 2. Shows the current image to the screen with the largest contour drawn
    #    on top in bright green

    depth_image = rc.camera.get_depth_image()

    if depth_image is None:
        print("No depth image found")
    else:
        # Calculate and print center depth
        center_depth = rc_utils.get_center_distance(depth_image)
        print("Depth at center: {} mm".format(center_depth))

        # Colorize and display the depth image to the screen
        colorized_depth = rc_utils.color_depth_image(depth_image)
        rc.display.show_image(colorized_depth)


def cone_park():
    """
    Drives toward the closest cone and parks at CONE_DISTANCE away
    """
    global speed
    global angle

    color_image = rc.camera.get_image()
    depth_image = rc.camera.get_depth_image()

    if color_image is None or depth_image is None:
        print("No image or depth image found in handle_cone")
        speed = 0
        angle = 0
        return

    # Find all of the orange contours
    contours = rc_utils.find_contours(color_image, ORANGE[0], ORANGE[1])

    # Assume the largest contour is the closest cone
    contour = rc_utils.get_largest_contour(contours, MIN_CONTOUR_SIZE)

    if contour is None:
        speed = 0
        angle = 0
        return

    # Use proportional control based on the contour center to set angle
    contour_center = rc_utils.get_center(contour)
    angle = rc_utils.remap_range(contour_center[1], 0, rc.camera.get_width(), -1, 1)

    # Calculate the distance of the cone using the depth image
    cone_distance = rc_utils.get_average_distance(
        depth_image, contour_center[0], contour_center[1]
    )

    # Use proportional control based on cone distance to set speed
    speed = rc_utils.remap_range(
        cone_distance, CONE_DISTANCE, 2 * CONE_DISTANCE, 0.0, 1.0
    )
    speed = max(-1.0, min(1.0, speed))

    # If speed is close to 0, round to 0 to avoid jittering
    if -0.2 < speed < 0.2:
        speed = 0


def wall_park():
    """
    Aligns perpendicularly with the closest wall and parks at WALL_DISTANCE away
    """
    global speed
    global angle
    global driving_forward

    # Calculate the distances of the left and right reference points
    depth_image = rc.camera.get_depth_image()
    left_distance = rc_utils.get_average_distance(
        depth_image, LEFT_POINT[0], LEFT_POINT[1]
    )
    right_distance = rc_utils.get_average_distance(
        depth_image, RIGHT_POINT[0], RIGHT_POINT[1]
    )

    # Calculate the percentage difference of these distances
    average_distance = right_distance + left_distance
    dif_percent = (right_distance - left_distance) / average_distance

    if -MAX_DIF_PERCENT < dif_percent < MAX_DIF_PERCENT:
        # If dif_percent is close enough to aligned, drive straight to WALL_DISTANCE
        speed = rc_utils.remap_range(average_distance, 0, WALL_DISTANCE, -1.0, 0.0)
        speed = max(-1.0, min(1.0, speed))

        # If speed is close to 0, round to 0 to avoid jittering
        if -0.2 < speed < 0.2:
            speed = 0
    elif driving_forward:
        # Drive forward and turn opposite of dif_percent to reduce the difference
        angle = -dif_percent
        speed = ALIGN_SPEED

        # If we are getting to close to the wall, back up instead
        if average_distance < WALL_DISTANCE:
            driving_forward = False
    else:
        # Drive backward and turn the opposite way (since steering is reversed)
        angle = dif_percent
        speed = -ALIGN_SPEED

        # Once we back up enough, start driving forward again
        if average_distance > 2 * WALL_DISTANCE:
            driving_forward = True


################################################################################
# Do not modify any code beyond this point
################################################################################

if __name__ == "__main__":
    rc.set_start_update(start, update, update_slow)
    rc.go()
