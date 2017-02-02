import kafka.serializer.StringDecoder

import org.apache.spark.streaming._
import org.apache.spark.streaming.kafka._
import org.apache.spark.SparkConf
import org.apache.spark.rdd.RDD
import org.apache.spark.SparkContext
import org.apache.spark.sql._
import com.redis.RedisClient

object TrafficDataStreaming {
  def main(args: Array[String]) {

    val brokers = "ec2-35-167-53-204.us-west-2.compute.amazonaws.com:9092"
    val topics = "auto_log"
    val topicsSet = topics.split(",").toSet

    // Create context with 2 second batch interval
    val sparkConf = new SparkConf().setAppName("traffic_data")
    val ssc = new StreamingContext(sparkConf, Seconds(10))

    // Create direct kafka stream with brokers and topics
    val kafkaParams = Map[String, String]("metadata.broker.list" -> brokers)
    val messages = KafkaUtils.createDirectStream[String, String, StringDecoder, StringDecoder](ssc, kafkaParams, topicsSet)
    val windowStream = messages.window(Seconds(300), Seconds(10))

    // Get the lines and show results
    windowStream.foreachRDD { rdd =>

        val sqlContext = SQLContextSingleton.getInstance(rdd.sparkContext)
        import sqlContext.implicits._

        val lines = rdd.map(_._2)
        val ticksDF = lines.map( x => {
				       val tokens = x.split(";")
                                       Tick(tokens(0), tokens(3).toDouble, 1)
				      }).toDF()
        val ticks_per_source_DF = ticksDF.groupBy("grid_id")
                                .agg("speed" -> "avg", "volume" -> "sum")
                                .orderBy("grid_id")
	
	val r = new RedisClient("52.34.86.155", 6379, secret=Option("this is not real password XP"))
	ticks_per_source_DF.collect().foreach(t => {
			r.set(t(0),t(1).toString()+";"+t(2).toString())
		}
	)

        ticks_per_source_DF.show()
    }

    // Start the computation
    ssc.start()
    ssc.awaitTermination()
  }
}

case class Tick(grid_id: String, speed: Double, volume: Int)

/** Lazily instantiated singleton instance of SQLContext */
object SQLContextSingleton {

  @transient  private var instance: SQLContext = _

  def getInstance(sparkContext: SparkContext): SQLContext = {
    if (instance == null) {
      instance = new SQLContext(sparkContext)
    }
    instance
  }
}