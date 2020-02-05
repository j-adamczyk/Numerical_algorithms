import java.io._

object Main
{
  def main(args: Array[String]) =
  {
    val P_0 = 0.2f
    val n = 100
    val m = 90 //number of last iterations to be saved, min 1 and max n-1

    //creating file to export for GNUPlot
    val file = new File("C:\\Users\\Lenovo\\Desktop\\Zadanie 4\\data.dat")
    val bw = new BufferedWriter(new FileWriter(file))

    var points = ""

    for (r <- 3.75f to 3.8f by math.pow(10,-4).toFloat)
    {
      val data = logisticMapSimpleDouble(P_0,r,n,m)
      for (i <- data.indices)
        points = points + r.toString + " " + data(i).toString + "\n"
    }

    bw.write(points)
    bw.close()

    /*println("x_0:    Float:     Double:")
    //measuring steps needed to get to 0 with r=4
    for (x_0 <- 0.1 to 1 by 0.1)
    {
      println(x_0 + "     " + logisticMapCountTo0Float(x_0.toFloat) + "       " + logisticMapCountTo0Double(x_0))
    }*/
  }

  def logisticMapSimpleFloat (P_0: Float, r: Float, n: Int, m: Int): Array[Float] =
  {
    val P = new Array[Float](n)
    P(0) = P_0

    for (i <- 0 until P.length - 1)
      P(i+1) = r * P(i) * (1 - P(i))

    P.slice(n - m,n)
  }

  def logisticMapSimpleDouble (P_0: Double, r: Double, n: Int, m: Int): Array[Double] =
  {
    val P = new Array[Double](n)
    P(0) = P_0

    for (i <- 0 until P.length - 1)
      P(i+1) = r * P(i) * (1 - P(i))

    P.slice(n - m,n)
  }

  def logisticMapCountTo0Float (x_0: Float): Int =
  {
    val r = 4
    var P_i: Float = x_0
    var P_i_next: Float = r * P_i * (1 - P_i)
    var counter = 0

    while (P_i_next > 0)
    {
      val tmp: Float = P_i_next
      P_i_next = r * P_i * (1 - P_i)
      P_i = tmp

      counter += 1
    }

    counter
  }

  def logisticMapCountTo0Double (x_0: Double): Int =
  {
    val r = 4
    var P_i: Double = x_0
    var P_i_next: Double = r * P_i * (1 - P_i)
    var counter = 0

    while (P_i_next > 0)
    {
      val tmp: Double = P_i_next
      P_i_next = r * P_i * (1 - P_i)
      P_i = tmp

      counter += 1
    }

    counter
  }
}
