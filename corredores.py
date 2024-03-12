import requests
from bs4 import BeautifulSoup
import pandas as pd

# def corridas(uri:str):
#     url_corredor = f'https://utmb.world/_next/data/AZM8Mw2pZpHJ-hmhE6gko/en/runner/{uri}.json?runner={uri}'
#     info = requests.get(url_corredor)
#     return (info.json()["pageProps"]["results"]["results"])

def infos(uri:str):
    url_corredor = f'https://utmb.world/en/runner/{uri}'
    page = requests.get(url_corredor)
    soup = BeautifulSoup(page.content, 'html.parser')
    list_info = ['Club','Team','Sponsor(s)','Description','Geral','20K','50K','100K','100m']
    element = soup.find_all('div', class_='runner-more-details_details_element__3rIxF')

    dict_about = {i: None for i in list_info}
    for i in element:
        if i.find('p', class_='runner-more-details_details_title__RIv1N').text in list_info:
            dict_about[i.find('p', class_='runner-more-details_details_title__RIv1N').text] = i.find('span', class_='runner-more-details_details_content__ZiSil').text

    list_rankings = [i.text if i.text != '-' else None for i in soup.find_all('h2', class_='performance_stat__hcZM_')]
    dict_about['Geral'] = list_rankings[0]
    dict_about['20K'] = list_rankings[1]
    dict_about['50K'] = list_rankings[2]
    dict_about['100K'] = list_rankings[3]
    dict_about['100m'] = list_rankings[4]

    return dict_about
