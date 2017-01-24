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
import matplotlib.pyplot as plt
import time

t0 = time.time()

# load SFMap test
my_map = SFMap()
print len(my_map.map_pixels)
print my_map.map_pixels[0][0].road_type
print my_map.map_pixels[90][252].road_type

# load cars test
my_cars = []
for i in xrange(1000):
    my_cars.append(Car(i,(i*2, i*3)))

print my_cars[123].distance_to_end, my_cars[123].current_location

# car move test
my_car = Car(1000, my_map.random_location())
x = []
y = []
for i in xrange(1000):
    new_location = my_map.move_location(my_car.current_location,
                                        my_car.pervious_location)
    x.append(new_location[0])
    y.append(new_location[1])
    my_car.move(25, new_location)

##plt.plot(x,y)
##plt.plot(x[0], y[0], '*')
##plt.plot(x[len(x)-1], y[len(y)-1], '.')
##plt.show()

def location_convertor(location):
    x = (122.470891 - 122.391583)/(800 - 338)
    y = -(37.813187 - 37.690489)/(900)
    x0 = -122.478101 - 295*x
    y0 = 37.813187

    return (y0 + location[1]*y, x0 + location[0]*x)
    

# generat one million car driving data for 3600 steps test
my_cars = []
number_of_cars = 1000000
number_of_steps = 3600
for i in xrange(number_of_cars):
    my_cars.append(Car(random.randint(1,100), my_map.random_location()))
    
with open('traffic_data.txt', 'w') as out_file:
    for i in xrange(number_of_steps):
        for j in xrange(number_of_cars):
            lat, lon = location_convertor(my_cars[j].current_location)
            out_file.write("%s, %s, %s, %s, %s\n"%
                           (j, lat, lon, i, my_cars[j].speed))
            
            new_location = my_map.move_location(my_cars[j].current_location,
                                                my_cars[j].pervious_location)
            if new_location[0] > 0 and new_location[0] < 899 and \
               new_location[1] > 0 and new_location[1] < 899:
                my_cars[j].move(25, new_location)
            else:
                my_cars[j] = Car(random.randint(1,100), my_map.random_location())


print time.time() - t0
