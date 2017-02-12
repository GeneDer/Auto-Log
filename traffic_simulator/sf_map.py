"""
Road model for the San Francisco roads
"""
from PIL import Image
import random


class Road:
    def __init__(self, road_type):
        """
        Each road object is one pixel, they can be
        one of the 4 types:
        none road, small road, big road, and free way
        Each of them also counts their current capacity
        and number of cars exited in this iteration.
        """
        self.road_type = road_type
        self.cars = 0
        self.exit_cars = 0


class SFMap:
    def __init__(self):
        """
        SFMap is an object that represents the roads in
        San Francisco. It iterates throguh each pixel and
        determines the road type. The corresponding road
        is then created.
        """
        sf_map = Image.open('sf_map.png')
        sf_map = sf_map.convert('RGB') # conversion to RGB
        sf_map_pixel = sf_map.load()

        road1 = Image.open('1.png')
        road2 = Image.open('2.png')
        road3 = Image.open('3.png')

        road1 = road1.convert('RGB')
        road2 = road2.convert('RGB')
        road3 = road3.convert('RGB')

        data1 = road1.load()
        data2 = road2.load()
        data3 = road3.load()

        # map_pixels is the 2d list that contained each road object
        # road_list is easy lookup for the a driveable road
        self.map_pixels = []
        self.road_list = []
        for i in xrange(sf_map.size[0]):
            self.map_pixels.append([])
            for j in xrange(sf_map.size[1]):
                if sf_map_pixel[i,j] == data1[0,0]:
                    self.map_pixels[i].append(Road(1))
                    if i > 0 and i < 899 and j > 0 and j < 899:
                        self.road_list.append((i,j))
                elif sf_map_pixel[i,j] == data2[0,0]:
                    self.map_pixels[i].append(Road(2))
                    if i > 0 and i < 899 and j > 0 and j < 899:
                        self.road_list.append((i,j))
                elif sf_map_pixel[i,j] == data3[0,0]:
                    self.map_pixels[i].append(Road(3))
                    if i > 0 and i < 899 and j > 0 and j < 899:
                        self.road_list.append((i,j))
                else:
                    self.map_pixels[i].append(Road(0))


    def random_location(self):
        """
        This function helps to generate a random location
        for a new car to spawn. It randomly pick a driveable
        location, increments the capacity, and returns the location.
        """
        idx = random.randint(0, len(self.road_list) - 1)
        loc = self.road_list[idx]
        self.map_pixels[loc[0]][loc[1]].cars += 1
        return loc


    def check_location_cars(self, loc):
        """
        This function is used by move_location for checking
        if there are extra capacity on a given location to host
        another car. The maximum capacity is calculated as five
        times of road_type.
        """
        current_cars = self.map_pixels[loc[0]][loc[1]].cars
        max_cars = self.map_pixels[loc[0]][loc[1]].road_type*5
        if current_cars <= max_cars:
            return True
        else:
            return False


    def check_location_exit_cars(self, loc):
        """
        This function is used by move_location for checking
        if there are extra capacity on a given location to exit
        another car. The maximum capacity is calculated as two
        times of road_type.
        """
        current_exit_cars = self.map_pixels[loc[0]][loc[1]].exit_cars
        max_exit_cars = self.map_pixels[loc[0]][loc[1]].road_type*2
        if current_exit_cars <= max_exit_cars:
            return True
        else:
            return False

    
    def move_location(self, current_location, pervious_location):
        """
        This function takes the current_location and check all 
        nine neighboring location for a car move location. The
        can not travel back. The new location is randomly picked
        within the possible locations. If no possible location,
        the car will stay in place.
        """
        if check_location_exit_cars(current_location):
            possible_location = []
            locations_to_check = [(-1, -1), (0, -1), (1, -1),
                                  (-1, 0), (1, 0),
                                  (-1, 1), (0, 1), (1, 1)]
            for location_offset in locations_to_check:
                tmp_location = (current_location[0] + location_offset[0],
                                current_location[1] + location_offset[1])
                if tmp_location != pervious_location and \
                   self.check_location(tmp_location):
                    possible_location.append(tmp_location)
                    
            if len(possible_location) == 0:
                return (current_location,
                        self.map_pixels[current_location[0]][current_location[1]].road_type,
                        self.map_pixels[current_location[0]][current_location[1]].cars)
            else:
                new_location = random.choice(possible_location)
                self.map_pixels[new_location[0]][new_location[1]].cars += 1
                self.map_pixels[current_location[0]][current_location[1]].cars -= 1
                self.map_pixels[current_location[0]][current_location[1]].exit_cars += 1
                return (new_location,
                        self.map_pixels[new_location[0]][new_location[1]].road_type,
                        self.map_pixels[new_location[0]][new_location[1]].cars)
        else:
            return (current_location,
                    self.map_pixels[current_location[0]][current_location[1]].road_type,
                    self.map_pixels[current_location[0]][current_location[1]].cars)

        
            
    def reset_exit_cars(self):
        """
        After each iteration, the exit cars on each road block
        need to be reset to 0. This method is used to reset
        exit_cars in all driveable roads.
        """
        for road in self.road_list:
            self.map_pixels[road[0]][road[1]].exit_cars = 0
                
    
    def remove_car(self, location):
        """
        This function help to remove the car on a given road.
        It is needed for the respawn new car to work. If the
        old car is not being removed and new car keep spawn,
        the simulator will only produce 0 speed everywhere.
        """
        self.map_pixels[location[0]][location[1]].cars -= 1
