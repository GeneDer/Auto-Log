from sf_map import SFMap
import matplotlib.pyplot as plt


def location_convertor(location):
    x = (122.470891 - 122.391583)/(800 - 338)
    y = -(37.813187 - 37.690489)/(900)
    x0 = -122.478101 - 295*x
    y0 = 37.813187

    return (y0 + location[1]*y, x0 + location[0]*x)


my_map = SFMap()
x = []
y = []
x2 = []
y2 = []
for i in xrange(900):
    for j in xrange(900):
        grid_id = str(50*(j/18) + i/18)
        if grid_id == "51":
            lat, lon = location_convertor((i,j))
            x2.append(lon)
            y2.append(lat)
            
        if my_map.map_pixels[i][j].road_type != 0:
            lat, lon = location_convertor((i,j))
            y.append(lat)
            x.append(lon)

plt.plot(x,y,'.')
plt.plot(x2,y2,'.')
plt.show()
        
