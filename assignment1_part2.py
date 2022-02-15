import picar_4wd as fc
import time

import ultrasonic_scan
import object_detector

from collections import namedtuple

Coordinate = namedtuple('coordinate', ['x', 'y'])

current_loc = Coordinate(0,0)
destination_loc = Coordinate(0,8)

turn_speed = 25
turn_duration = 1.1
forward_speed = 1
forward_duration = 1

def main():   
    current_heading = 0
    current_loc = Coordinate(0,0)
    destination_loc = Coordinate(0,7)

    while current_loc != destination_loc:
        if object_detector.detect_labels():
            continue

        if ultrasonic_scan.detect() == True:
            current_heading = turn_right(current_heading)
            current_loc = move_forward(current_loc, current_heading)
            current_heading = turn_left(current_heading)
            continue

        print('Current Loc ' , current_loc)
        print('Current Heading ' , current_heading)

        if current_loc.y == destination_loc.y and current_heading == 0:
            if current_loc.x < 1:
                current_heading = turn_left(current_heading)
            else:
                current_heading = turn_right(current_heading)

        current_loc = move_forward(current_loc, current_heading)

    fc.stop()

def turn_left(heading):
    #Turns slower on the left, so increase the speed to compensate.
    fc.turn_left(turn_speed + 5)
    time.sleep(turn_duration)
    fc.stop()
    return heading + 90

def turn_right(heading):
    fc.turn_right(turn_speed)
    time.sleep(turn_duration)
    fc.stop()
    return heading - 90

def move_forward(location, heading):
    fc.forward(forward_speed)
    time.sleep(forward_duration)
    fc.stop()
    if heading == 0:
        return location._replace(y = location.y + 1)
        #current_y += 1
    elif heading == 90:
        return location._replace(x = location.x + 1)
    else:
        return location._replace(x = location.x - 1)


if __name__ == "__main__":
    try:
        main()
    finally:
        fc.stop()
