"""
This script is used to mock the traffic data in scaled down version of
San Francisco. The road map is taken from Google Maps. Each car will
randomly occupy a space on the road and each road space has a capacity
of cars that can be traveling. Each car will be traveling for a certain
distance. Once the full distance is traveled, it will be removed. 
"""

import random
from sf_map import SFMap
from car import Car

my_map = SFMap()
print len(my_map.map_pixels)
print my_map.map_pixels[0][0].road_type
print my_map.map_pixels[90][252].road_type

my_cars = []
for i in xrange(1000):
    my_cars.append(Car(i,(i*2, i*3)))

print my_cars[123].distance_to_end, my_cars[123].current_location
