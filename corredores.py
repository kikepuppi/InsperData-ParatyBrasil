import requests
from bs4 import BeautifulSoup
import pandas as pd
import numpy as np

def infos(uri:str):
    url_corredor = f'https://utmb.world/en/runner/{uri}'
    page = requests.get(url_corredor)
    soup = BeautifulSoup(page.content, 'html.parser')

    list_info = ['Club','Team','Sponsor(s)','Description','Geral','20K','50K','100K','100m']
    dict_about = {i: None for i in list_info}

    for element in soup.find_all('div', class_='runner-more-details_details_element__3rIxF'):
        title = element.find('p', class_='runner-more-details_details_title__RIv1N').text
        if title in dict_about:
            dict_about[title] = element.find('span', class_='runner-more-details_details_content__ZiSil').text

    list_rankings = [i.text if i.text != '-' else None for i in soup.find_all('h2', class_='performance_stat__hcZM_')]
    dict_about.update(zip(['Geral', '20K', '50K', '100K', '100m'], list_rankings))

    return dict_about

def corrida(uri: str):
    url = f'https://utmb.world/utmb-index/races/{uri}'
    page = requests.get(url)
    soup = BeautifulSoup(page.content, 'html.parser')

    lista_infos = ['Title', 'City / Country', 'Day', 'Month', 'Year', 'Race Category', 'Distance', 'Elevation Gain']
    dict_infos = {i: None for i in lista_infos}

    dict_infos['Title'] = soup.find('h1', class_='race-header_rh_race_title__COtYd').text
    infos = soup.find_all('div', class_='race-header_rh_stat_wrapper__1aSTO')
    dict_infos['City / Country'] = infos[0].find('span', class_='race-header_rh_start_point__n5N_D').text
    dict_infos['Day'] = infos[1].find('span', class_='font-18').text.split()[0][:-2]
    dict_infos['Month'] = infos[1].find('span', class_='font-18').text.split()[1]
    dict_infos['Year'] = infos[1].find('span', class_='font-18').text.split()[2]
    dict_infos['Race Category'] = infos[2].find('div',class_='pi-category-logo_container__1zLvC').find('img')['alt']
    dict_infos['Distance'] = infos[3].find('span', class_='font-18').text.split()[0]
    dict_infos['Elevation Gain'] = infos[4].find('span', class_='font-18').text.split()[0]

    return dict_infos

def corredor_corrida(uri: str):
    url = f'https://api.utmb.world/races/{uri}/results?lang=en&offset=0&limit=10000'
    page = requests.get(url)
    return list(page.json()['results'])


def corridas():
    lista_off = np.arange(0, 44982, 20)

    list_corridas = []

    for num in lista_off:
        offset = f'&offset={num}'
        url = f'https://api.utmb.world/search/races-qualifiers?lang=en&dateMin=1999-12-31&dateMax=2025-12-30{offset}'
        page = requests.get(url)
        races_dict = page.json()['races']

        for race_dict in races_dict:
            corrida = {
                "Corrida": race_dict["eventName"],
                "URI": race_dict["uriResults"]
            }
            list_corridas.append(corrida)


    df_corridas = pd.DataFrame(list_corridas)
    return df_corridas

