from camera_utils import CameraThread
from ev3_utils import MotorThread

import cv2

camera_thread = CameraThread()
motor_thread = MotorThread()

camera_thread.start()
motor_thread.start()
# threads = [camera_thread, motor_thread]
#
# for thread in threads:
#     thread.start()
from time import sleep
sleep(3)

def come_back():
    if camera_thread.centers_of_markers['green'][0] < camera_thread.coordinates_of_lines[1][1][0]:
        motor_thread.motor_l_speed, motor_thread.motor_r_speed = -20, -20
    elif camera_thread.centers_of_markers['green'][0] > camera_thread.coordinates_of_lines[1][1][0]:
        motor_thread.motor_l_speed, motor_thread.motor_r_speed = 0, 0

while True:
    print(camera_thread.centers_of_markers['green'][0], camera_thread.coordinates_of_lines[1][1][0])

    if camera_thread.centers_of_markers['green'][0] < camera_thread.coordinates_of_lines[1][1][0]:
        motor_thread.motor_l_speed, motor_thread.motor_r_speed = -20, -20
    elif camera_thread.centers_of_markers['green'][0] > camera_thread.coordinates_of_lines[1][1][0]:
        motor_thread.motor_l_speed, motor_thread.motor_r_speed = 0, 0
