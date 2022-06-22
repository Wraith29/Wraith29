import requests as r
from configparser import ConfigParser

def reached_ratelimit(username, token):
    url = f"https://api.github.com/users/{username}"
    res = r.get(url, headers={'Authorization': f'token {token}'}).headers

    if res["X-RateLimit-Remaining"] == 0:
        return True
    return False

def get_token():
    cp = ConfigParser()
    cp.read("./config.ini")

    return cp.get("user", "token")

def get_repos(username = "Wraith29"):
    token = get_token()

    if reached_ratelimit(username, token):
        print("RateLimit Reached. Try again later.")
        return
    
    url = f"https://api.github.com/users/{username}/repos"
    repos = r.get(url, headers={'Authorization': f'token {token}'}).json()
    return repos

def get_language_map(username = "Wraith29"):
    repos = get_repos(username)
    lang_map = {}
    for repo in repos:
        url = repo["languages_url"]
        data = r.get(url, headers={"Authorization": f"token {get_token()}"}).json()
        for lang, count in data.items():
            try:
                lang_map[lang] += count
            except KeyError:
                lang_map[lang] = count
    
    lm = dict(reversed(sorted(lang_map.items(), key = lambda x: x[1])))
    
    return lm