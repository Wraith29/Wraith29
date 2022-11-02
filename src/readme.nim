import
  std/[
    os,
    times,
    enumerate,
    strutils,
    strformat
  ],
  ./github,
  ./language,
  ./pieChart

proc update(username: string) =
  let 
    languageMap = getLanguageMap(username)
    languageBreakdown = getLanguageBreakdown(languageMap)
    pieChart = createPieChart(400, languageMap)
    updatedAt = getTime().format("dddd dd MMM YYYY HH:mm:ss")
  
  var
    templ = readFile("./TEMPLATE.md").split("\n")

  for idx, line in enumerate(templ):
    if line == "{pieChart}":
      templ[idx] = &"{pieChart}\n"
    elif line == "{languageTable}":
      templ[idx] = &"{languageBreakdown}\n"
    elif line == "{updatedAt}":
      templ[idx] = &"{updatedAt}\n"
    
  writeFile("./README.md", templ.join("\n"))

proc main =
  var username = "Wraith29"
  if paramCount() == 1:
    username = paramStr(1)
  username.update

when isMainModule:
  main()