import scala.collection.mutable.ListBuffer

object Main
{
  def main(args: Array[String]) =
  {
    var sValues = new ListBuffer[Double]
    sValues += (2.0, 3.667, 5.0, 7.2, 10.0)
    var nValues = new ListBuffer[Int]
    nValues += (50, 100, 200, 500, 1000)

    //single precision dzeta
    var dzetaValuesFloatForward = new ListBuffer[FunctionResult]
    for (s <- sValues; n <- nValues)
      dzetaValuesFloatForward += new FunctionResult(s, n, dzeta(s, n, "forward", "Float").toFloat)

    var dzetaValuesFloatBackward = new ListBuffer[FunctionResult]
    for (s <- sValues; n <- nValues)
      dzetaValuesFloatBackward += new FunctionResult(s, n, dzeta(s, n, "backward", "Float").toFloat)

    //single precision eta
    var etaValuesFloatForward = new ListBuffer[FunctionResult]
    for (s <- sValues; n <- nValues)
      etaValuesFloatForward += new FunctionResult(s, n, eta(s, n, "forward", "Float").toFloat)

    var etaValuesFloatBackward = new ListBuffer[FunctionResult]
    for (s <- sValues; n <- nValues)
      etaValuesFloatBackward += new FunctionResult(s, n, eta(s, n, "backward", "Float").toFloat)

    //double precision dzeta
    var dzetaValuesDoubleForward = new ListBuffer[FunctionResult]
    for (s <- sValues; n <- nValues)
      dzetaValuesDoubleForward += new FunctionResult(s, n, dzeta(s, n, "forward", "Double"))

    var dzetaValuesDoubleBackward = new ListBuffer[FunctionResult]
    for (s <- sValues; n <- nValues)
      dzetaValuesDoubleBackward += new FunctionResult(s, n, dzeta(s, n, "backward", "Double"))

    //double precision eta
    var etaValuesDoubleForward = new ListBuffer[FunctionResult]
    for (s <- sValues; n <- nValues)
      etaValuesDoubleForward += new FunctionResult(s, n, eta(s, n, "forward", "Double"))

    var etaValuesDoubleBackward = new ListBuffer[FunctionResult]
    for (s <- sValues; n <- nValues)
      etaValuesDoubleBackward += new FunctionResult(s, n, eta(s, n, "backward", "Double"))

    println("Single precision dzeta (forward and backward in next lines for each n and s):")
    println("n:     s:     value:")
    for (i <- dzetaValuesFloatForward.indices)
    {
      print(dzetaValuesFloatForward(i).n + " " + dzetaValuesFloatForward(i).s + " ")
      print(dzetaValuesFloatForward(i).value + "\n")
      print("        " + dzetaValuesFloatBackward(i).value + "\n")
    }

    println("\n\n")

    println("Double precision dzeta (forward and backward in next lines for each n and s):")
    println("n:     s:     value:")
    for (i <- dzetaValuesDoubleForward.indices)
    {
      print(dzetaValuesDoubleForward(i).n + " " + dzetaValuesDoubleForward(i).s + " ")
      print(dzetaValuesDoubleForward(i).value + "\n")
      print("        " + dzetaValuesDoubleBackward(i).value + "\n")
    }
  }

  def dzeta(s: Double, n: Int, direction: String, precision: String) =
  {
    direction match
    {
      case "forward" =>
        precision match
        {
          case "Float" =>
            var value: Float = 0.0f
            for (k <- 1 to n) value += (1 / math.pow(k, s)).toFloat
            value.toDouble

          case "Double" =>
            var value: Double = 0.0
            for (k <- 1 to n) value += 1 / math.pow(k, s)
            value
        }

      case "backward" =>
        precision match
        {
          case "Float" =>
            var value: Float = 0.0f
            for (k <- (1 to n).reverse) value += (1 / math.pow(k, s)).toFloat
            value.toDouble

          case "Double" =>
            var value: Double = 0.0
            for (k <- (1 to n).reverse) value += 1 / math.pow(k, s)
            value
        }
    }
  }

  def eta(s: Double, n: Int, direction: String, precision: String) =
  {
    direction match
    {
      case "forward" =>
        precision match
        {
          case "Float" =>
            var value: Float = 0.0f
            for (k <- 1 to n) value += (math.pow(-1, k - 1) * (1 / math.pow(k, s))).toFloat
            value.toDouble

          case "Double" =>
            var value: Double = 0.0
            for (k <- 1 to n) value += math.pow(-1, k - 1) * (1 / math.pow(k, s))
            value
        }

      case "backward" =>
        precision match
        {
          case "Float" =>
            var value: Float = 0.0f
            for (k <- (1 to n).reverse) value += (math.pow(-1, k - 1) * (1 / math.pow(k, s))).toFloat
            value.toDouble

          case "Double" =>
            var value: Double = 0.0
            for (k <- (1 to n).reverse) value += math.pow(-1, k - 1) * (1 / math.pow(k, s))
            value
        }
    }
  }
}
