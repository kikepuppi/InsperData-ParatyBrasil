import requests
from bs4 import BeautifulSoup
import pandas as pd

def corredor_info(uri: str):
    dic = {}
    link = f'https://utmb.world/en/runner/{uri}'
    url = str(link)
    page = requests.get(url, headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome / 86.0.4240.198Safari / 537.36'})
    soup = BeautifulSoup(page.content, 'html.parser')
    dict_about = {i: None for i in ['Club', 'Team', 'Sponsor(s)', 'Website']}
    for i in soup.select('.runner-more-details_details_element__3rIxF'):
        dict_about[i.find('p').text] = i.find('span').text 
    dic[link] = list(dict_about.values()) + [i.text for i in soup.select('.performance_stats_container__Guwj0')[0].find_all('h2')]
    df_info = pd.DataFrame(dic.values(), index=dic.keys()).set_axis(['Club', 'Team', 'Sponsor(s)', 'Website','UTMB Geral','20K','50K','100K','100m'], axis=1)
    return df_info

def corredor_corridas(uri:str):
    url_corredor = f'https://utmb.world/_next/data/AZM8Mw2pZpHJ-hmhE6gko/en/runner/{uri}.json?runner={uri}'
    info = requests.get(url_corredor)
    return pd.DataFrame(info.json()["pageProps"]["results"]["results"])

def infos(uri:str):
    url_corredor = f'https://utmb.world/_next/data/AZM8Mw2pZpHJ-hmhE6gko/en/runner/{uri}.json?runner={uri}'
    info = requests.get(url_corredor)
    dict_about = {"Club":info.json()["pageProps"]["club"],
                  "Team":info.json()["pageProps"]["team"],
                  "Sponsor":info.json()["pageProps"]["sponsor"],
                  "Description":info.json()["pageProps"]["description"],
                  "Website":info.json()["pageProps"]["website"],
                  "Geral":info.json()["pageProps"]["performanceIndexes"][0]["index"],
                  "20K":info.json()["pageProps"]["performanceIndexes"][1]["index"],
                  "50K":info.json()["pageProps"]["performanceIndexes"][2]["index"],
                  "100K":info.json()["pageProps"]["performanceIndexes"][3]["index"],
                  "100m":info.json()["pageProps"]["performanceIndexes"][4]["index"]}
    return dict_about
