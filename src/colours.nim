import 
  std/[
    json
  ]

proc getLanguageColour*(language: string): string =
  let colours = readFile("colours.json").parseJson
  if colours.hasKey(language):
    return $colours[language]
  "green"
