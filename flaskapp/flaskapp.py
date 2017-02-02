from flask import Flask, request, g, render_template, redirect, url_for, jsonify, abort
import redis
import numpy

app = Flask(__name__)
app.config.from_object(__name__)

def query_all_data():
    with open("/home/ubuntu/Auto-Log/flaskapp/key.txt", 'r') as key_file:
        ip = key_file.readline().strip()
        password = key_file.readline().strip()
    
    r = redis.StrictRedis(host=ip,
                          port=6379,
                          password=password)
    
    data = {}
    max_volume = 1
    for key in r.scan_iter():
        val = r.get(key).split(';')
        data[key] = {"average speed": val[0],
                     "volume": val[1]}
        if int(val[1]) > max_volume:
            max_volume = int(val[1])
    return data, max_volume


# convert the pixel into lat and long
def location_convertor(location):
    x = (122.470891 - 122.391583)/(800 - 338)
    y = -(37.813187 - 37.690489)/(900)
    x0 = -122.478101 - 295*x
    y0 = 37.813187

    return (y0 + location[1]*y, x0 + location[0]*x)

def get_colors(current_vol, max_vol):
    color_level = 255*current_vol/max_vol
    red = hex(color_level)[2:]
    if len(red) == 1:
        red = '0' + red
    blue = hex(255 - color_level)[2:]
    if len(blue) == 1:
        blue = '0' + blue
    color = "#%s00%s"%(red, blue)
    return color

@app.route('/')
def index():
    data, max_volume = query_all_data()
    
    grids = []                 
    for i in xrange(0,901,18):
        for j in xrange(0,901,18):
            grid_id = str(50*(i/18) + j/18)
            lat1, lon1 = location_convertor((i,j))
            lat2, lon2 = location_convertor((i,j + 18))
            lat3, lon3 = location_convertor((i + 18,j + 18))
            lat4, lon4 = location_convertor((i + 18,j))
            if grid_id in data:
                speed = "average speed: %s"%data[grid_id]["average speed"]
                volume = "traffic volume: %s"%data[grid_id]["volume"]
                grids.append([lat1, lon1, lat2, lon2,
                              lat3, lon3, lat4, lon4,
                              speed, volume,
                              get_colors(int(data[grid_id]["volume"]),
                                         max_volume)])
            else:
                grids.append([lat1, lon1, lat2, lon2,
                              lat3, lon3, lat4, lon4,
                              "average speed: NA", "traffic volume: 0",
                              get_colors(0, max_volume)])

    return render_template("index.html", grids=grids)


@app.route('/api')
def api():
    data, volume = query_all_data()
    return jsonify(data)

if __name__ == '__main__':
    app.run()
