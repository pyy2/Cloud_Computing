/* SimpleApp.scala */
import org.apache.spark.SparkContext
import org.apache.spark.SparkContext._
import org.apache.spark._

object SimpleApp {
  def main(args: Array[String]) {
    /* SimpleApp.scala */
    // val conf= new SparkConf()
    // conf.set("spark.app.name", "Simple Application") 
    // conf.set("spark.master", "local[4]")
    // conf.set("spark.ui.port", "36000") // Override the default port 
    // // Create a SparkContextwith this configuration 
    // val sc = new SparkContext(conf)

        val spark = SparkSession
      .builder
      .appName("Movies Reviews")
      .config("spark.master", "local")
      .getOrCreate()

    val logFile = "/usr/local/spark/README.md" // Should be some file on your system
    val logData = sc.read.textFile(logFile).cache()
    val numAs = logData.filter(line => line.contains("a")).count()
    val numBs = logData.filter(line => line.contains("b")).count()
    println(s"Lines with a: $numAs, Lines with b: $numBs")
    sc.stop()
  }
}