from enum import IntEnum


class State(IntEnum):
    search = 0
    obstacle = 1
    approach = 2
    stop = 3


cur_state: State = State.search


def start():
    """
    This function is run once every time the start button is pressed
    """
    global cur_state
    cur_state = State.search


def update():
    """
    After start() is run, this function is run every
    frame until the back button is pressed
    """
    global cur_state

    speed: float = 0
    angle: float = 0
    if cur_state == State.search:
        # Set speed and angle to "wander"

        if cone_identified:
            cur_state = State.approach

        if about_to_hit_something:
            cur_state = State.obstacle

    elif cur_state == State.obstacle:
        # Set speed and angle to avoid obstacle

        if obstacle_avoided:
            cur_state = State.search

    elif cur_state == State.approach:
        # Set angle to face cone and approach

        if next_to_cone:
            cur_state = State.stop

        if not cone_identified:
            cur_state = State.search

    elif cur_state == State.stop:
        speed = 0
        angle = 0

    rc.drive.set_speed_angle(speed, angle)
