import time
import pynput.keyboard
import threading

class Car:

    class Sensor_motor:
        def __init__(self, angular_velocity):
            self.motor = True
            self.angular_velocity = angular_velocity
            self.tn = 0
            self.tn_sum = 0
            self.time_start = 0
            self.radius = 1
            self.gear_ratio_value = 1

        def switch(self):
            self.motor = not bool(self.motor)

        # def angle(self, angular_velocity, tn):
        #     self.angle =  self.angular_velocity * self.tn

        def indicate(self):
            if(self.motor):
                return('Turning Right')
            else:
                return('Turning Left')

        def gear_ratio(self):
            angle = self.angular_velocity * self.tn
            ratio = 1
            return ratio

        def gear_ratio_modified(self):
            return self.gear_ratio() * self.motor

        def start_timer(self):
            self.time_start = time.time()

        def first_touch_time(self):
            time_now = time.time() - self.time_start
            tn = time_now
            self.tn_sum += tn
            return(round(tn,3))

        def touch_time(self):
            if(self.tn_sum != 0):
                time_now = time.time() - self.time_start
                tn = time_now - 2 * self.tn_sum
                self.tn_sum += tn
                return(round(tn,3))
            else:
                return('[-]Error: Run first_get_time()')

        def get_tn_sum(self):
            return(self.tn_sum)


    def __init__(self):
        print('CAR READY [PRESS BACKSPACE TO BEGIN && PRESS SPACE TO DETECT LINE]')
        self.sensor_motor = self.Sensor_motor(5)
        self.no_touch_turn_count = 0
        self.t0 = 5
        self.t = 0
        self.keyboard_listener = pynput.keyboard.Listener(on_press=self.process_key_press)
        with self.keyboard_listener:
            self.keyboard_listener.join()



    def process_key_press(self, key):
        if(key == key.backspace):
            self.sensor_motor.start_timer()
            print('[+]Sensor On')
            self.t = threading.Timer(self.t0, self.first_no_touch_turn)
            self.t.start()

        elif(key == key.space and self.sensor_motor.time_start != 0):

            if(self.no_touch_turn_count%2==0):self.sensor_motor.switch()

            if(self.sensor_motor.tn_sum == 0):
                if(self.t!=0):self.t.cancel()
                tn = self.sensor_motor.first_touch_time()
                self.t = threading.Timer(tn+self.t0, self.no_touch_turn)
                self.t.start()
                self.no_touch_turn_count = 0
                print('[+]Line Detected  ' + 'tn:{}  Indicator:{}'.format(tn, self.sensor_motor.indicate()))

            else:
                if(self.t!=0):self.t.cancel()
                tn = self.sensor_motor.touch_time()
                self.t = threading.Timer(tn+self.t0, self.no_touch_turn)
                self.t.start()
                self.no_touch_turn_count = 0
                print('[+]Line Detected  ' + 'tn:{}  Indicator:{}'.format(tn, self.sensor_motor.indicate()))

    def first_no_touch_turn(self):
        tn = self.sensor_motor.first_touch_time()
        self.no_touch_turn_count += 1
        print('[+]Reached limit  ' + 'tn:{}  Indicator:{} (UNCHANGED)  Count:{}'.format(tn, self.sensor_motor.indicate(), self.no_touch_turn_count))
        self.t = threading.Timer(tn+self.t0, self.no_touch_turn)
        self.t.start()

    def no_touch_turn(self):
        tn = self.sensor_motor.touch_time()
        self.check_count()
        self.no_touch_turn_count += 1
        print('[+]Reached limit  ' + 'tn:{}  Indicator:{} (UNCHANGED)  Count:{}'.format(tn, self.sensor_motor.indicate(), self.no_touch_turn_count))
        self.t = threading.Timer(tn+self.t0, self.no_touch_turn)
        self.t.start()

    def check_count(self):
        if(self.no_touch_turn_count == 3):
            self.t.cancel()
            self.no_touch_turn_count = 0
            print('[-]Counter exceeded limit\n[-]Exiting...')
            exit()

car = Car()
