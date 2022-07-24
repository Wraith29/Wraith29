import strformat, httpclient, parsecfg, json, tables, uri, algorithm, sugar
import ./language

type Language = tuple[name: string, count: int]

proc getToken(): string =
  let config = loadConfig("config.ini")
  config.getSectionValue("user", "token")

proc getClient(): HttpClient =
  let token = getToken()
  result = newHttpClient()
  result.headers = newHttpHeaders({
    "Authorization": fmt"token {token}"
  })

proc reachedRatelimit(username: string, token: string): bool = 
  let client = getClient()
  var res = client.get(fmt"https://api.github.com/users/{username}")
  var rem = res.headers["x-ratelimit-remaining"]

  $rem == "0"

proc getRepos(username: string): JsonNode =
  let 
    client = getClient()
    token = getToken()
    url = fmt"https://api.github.com/users/{username}/repos"

  if reachedRatelimit(username, token):
    echo "Ratelimit Reached, please try again later."
    return

  client.getContent(url).parseJson

proc getLanguageMap*(username: string): LanguageMap =
  let 
    client = getClient()
    repos = username.getRepos

  for repoNode in repos:
    var url = $repoNode.getOrDefault("languages_url")
    if url[0] == '"' and url[url.len-1] == '"':
      url = url.substr(1, url.len - 2)
    let res = client.getContent(url).parseJson
    for key, value in res.pairs:
      if result.hasKey(key):
        result[key] += value.getInt
      else:
        result[key] = value.getInt

  result.sort((x, y: Language) => (cmp(x.count, y.count)), SortOrder.Descending)