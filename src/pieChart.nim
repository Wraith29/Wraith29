import std/[math, strformat, tables, strutils, enumerate]
import ./language
import ./colours
import ./svg

type
  Pos = ref object
    x, y: int

  LargeArcFlag = enum
    Zero, One

  Arc = ref object
    radius: int
    startPos, endPos: Pos
    largeArcFlag: LargeArcFlag

func newPos(x, y: int): Pos =
  new result
  result.x = x
  result.y = y

func toCartesian(pos: Pos, radius, angleInDegrees: int): Pos =
  new result
  let 
    angleInRadians = (angleInDegrees - 90).toFloat * PI / 180.toFloat
    x = (pos.x.toFloat + (radius.toFloat * cos(angleInRadians))).floor.toInt
    y = (pos.y.toFloat + (radius.toFloat * sin(angleInRadians))).floor.toInt
  
  newPos(x, y)

func `$`(largeArcFlag: LargeArcFlag): string =
  case largeArcFlag:
  of LargeArcFlag.Zero: "0"
  of LargeArcFlag.One: "1"

func newArc(pos: Pos, radius, startAngle, endAngle: int): Arc =
  new result
  result.radius = radius
  result.startPos = pos.toCartesian(radius, endAngle)
  result.endPos = pos.toCartesian(radius, startAngle)
  result.largeArcFlag = if endAngle - startAngle <= 180: LargeArcFlag.Zero else: LargeArcFlag.One

func createArc(center: Pos, arc: Arc): string =
  fmt"M {center.x} {center.y} L {arc.startPos.x} {arc.startPos.y} A {arc.radius} {arc.radius} 0 {$arc.largeArcFlag} 0 {arc.endPos.x} {arc.endPos.y} L {center.x} {center.y}"

proc createPieChart*(svgSize: int, map: LanguageMap): string =
  let 
    total  = map.total
    center = newPos((svgSize / 2).toInt, (svgSize / 2).toInt)
    radius = (svgSize / 2).toInt

  var
    cumulativeTotal = 0
    data = newSeq[string](map.len)

  for index, (language, count) in enumerate(map.pairs):
    let 
      angleCoverage = ((count / total) * 360).toInt
      arc = newArc(center, radius, cumulativeTotal, cumulativeTotal + angleCoverage)
      colour = getLanguageColour(language)

    data[index] = createArcPath(language, colour, createArc(center, arc))
    cumulativeTotal += angleCoverage
  
  createSvg(svgSize, svgSize, data.join("\n"), "PieChart")
  "![Pie Chart](./assets/PieChart.svg \"Pie Chart Detailing used languages\")"