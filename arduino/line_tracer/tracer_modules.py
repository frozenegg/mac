import time
import pynput.keyboard
import threading
import numpy as np

class Car:

    class Sensor_motor:                             # sensor module initial setup
        def __init__(self, gear_extent):
            self.motor = True
            self.tn = 0                             # time to touch
            self.t0 = 5                             # full stroke time
            self.tn_sum = 0                         # accumulation of tn
            self.time_start = 0                     # time when sensor_motor started
            self.radius = 1                         # radius of the sensors from centre
            self.gear_ratio_value = 1               # initial gear ratio
            self.gear_extent = gear_extent          # how much the car would turn  correlated with tn

        def switch(self):                           # left/right turn switch
            self.motor = not bool(self.motor)

        def indicate(self):                         # indicates which way to turn
            if(self.motor):
                return('Turning Right')
            else:
                return('Turning Left ')

        def sigmoid(self, x):                       # sigmoid function
            return np.exp(x) / (np.exp(x) + 1)

        def gear_ratio(self, tn):                   # returns gear ratio in the form of fraction
            time_ratio = tn / self.t0
            gear_ratio = self.sigmoid(time_ratio * self.gear_extent)
            return gear_ratio

        def gear_ratio_modified(self, tn):          # modifes gear ratio from fraction to ratio and also implements right/left correlation
            if(self.motor):
                modified_ratio = self.gear_ratio(tn)
            else:
                modified_ratio = self.gear_ratio(tn) ** -1
            right_gear = round(1 / (modified_ratio + 1), 3)
            left_gear = round(modified_ratio / (modified_ratio + 1), 3)
            return right_gear, left_gear

        def start_timer(self):                      # starts timer
            self.time_start = time.time()

        def first_touch_time(self):                 # returns when sensor detects line for the first time
            time_now = time.time() - self.time_start
            tn = time_now
            self.tn_sum += tn
            return(round(tn,3))

        def touch_time(self):                       # returns when sensor detects line after the first move
            if(self.tn_sum != 0):
                time_now = time.time() - self.time_start
                tn = time_now - 2 * self.tn_sum
                self.tn_sum += tn
                return(round(tn,3))
            else:
                print('[-]Error: Run first_get_time()\n[-]Exiting...')
                exit()

        def get_tn_sum(self):
            return(self.tn_sum)


    def __init__(self):                             # car module initial setup
        print('CAR READY [PRESS BACKSPACE TO BEGIN && PRESS LEFT-SHIFT TO DETECT LINE]')
        self.sensor_motor = self.Sensor_motor(5)
        self.no_touch_turn_count = 0
        self.t = 0
        self.keyboard_listener = pynput.keyboard.Listener(on_press=self.process_key_press)
        with self.keyboard_listener:
            self.keyboard_listener.join()



    def process_key_press(self, key):               # activate functions when key is pressed
        if(key == key.backspace):                   # activate sensor module when backspace is pressed
            self.sensor_motor.start_timer()
            print('[+]Sensor On')
            self.t = threading.Timer(self.sensor_motor.t0, self.first_no_touch_turn)
            self.t.start()

        elif(key == key.shift and self.sensor_motor.time_start != 0):

            if(self.no_touch_turn_count%2==0):self.sensor_motor.switch()

            if(self.sensor_motor.tn_sum == 0):
                if(self.t!=0):self.t.cancel()
                tn = self.sensor_motor.first_touch_time()
                self.t = threading.Timer(tn+self.sensor_motor.t0, self.no_touch_turn)
                self.t.start()
                self.no_touch_turn_count = 0
                print('[+]Line Detected  ' + 'tn:{}  Indicator:{}  Speed Ratio:[{}:{}]'.format(tn, self.sensor_motor.indicate(), self.sensor_motor.gear_ratio_modified(tn)[0], self.sensor_motor.gear_ratio_modified(tn)[1]))

            else:
                if(self.t!=0):self.t.cancel()
                tn = self.sensor_motor.touch_time()
                self.t = threading.Timer(tn+self.sensor_motor.t0, self.no_touch_turn)
                self.t.start()
                self.no_touch_turn_count = 0
                print('[+]Line Detected  ' + 'tn:{}  Indicator:{}  Speed Ratio:[{}:{}]'.format(tn, self.sensor_motor.indicate(), self.sensor_motor.gear_ratio_modified(tn)[0], self.sensor_motor.gear_ratio_modified(tn)[1]))

    def first_no_touch_turn(self):
        tn = self.sensor_motor.first_touch_time()
        self.no_touch_turn_count += 1
        print('[+]Reached limit  ' + 'tn:{}  Indicator:{} (SPEED CONSISTENT)  Count:{}'.format(tn, self.sensor_motor.indicate(), self.no_touch_turn_count))
        self.t = threading.Timer(tn+self.sensor_motor.t0, self.no_touch_turn)
        self.t.start()

    def no_touch_turn(self):
        tn = self.sensor_motor.touch_time()
        self.check_count()
        self.no_touch_turn_count += 1
        print('[+]Reached limit  ' + 'tn:{}  Indicator:{} (SPEED CONSISTENT)  Count:{}'.format(tn, self.sensor_motor.indicate(), self.no_touch_turn_count))
        self.t = threading.Timer(tn+self.sensor_motor.t0, self.no_touch_turn)
        self.t.start()

    def check_count(self):
        if(self.no_touch_turn_count == 3):
            self.t.cancel()
            self.no_touch_turn_count = 0
            print('[-]Counter exceeded limit\n[-]Exiting...')
            exit()

car = Car()
