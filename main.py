import re
import eel
import requests
import urllib.parse
from random import randint
from bs4 import BeautifulSoup as BS

eel.init("web")


@eel.expose
def getActress():
    stars = []
    r = requests.get('https://www.imdb.com/list/ls058874836/')
    html = BS(r.content, 'html.parser')
    for el in html.select('.lister-item-header'):
        actress = el.text
        actress = ''.join([i for i in actress if not i.isdigit()])
        actress = actress.replace('\n', '')
        actress = actress.replace('.', '')
        actress = actress[2:-1]

        raw = str(el)
        site = re.findall(r'href=\"(?<=\")([\s\S]+?)(?=\")', raw)
        site = str(site)[2:-2]
        site = site.replace('/name/', '')

        stars.append({actress: site})

    return stars[randint(0, len(stars) - 1)]


@eel.expose
def getActressImage():
    for k, v in getActress().items():
        # print(v)
        images = []
        r = requests.get("https://www.imdb.com/name/" + v)
        html = BS(r.content, 'html.parser')
        for el in html.select('.image'):
            # print(el)
            raw = str(el)
            site = re.findall(r'src=\"(?<=\")([\s\S]+?)(?=\")', raw)
            site = str(site)[2:-2]
            images.append(site)

        result = [images[0], v]
        
    return result


@eel.expose
def getContent(v):
    content = []
    r = requests.get('https://www.imdb.com/filmosearch/?explore=genres&role=' + v + '&ref_=filmo_ref_typ&mode=detail&page=1&genres=Comedy&sort=moviemeter,asc&job_type=actress&title_type=movie')
    html = BS(r.content, 'html.parser')
    for el in html.select('.lister-item'):
        # print(el)
        site = str(el)
        site = site.replace("loadlate", "src")
        content.append(site)
    
    return content[randint(0, len(content) - 1)]


# print(getActressImage())

eel.start("index.html", size=(1000, 800))
