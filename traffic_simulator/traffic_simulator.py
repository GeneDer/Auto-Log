"""
This script is used to mock the traffic data in scaled down version of
San Francisco. The road map is taken from Google Maps. Each car will
randomly occupy a space on the road and each road space has a capacity
of cars that can be traveling. Each car will be traveling for a certain
distance. Once the full distance is traveled, it will be removed. 
"""

import random
from sf_map import SFMap

my_map = SFMap()
print len(my_map.map_pixels)
print my_map.map_pixels[0][0].road_type
print my_map.map_pixels[90][252].road_type
