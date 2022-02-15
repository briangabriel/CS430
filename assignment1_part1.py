import picar_4wd as fc

import ultrasonic_scan

import time

turn_speed = 30
turn_duration = 1.1
forward_speed = 1

def main():
    
    while True:
        if ultrasonic_scan.scan_front():
            fc.stop()
            turn_left()
        
        fc.forward(forward_speed)

def turn_left():
    fc.turn_left(turn_speed)
    time.sleep(turn_duration)
    fc.stop()

if __name__ == "__main__":
    try:
        main()
    finally:
        fc.stop()