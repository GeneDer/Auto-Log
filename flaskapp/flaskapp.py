from flask import Flask, request, g, render_template, redirect, url_for, jsonify, abort
import redis
import numpy

app = Flask(__name__)
app.config.from_object(__name__)

def query_all_data():
    with open("key.txt", 'r') as o:
        for i in o:
            password = i.strip()
    
    r = redis.StrictRedis(host='52.25.7.221',
                          port=6379,
                          password=password)
    
    data = {}
    for key in r.scan_iter():
        val = r.get(key).split(';')
        data[key] = {"average speed": val[0],
                     "volume": val[1]}
    return data


# convert the pixel into lat and long
def location_convertor(location):
    x = (122.470891 - 122.391583)/(800 - 338)
    y = -(37.813187 - 37.690489)/(900)
    x0 = -122.478101 - 295*x
    y0 = 37.813187

    return (y0 + location[1]*y, x0 + location[0]*x)
        

@app.route('/')
def index():
    import time
    t0 = time.time()
    data = query_all_data()
    print time.time() - t0

    t0 = time.time()
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
                              speed, volume])
            else:
                grids.append([lat1, lon1, lat2, lon2,
                              lat3, lon3, lat4, lon4,
                              "average speed: NA", "traffic volume: 0"])
    print time.time() - t0
    return render_template("index.html", grids=grids)


@app.route('/api')
def api():    
    return jsonify(query_all_data())

if __name__ == '__main__':
    app.run()
