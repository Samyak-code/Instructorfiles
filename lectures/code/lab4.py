import math

# Example 1
def update():
    accel = rc.physics.get_linear_acceleration()
    ang_vel = rc.physics.get_angular_velocity()

    if accel[3] > 0.10:
        print("Kachow!")

    if ang_vel[0] > 0.25:
        rc.drive.stop()


# Example 2
foo = 0

def update():
    global foo

    ang_vel = rc.physics.get_angular_velocity()
    foo += ang_vel[1]

    if foo < math.pi / 2:
        rc.drive.set_speed_angle(1, 1)
    else:
        rc.drive.set_speed_angle(1, 0)
