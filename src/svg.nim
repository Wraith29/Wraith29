import 
  std/[
    strformat
  ]

proc createSvg*(width, height: int, data, filename: string) {.inline.} =
  let content = &"<svg width=\"{width}\" height=\"{height}\" xmlns=\"http://www.w3.org/2000/svg\">\n{data}\n</svg>"
  writeFile(fmt"./assets/{filename}.svg", content)

proc createRect(width, height: int, colour: string, x: int = 0, rx: int = 0): string {.inline.} =
  &"<rect width=\"{width}\" height=\"{height}\" fill={colour} rx=\"{rx}\" />"

proc createLanguageRow*(language, colour: string, count: int): string =
  createSvg(10, 10, createRect(10, 10, colour), language)
  fmt"|![{language}](./assets/{language}.svg) {language}|{count}|"

proc createArcPath*(language, colour, arcPath: string): string {.inline.} =
  &"<path class=\"{language}\" d=\"{arcPath}\" fill={colour} stroke={colour}><title>{language}</title></path>"

proc createText*(x, y: int, fill, stroke, text: string, textLength: int = 0): string =
  if textLength == 0: return &"<text x=\"{x}\" y=\"{y}\" fill={fill} stroke={stroke}>{text}</text>"
  &"<text x=\"{x}\" y=\"{y}\" fill={fill} stroke={stroke} textLength=\"{textLength}\">{text}</text>"
