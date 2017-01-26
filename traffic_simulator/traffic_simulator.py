"""
This script is used to mock the traffic data in scaled down version of
San Francisco. The road map is taken from Google Maps. Each car will
randomly occupy a space on the road and each road space has a capacity
of cars that can be traveling. Each car will be traveling for a certain
distance. Once the full distance is traveled, it will be removed and restart
with a new location. 
"""

import random
from sf_map import SFMap
from car import Car

import random
import sys

from kafka.client import SimpleClient
from kafka.producer import KeyedProducer

class Producer(object):

    def __init__(self, addr):
        self.client = SimpleClient(addr)
        self.producer = KeyedProducer(self.client)

    def produce_msgs(self, number_of_cars):
        # load SFMap test
        my_map = SFMap()

        # generat cars according to the number_of_cars
        my_cars = []
        for i in xrange(number_of_cars):
            my_cars.append(Car(random.randint(1,100), my_map.random_location()))

        # convert the pixel into lat and long
        def location_convertor(location):
            x = (122.470891 - 122.391583)/(800 - 338)
            y = -(37.813187 - 37.690489)/(900)
            x0 = -122.478101 - 295*x
            y0 = 37.813187

            return (y0 + location[1]*y, x0 + location[0]*x)

        time_field = 0
        while True:
            time_field += 1
            for car_id in xrange(number_of_cars):
                #lat, lon = location_convertor(my_cars[j].current_location)

                # convert the indices, 10 x 10 grid for now
                grid_id = str(my_cars[car_id].current_location[0]/90 +\
                          10*(my_cars[car_id].current_location[1]/90))
                speed_field = my_cars[car_id].speed
                str_fmt = "{};{};{};{}"
                message_info = str_fmt.format(grid_id,
                                              car_id,
                                              time_field,
                                              speed_field)
                print message_info
                self.producer.send_messages('auto_log', grid_id, message_info)
                
                new_location = my_map.move_location(my_cars[car_id].current_location,
                                                    my_cars[car_id].pervious_location)
                if new_location[0] > 0 and new_location[0] < 899 and \
                   new_location[1] > 0 and new_location[1] < 899:
                    new_speed = my_cars[car_id].speed + random.randint(-10, 10)
                    if new_speed < 1:
                        new_speed = 1
                    my_cars[car_id].move(new_speed, new_location)
                else:
                    my_cars[car_id] = Car(random.randint(1,100), my_map.random_location())


if __name__ == "__main__":
    args = sys.argv
    ip_addr = str(args[1])
    number_of_cars = int(args[2])
    prod = Producer(ip_addr)
    prod.produce_msgs(number_of_cars)
