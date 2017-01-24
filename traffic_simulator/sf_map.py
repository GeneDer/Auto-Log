"""
Road model for the San Francisco roads
"""
from PIL import Image
import random

class Road:
    def __init__(self, road_type):
        self.road_type = road_type
        self.cars = 0


class SFMap:
    def __init__(self):
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

        self.map_pixels = []
        self.road_list = []
        for i in xrange(sf_map.size[0]):
            self.map_pixels.append([])
            for j in xrange(sf_map.size[1]):
                if self.sf_map_pixel[i,j] == data1[0,0]:
                    self.map_pixels[i].append(Road(1))
                    self.road_list.append((i,j))
                elif self.sf_map_pixel[i,j] == data2[0,0]:
                    self.map_pixels[i].append(Road(2))
                    self.road_list.append((i,j))
                elif self.sf_map_pixel[i,j] == data3[0,0]:
                    self.map_pixels[i].append(Road(3))
                    self.road_list.append((i,j))
                else:
                    self.map_pixels[i].append(Road(0))


    def random_location(self):
        idx = random.randint(0, len(self.road_dict) - 1)
        loc = self.road_list[idx]
        self.map_pixels[loc[0]][loc[1]].cars += 1
        return loc


    def check_location(self, loc):
        if self.map_pixels[loc[0]][loc[1]].cars < \
           self.map_pixels[loc[0]][loc[1]].road_type*5:
            return True
        else:
            return False

    
    def move_location(self, current_location, pervious_location):
        possible_location = []
        locations_to_check = [(-1, -1), (0, -1), (1, -1),
                              (-1, 0), (1, 0),
                              (-1, 1), (0, 1), (1, 1)]
        for location_offset in locations_to_check:
            tmp_location = (current_location[0] + location_offset[0],
                               current_location[1] + location_offset[1])
            if check_location(tmp_location) and \
               tmp_location != pervious_location:
                possible_location.append(tmp_location)
                
        if len(possible_location) == 0:
            return current_location
        else:
            new_location = random.choice(possible_location)
            self.map_pixels[new_location[0]][new_location[1]].cars += 1
            self.map_pixels[current_location[0]][current_location[1]].cars += 1
            return new_location
        
            


        
