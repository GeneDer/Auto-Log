# Auto Log
Insight Data Engineering  
Session 2017A

## Motivation
Traffic is always a headache for getting from point A to point B. It is especially
worse in the Bay Area during the rush hours. Imagine you can have data from all 
vehicles driving on the road. What can you do with it? Simply visualize the traffic
density and average speed of each region can help city planer make better roads
and reduce congestions. Delivery services can better route their trucks and increase
efficiency. Navigation softwares can incorporate these data and further imporve user
experience. 

## Data Pipeline
![Alt text](miscellaneous/pipeline.png?raw=true "Optional Title")

## Architecture
The data is assumed pumping into Kafka cluster from mutiple devices. Each message 
contains lat, long, car id, time, and speed. Spark streaming then consume 20 seconds
worth of messages and map a grid id to each message. This mapping can also be done 
on street id if the condition of specific road is perfered. The filtering of time will 
also be done in case of trandfer delay. The processed messages then being aggregate
by grid id, calculate the unique count and average speed, and store the resulting 
calculations in Redis. Each message is also grouped by location and time for generate
the graph. The graph information are stored in the db 1 of the same Redis server and
being flush and recomputed every 20 seconds. In the frontend, when the map is being 
requested, Flask will query all data from db 0 and generate the location information 
for each grid for display on the map. Query one will convert the lat and long 
back to the grid id and make the query. Query all will query all data and generate json 
structure for all grid information. When the graph is requested, Flask will query all 
data from db 1 and generate the connection json file. The number of connection is 
bounded by 5000. Then the front end will read the newly generated file and display the
traffic graph.


## Product
- All demo were presented at this point and AWS servers were taken down. Please refer to the Youtube video for the 
[product](https://youtu.be/DCf3mRKyO_8).

![Alt text](miscellaneous/real_time_traffic.png?raw=true "Optional Title")
- Live demo is at [http://autolog.online/](http://autolog.online/)
- Query traffic data for a specific location with 
[http://autolog.online/api/query?lat=37.765217&long=-122.438982](http://autolog.online/api/query?lat=37.765217&long=-122.438982)
- Query all data with [http://autolog.online/api/alldata](http://autolog.online/api/alldata)
- Plot car connections wtih [http://autolog.online/graph](http://autolog.online/graph)
![Alt text](miscellaneous/car_connection_graph.png?raw=true "Optional Title")


## Project Setups
### Clusters Setup
1. Use [pegasus](https://github.com/InsightDataScience/pegasus) and the 
yml files in `cluster_setup` folder to setup clusters. Install and start 
Zookeeper and Kafka for `gene-su-kafka` with pegasus. Insatll and start 
Hadoop and Spark for `gene-su-spark`.
2. Login to master node of `gene-su-kafka` and create the `auto_log` topic with 
    
    ~~~
    /usr/local/kafka/bin/kafka-topics.sh --create --zookeeper localhost:2181 --topic auto_log --partitions 4 --replication-factor 2
    ~~~

### Simulator Setup
1. Create a new AWS EC2 for traffic simulation (or simulate on local machine).
2. Install the required libraries on the new EC2 instance (follow for Ubuntu 14.04).
    
    ~~~
    sudo apt-get update
    sudo apt-get install python-pip
    sudo apt-get install build-essential python-dev
    sudo apt-get install gfortran
    sudo pip install numpy
    sudo apt-get install libjpeg-dev
    sudo apt-get install libjpeg8-dev
    sudo apt-get install libpng3 
    sudo apt-get install libfreetype6-dev
    sudo pip install Pillow
    sudo pip install kafka-python
    ~~~

3. Clone this repository 
    
    ~~~
    sudo apt-get install git
    git clone https://github.com/GeneDer/Auto-Log
    ~~~

4. Know the IP of master node of `gene-su-kafka` and start the simulation.
   
    ~~~
    cd Auto-Log/traffic_simulator
    bash spawn_kafka_streams.sh <ip address> <number of session> <session name> <number of car simulated>

    e.g. bash spawn_kafka_streams.sh 35.167.53.204 10 k1 100000
    ~~~

5. You can check the message produced by the simulator with the following commend 
in master node of `gene-su-kafka`.
    
    ~~~
    /usr/local/kafka/bin/kafka-simple-consumer-shell.sh --broker-list localhost:9092 --topic auto_log --partition 0
    ~~~

### Redis and Spark Setup
1. Follow [this guide](https://github.com/InsightDataScience/data-engineering-ecosystem/wiki/Redis)
to install Redis on the master node of `gene-su-spark`. Make the following change to
the `redis.conf` file before start, so it can be accessed from outside.
   
    ~~~
    #bind 127.0.0.1
    requirepass <your password here>
    daemonize yes
    ~~~

2. Clone this repository to the master node of `gene-su-spark`.

    ~~~
    git clone https://github.com/GeneDer/Auto-Log
    ~~~

3. Change the DNS of Kafka server and ip and password of Redis server in 
`Auto-Log/spark_streaming/src/main/scala/traffic_data.scala` on line 15, 42, and 58.
4. Compile and start spark job.

    ~~~
    cd Auto-Log/spark_streaming/
    sbt assembly
    sbt package
    spark-submit --class TrafficDataStreaming --master spark://<spark master node private DNS>:7077 --jars target/scala-2.11/traffic_data-assembly-1.0.jar target/scala-2.11/traffic_data-assembly-1.0.jar

    e.g.
    spark-submit --class TrafficDataStreaming --master spark://ip-172-31-0-69:7077 --jars target/scala-2.11/traffic_data-assembly-1.0.jar target/scala-2.11/traffic_data-assembly-1.0.jar
    ~~~

### Flask Setup (was modified from this [guide](http://www.datasciencebytes.com/bytes/2015/02/24/running-a-flask-app-on-aws-ec2/))
1. In master node of `gene-su-spark`, replace the `key.txt` file under 
`flaskapp` with your redis ip and password.
2. Install the apache webserver, mod_wsgi, flask, and redis client.

    ~~~
    sudo apt-get update
    sudo apt-get install apache2
    sudo apt-get install libapache2-mod-wsgi
    sudo pip install flask
    sudo pip install redis
    ~~~

3. Create the flask directory for apache

    ~~~
    sudo ln -sT /home/ubuntu/Auto-Log/flaskapp /var/www/html/flaskapp
    ~~~

4. Enable mod_wsgi.

    ~~~
    sudo nano /etc/apache2/sites-enabled/000-default.conf

    # add the following under `DocumentRoot /var/www/html`
    WSGIDaemonProcess flaskapp threads=5
    WSGIScriptAlias / /var/www/html/flaskapp/flaskapp.wsgi

    <Directory flaskapp>
        WSGIProcessGroup flaskapp
        WSGIApplicationGroup %{GLOBAL}
        Order deny,allow
        Allow from all
    </Directory>
    ~~~

5. Restart the webserver.

    ~~~
    sudo apachectl restart
    ~~~

6. Change the file owner of `data.json` so that flask can rewrite new data.

    ~~~
    sudo chown www-data:www-data Auto-Log/flaskapp/static/data.json
    ~~~

7. Now you can check the traffic density and average speed of simulated 
San Francisco traffics with the IP of the master node of `gene-su-spark`.
As a note to myself, the apache error log can be found 
    ~~~
    nano /var/log/apache2/error.log
    ~~~
