import requests
from bs4 import BeautifulSoup
import re

urls = [
    "https://www.kickstarter.com/projects/470959527/these-hard-streets",
    "https://www.kickstarter.com/projects/clarissaredwine/swingby-a-voyager-gravity-puzzle",
    "https://www.kickstarter.com/projects/100389301/us-army-navy-marines-air-force-special-challenge-c"
]
slugs = []

#extract slugs from url
for url in urls:
    slugs.append(re.search('/projects/(.*)', url).group(1))

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

for slug in slugs:
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

    result = r.json()

    print("-------STORY--------")
    story_html = result["data"]["project"]["story"]
    soup = BeautifulSoup(story_html, 'html.parser')
    for i in soup.find_all('p')[:2]:
        print(i.get_text())

    # print("-------RISKS--------")
    # print(result["data"]["project"]["risks"])
