from flask import Flask, request, g, render_template, redirect, url_for, jsonify, abort
import redis

app = Flask(__name__)
app.config.from_object(__name__)

@app.route('/')
def index():
    return render_template("index.html")

@app.route('/api')
def api():
    with open("key.txt", 'r') as o:
        for i in o:
            password = i.strip()
    
    r = redis.StrictRedis(host='52.25.7.221',
                          port=6379,
                          password=password)
    
    j = {}
    count = 0
    
    for key in r.scan_iter():
        key = r.get(key).split(';')
        j[key] = {"average speed": val[0],
                  "volume": val[1]}
        count += 1
    print count
        
    
    return jsonify(data)

if __name__ == '__main__':
    app.run()
