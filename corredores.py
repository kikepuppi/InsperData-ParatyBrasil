import requests
from bs4 import BeautifulSoup
import pandas as pd

def corredores(link):
    
    dic = {}

    url = str(link)
    browsers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 \(KHTML, like Gecko) Chrome / 86.0.4240.198Safari / 537.36'}
    page = requests.get(url, headers=browsers)

    soup = BeautifulSoup(page.content, 'html.parser')
    dict_about = {}
    need = ['Club', 'Team', 'Sponsor(s)', 'Website']
    for i in need:
        dict_about[i] = None

    about = soup.select('.runner-more-details_details_element__3rIxF')
    for i in about:
        dict_about[i.find('p').text] = i.find('span').text 

    dic[link] = list(dict_about.values())

    index = soup.select('.performance_stats_container__Guwj0')[0].find_all('h2')
    lista_index = [
        i.text
        for i in index
    ]

    dic[link] += lista_index

    df = pd.DataFrame(dic.values(), index=dic.keys())
    df = df.set_axis(['Club', 'Team', 'Sponsor(s)', 'Website','UTMB Geral','20K','50K','100K','100m'], axis=1)

    return df



links = ['https://utmb.world/en/runner/2623403.wellington.robertonoronha',
'https://utmb.world/en/runner/395551.celio.augustorosa',
'https://utmb.world/en/runner/5027328.johnny.lunalima',
'https://utmb.world/en/runner/1359763.rogerio.silvestrin'
]

print(corredores(links[0]))

