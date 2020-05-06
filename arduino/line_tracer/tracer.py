from tracer_modules import *
import time
import pynput.keyboard

# time_start = 0

def start_timer():
    time_start = time.time()
    time.sleep(1)
    time_end = time.time()
    print(time_end - time_start)
    time.sleep(1)
    time_end2 = time.time()
    print(time_end2 - time_start)

# start_timer()

# timer = Time_Counter()

# timer.start_timer()
# print(timer.get_tn_sum())
# time.sleep(1)
# print(timer.first_get_time())
# print('sum', timer.get_tn_sum())
# time.sleep(2)
# print(timer.get_time())
# print('sum', timer.get_tn_sum())
# time.sleep(2)
# print(timer.get_time())
# print('sum', timer.get_tn_sum())
# time.sleep(2)
# print(timer.get_time())
# print('sum', timer.get_tn_sum())

def process_key_press(key):
    if(key == key.space):
        print('Space key pressed')

# keyboard_listener = pynput.keyboard.Listener(on_press=process_key_press)
# with keyboard_listener:
#     keyboard_listener.join()
#
# class Sensor_motor:
#     def __init__(self, angular_velocity, tn):
#         self.motor = 1
#         self.angular_velocity = angular_velocity
#         self.tn = tn
#         self.time_counter = Time_Counter()
#
#     def switch(self):
#         self.motor = self.motor * -1
#
#     def angle(self, angular_velocity, tn):
#         return self.angular_velocity * self.tn
#
#     def show(self):
#         if(self.motor == 1):
#             return('Turning Right')
#         else:
#             return('Turning Left')
#
#     def gear_ratio(self):
#         # parameter : angle
#         return ratio
#
#     def gear_ratio_modified(self):
#         return self.gear_ratio() * self.motor
# class Time_Counter:
#     def __init__(self):
#         self.tn_sum = 0
#         self.time_start = 0
#
#     def start_timer(self):
#         self.time_start = time.time()
#
#     def first_get_time(self):
#         time_now = time.time() - self.time_start
#         tn = time_now
#         self.tn_sum += tn
#         return(tn)
#
#     def get_time(self):
#         if(self.tn_sum != 0):
#             time_now = time.time() - self.time_start
#             tn = time_now - 2 * self.tn_sum
#             self.tn_sum = self.tn_sum + tn
#             return(tn)
#         else:
#             return('Implement first_get_time')
#
#     def get_tn_sum(self):
#         return(self.tn_sum)

# def boo():
#     if(False):
#         return('Turning Right')
#     else:
#         return('Turning Left')
#
# print(boo())

car = Car()
