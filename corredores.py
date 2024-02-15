import requests
from bs4 import BeautifulSoup
import pandas as pd


links = ['https://utmb.world/en/runner/2623403.wellington.robertonoronha',
'https://utmb.world/en/runner/395551.celio.augustorosa',
'https://utmb.world/en/runner/5027328.johnny.lunalima',
'https://utmb.world/en/runner/1359763.rogerio.silvestrin'
]

def corredor_info(link):
    dic = {}
    url = str(link)
    page = requests.get(url, headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome / 86.0.4240.198Safari / 537.36'})
    soup = BeautifulSoup(page.content, 'html.parser')
    dict_about = {i: None for i in ['Club', 'Team', 'Sponsor(s)', 'Website']}
    for i in soup.select('.runner-more-details_details_element__3rIxF'):
        dict_about[i.find('p').text] = i.find('span').text 
    dic[link] = list(dict_about.values()) + [i.text for i in soup.select('.performance_stats_container__Guwj0')[0].find_all('h2')]
    df_info = pd.DataFrame(dic.values(), index=dic.keys()).set_axis(['Club', 'Team', 'Sponsor(s)', 'Website','UTMB Geral','20K','50K','100K','100m'], axis=1)
    return df_info

def corredor_corridas(link):
    url = str(link)
    page = requests.get(url, headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome / 86.0.4240.198Safari / 537.36'})
    soup = BeautifulSoup(page.content, 'html.parser')
    corridas = soup.select('.my-table_row__nlm_j')
    dict_corridas = {i.find_all('div')[0].text:
        [i.find_all('div')[1].text,
        str(i.find_all('div')[2])[158:160],
        i.find_all('div')[3].find('img')['alt'],
        i.find_all('div')[5].text.split('M')[0],
        i.find_all('div')[5].text.split('M')[1].strip() + 'm',
        i.find_all('div')[6].text,
        i.find_all('div')[7].text,
        i.find_all('div')[8].text] for i in corridas}
    df_corridas = pd.DataFrame(dict_corridas.values(), index=dict_corridas.keys()).set_axis(['Race', 'country', 'Cat.', 'Distance','mt+', 'Time', 'Rank', 'Gender'], axis=1)
    return df_corridas

print(corredor_info(links[0]))
print('-'*100)
print(corredor_corridas(links[0]))


