"""
Road model for the San Francisco roads
"""
from PIL import Image


class Road:
    def __init__(self, road_type):
        self.road_type = road_type
        self.cars = []


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
        for i in xrange(sf_map.size[0]):
            self.map_pixels.append([])
            for j in xrange(sf_map.size[1]):
                if sf_map_pixel[i,j] == data1[0,0]:
                    self.map_pixels[i].append(Road(1))
                elif sf_map_pixel[i,j] == data2[0,0]:
                    self.map_pixels[i].append(Road(2))
                elif sf_map_pixel[i,j] == data3[0,0]:
                    self.map_pixels[i].append(Road(3))
                else:
                    self.map_pixels[i].append(Road(0))



        
