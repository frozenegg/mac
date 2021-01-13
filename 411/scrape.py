import requests
from bs4 import BeautifulSoup
import re
import pickle

with open('urls_state_2.txt', 'rb') as f:
    urls_state = pickle.load(f)

try:
    with open('url_cotent.txt', 'rb') as f:
        content_state = pickle.load(f)
except:
    content_state = {}

slugs = []

#extract slugs from url
for url in urls_state.keys(): #
    # print(url)
    slugs.append(re.search('/projects/(.*)', url).group(1))

# print(slugs)

s = requests.Session()
r = s.get("https://www.kickstarter.com")
soup = BeautifulSoup(r.text, 'html.parser')
xcsrf = soup.find("meta", {"name": "csrf-token"})["content"]

query = """
query Campaign($slug: String!) {
  project(slug: $slug) {
    risks
    story(assetWidth: 680)
  }
}"""

n = 0

for slug in slugs:
    if slug in content_state.keys():
        print('Done', end='\r')
        continue
    n += 1
    # try:
    print(len(content_state), n, end='\r')
    print(f"--------{slug}------")
    r = s.post("https://www.kickstarter.com/graph",
        headers= {
            "x-csrf-token": xcsrf
        },
        json = {
            "operationName":"Campaign",
            "variables":{
                "slug": slug
            },
            "query": query
        })

    # print(r.status_code, '       ')
    print(len(content_state), n, end='\r')
    result = r.json()
    # print("-------STORY--------")
    if result["data"]["project"] == None:
        continue
    story_html = result["data"]["project"]["story"]
    soup = BeautifulSoup(story_html, 'html.parser')
    sentence = ''
    for i in soup.find_all('p')[:3]:
        sentence += i.get_text()

    state = urls_state["https://www.kickstarter.com/projects/" + slug]
    new_dict = {slug: sentence}
    print(len(content_state), n, new_dict)
    content_state.update(new_dict)
    with open('url_cotent.txt', 'wb') as f:
        pickle.dump(content_state, f)
    # except:
    #     continue

    # print("-------RISKS--------")
    # print(result["data"]["project"]["risks"])
print(len(content_state), n)
