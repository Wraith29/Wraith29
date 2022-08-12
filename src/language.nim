import 
  std/[
    tables, 
    math, 
    sugar, 
    strformat, 
    strutils
  ], 
  ./svg, 
  ./colours

type LanguageMap* = OrderedTable[string, int]

func total*(map: LanguageMap): int =
  sum(collect(for _,v in map.pairs:v))

proc getLanguageBreakdown*(map: LanguageMap): string =
  let total = map.total
  var rows = @[
    "|Language|Bytes|",
    "|:-:|:-:|",
    fmt"|Total|{total}|"
  ]

  for language, count in map.pairs:
    let language = language.replace("#", "Sharp")
    let colour = getLanguageColour(language)
    let langSvg = newSvg(10, 10, @[
      newSvgNode(
        Rect, 
        attrs = @[
          newSvgAttribute("width", "10"), 
          newSvgAttribute("height", "10"),
          newSvgAttribute("fill", colour),
        ]
      )
    ])
    langSvg.write(language)
    rows.add(fmt"![{language}](./assets/{language}.svg) {language}|{count}|")
  
  rows.join("\n")