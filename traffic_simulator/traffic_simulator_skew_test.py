"""
This script is used to mock the traffic data in a scaled down version of
San Francisco. The road map is taken from Google Maps. Each car will
randomly occupy a space on the road and each road space has a capacity
of cars that can be traveling. Each car will be traveling for a certain
distance. Once the full distance is traveled, it will be removed and new
car will respawn in a new location. 
"""

import random
from sf_map import SFMap
from car import Car

import numpy as np
import random
import sys

from kafka.client import SimpleClient
from kafka.producer import KeyedProducer

class Producer(object):

    def __init__(self, addr):
        # setup connection to the kafka in order to send messages
        self.client = SimpleClient(addr)
        self.producer = KeyedProducer(self.client)

    def produce_msgs(self, number_of_cars, session_id):
        # load SFMap test
        my_map = SFMap()

        # generate cars according to the number_of_cars
        # each car is traveled for random distance from 1 to 100
        my_cars = []
        max_car_id = number_of_cars
        for i in xrange(number_of_cars):
            car_id = i + number_of_cars*(session_id - 1)
            my_cars.append(Car(car_id, random.randint(1,100), my_map.random_location()))

        # generate new speed according to the current speed and
        # the road capacity
        def generate_new_speed(current_speed, road_type, number_of_car):
            speed_offset = abs(np.random.normal(0,5))
            if number_of_car*2 > road_type*5:
                current_speed -= speed_offset
                if current_speed < 0:
                    current_speed = 0
            else:
                current_speed += speed_offset
                if road_type == 1:
                    if current_speed > 30:
                        current_speed = 30
                elif road_type == 2:
                    if current_speed > 50:
                        current_speed = 50
                elif current_speed > 70:
                    current_speed = 40
            return current_speed

        # convert the indices into lat and long
        def location_convertor(location):
            x = (122.470891 - 122.391583)/(800 - 338)
            y = -(37.813187 - 37.690489)/(900)
            x0 = -122.478101 - 295*x
            y0 = 37.813187

            lat = "%.6f"%(y0 + location[1]*y)
            lon = "%.6f"%(x0 + location[0]*x)

            return lat, lon

        # generate new car with given id
        def respawn_new_car(car_id):
            new_car = Car(car_id, random.randint(1,100), (random.randint(0,18),
                                                          random.randint(0,18)))
            return new_car
            
        # while loop to iterate the simulator continuously 
        time_field = 0
        while True:
            time_field += 1
            my_map.reset_exit_cars()
            for idx in xrange(number_of_cars):
                lat, lon = location_convertor(my_cars[idx].current_location)
                grid_id = str(50*(my_cars[idx].current_location[1]/18) +\
                          my_cars[idx].current_location[0]/18)
                car_id = my_cars[idx].car_id
                
                speed_field = my_cars[idx].speed
                str_fmt = "{};{};{};{};{}"
                message_info = str_fmt.format(lat,
                                              lon,
                                              car_id,
                                              time_field,
                                              speed_field)
                #print message_info
                self.producer.send_messages('auto_log', grid_id, message_info)
                
                new_location = (random.randint(0,18), random.randint(0,18))
                
                if new_location == my_cars[idx].current_location:
                    new_speed = 0
                else:
                    new_speed = generate_new_speed(my_cars[idx].speed,
                                                   road_type,
                                                   number_of_car)
                my_cars[idx].move(new_speed, new_location)
                if my_cars[idx].distance_to_end == 0:
                    my_cars[idx] = respawn_new_car(my_cars[idx].car_id)


if __name__ == "__main__":
    args = sys.argv
    session_id = int(args[1])
    ip_addr = str(args[2])
    number_of_cars = int(args[3])
    prod = Producer(ip_addr)
    prod.produce_msgs(number_of_cars, session_id)
