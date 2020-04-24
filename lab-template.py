"""
Copyright Harvey Mudd College
MIT License
<Season> <Year>

Lab <n> - <Lab Title>
"""

################################################################################
# Imports
################################################################################

import sys

sys.path.insert(0, "../../library")
from racecar_core import *

rospy.init_node("racecar")


################################################################################
# Global variables
################################################################################

rc = Racecar()

################################################################################
# Functions
################################################################################


def start():
    """
    This function is run once every time the start button is pressed
    """
    pass


def update():
    """
    After start() is run, this function is run every frame until the back button
    is pressed
    """
    pass


def update_slow():
    """
    After start() is run, this function is run at a constant rate that is slower
    than update().  By default, update_slow() is run once per second
    """
    pass


################################################################################
# Do not modify any code beyond this point
################################################################################

if __name__ == "__main__":
    rc.set_start_update(start, update, update_slow)
    rc.go()
