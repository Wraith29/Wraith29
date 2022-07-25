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
    let colour = getLanguageColour(language)
    rows.add(createLanguageRow(language, colour, count))
  
  rows.join("\n")