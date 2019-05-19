
import scala.util.Random
import scala.math.max
import scala.math.min
import scala.math.pow
import org.apache.spark.sql.SparkSession


class RunningVar(values: TraversableOnce[Double]) extends Serializable{
  private var n: Long = 0     // Running count of our values
  private var mu: Double = 0  // Running mean of our values
  private var m2: Double = 0  // Running variance numerator (sum of (x - mean)^2)
  private var maxValue: Double = Double.NegativeInfinity // Running max of our values
  private var minValue: Double = Double.PositiveInfinity // Running min of our values

  merge(values);
  def this() = this(Nil)

  /** Add a value into this StatCounter, updating the internal statistics. */
  def merge(value: Double): RunningVar = {
    val delta = value - mu
    n += 1
    mu += delta / n
    m2 += delta * (value - mu)
    maxValue = math.max(maxValue, value)
    minValue = math.min(minValue, value)
    this
  }

  /** Add multiple values into this StatCounter, updating the internal statistics. */
  def merge(values: TraversableOnce[Double]): RunningVar = {
    values.foreach(v => merge(v))
    this
  }


  /** Merge another RunningVar into this one, adding up the internal statistics. */
  def merge(other: RunningVar): RunningVar= {
    if (other == this) {
      merge(other.copy())  // Avoid overwriting fields in a weird order
    } else {
      if (n == 0) {
        mu = other.mu
        m2 = other.m2
        n = other.n
        maxValue = other.maxValue
        minValue = other.minValue
      } else if (other.n != 0) {
        val delta = other.mu - mu
        if (other.n * 10 < n) {
          mu = mu + (delta * other.n) / (n + other.n)
        } else if (n * 10 < other.n) {
          mu = other.mu - (delta * n) / (n + other.n)
        } else {
          mu = (mu * n + other.mu * other.n) / (n + other.n)
        }
        m2 += other.m2 + (delta * delta * n * other.n) / (n + other.n)
        n += other.n
        maxValue = math.max(maxValue, other.maxValue)
        minValue = math.min(minValue, other.minValue)
      }
      this
    }
  }

  def copy() = {
    val other = new RunningVar
    other.n = n
    other.mu = mu
    other.m2 = m2
    other.maxValue = maxValue
    other.minValue = minValue
    other
  }

  def count: Long = n
  def mean: Double = mu
  def sum: Double = n * mu
  def max: Double = maxValue
  def min: Double = minValue

  def variance: Double = popVariance

  def popVariance: Double = {
    if (n == 0) {
      Double.NaN
    } else {
      m2 / n
    }
  }

  def sampleVariance: Double = {
    if (n <= 1) {
      Double.NaN
    } else {
      m2 / (n - 1)
    }
  }

  def stdev: Double = popStdev

  def popStdev: Double = math.sqrt(popVariance)

  def sampleStdev: Double = math.sqrt(sampleVariance)

  override def toString: String = {
    "(count: %d, mean: %f, stdev: %f, max: %f, min: %f)".format(count, mean, stdev, max, min)
  }

  def main() {
    val spark = SparkSession
    .builder
    .appName("Running Variance")
    .config("spark.master", "local")
    .getOrCreate()

    val random_numbers = (1 to 100).map(x => Random.nextInt(100))
    // now setup to parallelize the computation ...
    lazy val intRDD = spark.sparkContext.parallelize(random_numbers)
    var result = intRDD.mapPartitions(v => TraversableOnce(new RunningVar(v))).reduce((a, b) => a.merge(b))
    assert(result === intRDD.variance())
  }
}