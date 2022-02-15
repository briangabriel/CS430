from picar_4wd.pwm import PWM
from picar_4wd.pin import Pin
from picar_4wd.servo import Servo
from picar_4wd.ultrasonic import Ultrasonic

from statistics import mean

import math
import time

servo = Servo(PWM("P0"), offset=-9)
us = Ultrasonic(Pin('D8'), Pin('D9'))

def detect():
    obstacle_map = map()
    for point in obstacle_map:
        print(point)
        if point[0] <= 10 and point[0] >= -10:
            return True
    return False

def scan_front():
    servo.set_angle(0)
    distance = us.get_distance()
    print(distance)
    return distance < 30 and distance > -2

def map():
    ang = -90
    num_of_readings=18
    incr=180/num_of_readings

    num_samples = 5
    points = []

    while ang < 90:
        samples = [0] * num_samples

        servo.set_angle(ang)

        #this sleep is CRITICAL for accurate messurements, without it it would read while the servo is moving!
        time.sleep(0.5)

        for i in range(num_samples):
            samples[i] = us.get_distance()
            
        #attempt to clean up the data
        samples.remove(max(samples))
        samples.remove(min(samples))
        dist = mean(samples)

        #change the angle direction to match the grid
        normal_ang = -1 * (ang + 1)

        #trig to the rescue
        y = int( dist*math.cos(math.pi*(normal_ang/180)) / 10 )
        x = int (dist*math.sin(math.pi*(normal_ang/180)) / 10 )

        # print(ang, dist, x, y)

        ang += incr
        
        # ignore any outliers
        if dist < 0 or dist > 30:
            continue

        points.append((x,y))

    #print(points)
    servo.set_angle(-1)
    time.sleep(0.5)
    return points

if __name__ == '__main__':
  map()