#start with imports, ie: import the wrapper
import TMMC_Wrapper
import rclpy
import numpy as np
import math


#start ros
if not rclpy.ok():
    rclpy.init()

TMMC_Wrapper.is_SIM = False
if not TMMC_Wrapper.is_SIM:
    #specify hardware api
    TMMC_Wrapper.use_hardware()
    
if not "robot" in globals():
    robot = TMMC_Wrapper.Robot()

#debug messaging 
print("running main")

#start processessssssssss
robot.start_keyboard_control()   #this one is just pure keyboard control

rclpy.spin_once(robot, timeout_sec=0.1)



# robot.set_cmd_vel(10,10,60)

#run the keyboard control functions
try:
    print("Listening for keyboard events. Press keys to test, Ctrl C to exit")
    while True: 
        rclpy.spin_once(robot, timeout_sec=0.1)
        scan = robot.checkScan()
        min_dist, min_angle = robot.detect_obstacle(scan.ranges)
        print(min_dist)
        print(min_angle)
        if min_dist >= 0 :
                # camera side = 90/-90
                print("OBSTACLE DETECTED")
                if min_angle <= 45 and min_angle >=-45:
                    print("MOVING BACKWARDS")
                    TMMC_Wrapper.set_speed(0)
                    robot.set_cmd_vel(-0.8, 0, 0.3)
                    robot.set_cmd_vel(0.0, 1, 2.7)
                    robot.set_cmd_vel(0.0,0.0,1)
                
                    # robot.set_cmd_vel(0.2, 0.0, 1)
                # elif min_angle >= 135 or min_angle <=-135:
                #     # robot.set_cmd_vel(0.2, 0.0, 0.5)
                #     print("MOVING FORWARDS")
        else:
            TMMC_Wrapper.set_speed(0.5)
except KeyboardInterrupt:
    print("keyboard interrupt receieved.Stopping...")
finally:
    #when exiting program, run the kill processes
    robot.stop_keyboard_control()
    robot.destroy_node()
    rclpy.shutdown()




