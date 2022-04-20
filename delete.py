import requests
import urllib.request

S = requests.Session()

URL = "https://zh.moegirl.org.cn/api.php"

# Retrieve login token first
PARAMS_0 = {
    'action':"query",
    'meta':"tokens",
    'type':"login",
    'format':"json"
}

R = S.get(url=URL, params=PARAMS_0)
DATA = R.json()

LOGIN_TOKEN = DATA['query']['tokens']['logintoken']

print(LOGIN_TOKEN)

# Send a post request to login. Using the main account for login is not
# supported. Obtain credentials via Special:BotPasswords
# (https://www.mediawiki.org/wiki/Special:BotPasswords) for lgname & lgpassword

PARAMS_1 = {
    'action':"login",
    'lgname':"", #BOTUSERNAME
    'lgpassword':"", #BOTPASSWORD
    'lgtoken':LOGIN_TOKEN,
    'format':"json"
}

R = S.post(URL, data=PARAMS_1)
DATA = R.json()

print(DATA)
#n1 = urllib.request.urlopen(urlstr1)
PARAMS_2 = {
    "action": "query",
    "meta": "tokens",
    "format": "json"
}

R = S.get(url=URL, params=PARAMS_2)
DATA = R.json()

CSRF_TOKEN = DATA['query']['tokens']['csrftoken']

# Step 4: POST request to edit a page

PARAMS = {
    "action": "query",
    "format": "json",
    "prop": "categories",
    "titles": "" #TITLE
}

R = S.get(url=URL, params=PARAMS)
DATA = R.json()

PAGES = DATA["query"]["pages"]

for k, v in PAGES.items():
    for cat in v['categories']:
        PARAMS_3 = {
            'action':"delete",
            'title':cat["title"],
            'token':CSRF_TOKEN,
            'format':"json"
        }
        R = S.post(URL, data=PARAMS_3)
        DATA = R.json()
        print(DATA)
#print(html.json())
#html = html.decode("utf-8")
