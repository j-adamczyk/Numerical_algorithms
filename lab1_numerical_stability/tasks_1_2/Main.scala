import java.util.Random
import scala.collection.mutable.ListBuffer
import scalax.chart.api._

object Main
{
  def main(args: Array[String]) =
  {
    val minBound = 0.1f
    val maxBound = 0.9f
    val size = math.pow(10,7).toInt
    val randomizer = new Random
    //val v: Float = minBound + randomizer.nextFloat() * (maxBound - minBound)
    val v = 0.25f
    val vArray: Array[Float] = new Array[Float](size)
    for (i <- vArray.indices) vArray(i) = v
    summingNumbers(vArray)

    /*for (v <- 0.1f to 0.9f by 0.1f)
      {
        val vArray: Array[Float] = new Array[Float](size)
        for (i <- vArray.indices) vArray(i) = v
        summingNumbers(vArray)
      }*/

  }

  def summingNumbers(vArray: Array[Float]): Unit =
  {
    //preparations
    val size = vArray.length
    val v = vArray(0)
    val summedValueReal = size * v

    //summing linearly, task 1.1
    var summedValueLinear: Float = 0.0f
    var errorStepCounter = 0
    val relativeErrorValues = new ListBuffer[Float]()

    val summingLinearStartTime = System.nanoTime()
    for (i <- vArray.indices)
    {
      summedValueLinear += vArray(i)
      errorStepCounter += 1

      if (errorStepCounter == 25000)
      {
        val realValue: Float = (i+1) * v
        relativeErrorValues += math.abs(realValue - summedValueLinear)
        //relativeErrorValues += (math.abs(realValue - summedValueLinear) / realValue)
        errorStepCounter = 0
      }
    }
    val summingLinearEndTime = System.nanoTime()

    //absolute and relative errors, task 1.2
    val absErrorLinear = math.abs(summedValueReal - summedValueLinear)
    val relativeErrorLinear = math.abs(absErrorLinear / summedValueReal)

    //plotting relative error, task 1.3
    val data = for (i <- relativeErrorValues.indices) yield(25000*(i+1),relativeErrorValues(i))
    val chart = XYLineChart(data)
    chart.title = v.toString
    chart.show()

    //summing recursively
    val summingRecursiveStartTime = System.nanoTime()
    val summedValueRecursive = sumRecursively(0,size-1,vArray)
    val summingResursiveEndTime = System.nanoTime()

    val absErrorRecursive = math.abs(summedValueReal - summedValueRecursive)
    val relativeErrorRecursive = math.abs(absErrorRecursive / summedValueReal)

    //summing using Kahan summation algorithm
    val summingKahanStartTime = System.nanoTime()
    val summedValueKahan = sumKahan(vArray)
    val summingKahanEndTime = System.nanoTime()

    val absErrorKahan = math.abs(summedValueReal - summedValueKahan)
    val relativeErrorKahan = math.abs(absErrorKahan / summedValueReal)

    //results and sum and errors comparisons, tasks 1.2, 1.5 and 2.1
    println("Linear sum: " + summedValueLinear)
    println("Recursive sum: " + summedValueRecursive)
    println("Kahan sum: " + summedValueKahan)
    println("Real sum: " + summedValueReal)

    println("\n")

    println("Linear absolute error: " + absErrorLinear)
    println("Recursive absolute error: " + absErrorRecursive)
    println("Kahan absolute error: " + absErrorKahan)

    println("\n")

    println("Linear relative error: " + relativeErrorLinear)
    println("Recursive relative error: " + relativeErrorRecursive)
    println("Kahan relative error: " +relativeErrorKahan)

    //time comparison, tasks 1.6 and 2.3
    val summingLinearTime = summingLinearEndTime - summingLinearStartTime
    val summingRecursiveTime = summingResursiveEndTime - summingRecursiveStartTime
    val summingKahanTime = summingKahanEndTime - summingKahanStartTime

    println("Linear summing time: " + summingLinearTime + "ns")
    println("Recursive summing time: " + summingRecursiveTime + "ns")
    println("Kahan summing time: " + summingKahanTime + "ns")
  }

  def sumRecursively(left: Int, right: Int, array: Array[Float]): Float =
  {
    if (left == right) array(left)
    else
    {
      val mid = (left + right) / 2
      sumRecursively(left,mid,array) + sumRecursively(mid+1,right,array)
    }
  }

  //Kahan summation algorithm, task 2
  def sumKahan(array: Array[Float]): Float =
  {
    var sum: Float = 0.0f
    var err: Float = 0.0f

    for (i <- array.indices)
    {
      val y: Float = array(i) - err
      val tmp: Float = sum + y
      err = (tmp - sum) - y
      sum = tmp
    }

    sum
  }
}
