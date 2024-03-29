import
  std/[
    math,
    strformat,
    tables,
    enumerate
  ],
  language, colours, svg, class

class Pos:
  x: int
  y: int

  func newPos(x, y: int): Pos {.static.} =
    Pos(x: x, y: y)
  
  func toCartesian(self: Pos, radius, angleInDegrees: int): Pos =
    new result
    let 
      angleInRadians = (angleInDegrees - 90).toFloat * PI / 180.toFloat
      x = (self.x.toFloat + (radius.toFloat * cos(angleInRadians))).floor.toInt
      y = (self.y.toFloat + (radius.toFloat * sin(angleInRadians))).floor.toInt
    
    newPos(x, y)

type LargeArcFlag = enum
    Zero, One

func `$`(largeArcFlag: LargeArcFlag): string =
  case largeArcFlag:
  of LargeArcFlag.Zero: "0"
  of LargeArcFlag.One: "1"

class Arc:
  radius: int
  startPos: Pos
  endPos: Pos
  largeArcFlag: LargeArcFlag


  func newArc(pos: Pos, radius, startAngle, endAngle: int): Arc {.static.} =
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
    svg = newSvg(svgSize, svgSize)

  for index, (language, count) in enumerate(map.pairs):
    let 
      angleCoverage = ((count / total) * 360).toInt
      arc = newArc(center, radius, cumulativeTotal, cumulativeTotal + angleCoverage)
      colour = getLanguageColour(language)
      arcSvg = newSvgNode(Path,children = @[newSvgNode(Title, children = @[newSvgNode(Text, inner = language)])],attrs = @[newSvgAttribute("class", language),newSvgAttribute("d", createArc(center, arc)),newSvgAttribute("fill", colour),newSvgAttribute("stroke", colour)])
    
    svg.add(arcSvg)

    cumulativeTotal += angleCoverage
  
  svg.write("PieChart")
  "![Pie Chart](./assets/PieChart.svg \"Pie Chart Detailing used languages\")"