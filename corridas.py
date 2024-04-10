import requests
from bs4 import BeautifulSoup
import pandas as pd
import json
import warnings
warnings.filterwarnings('ignore')
import sqlalchemy as db
from sqlalchemy import insert
from tqdm import tqdm
import numpy as np

class Corridas:

    def __init__(self):
        pass

    def corridas_total(self, size):
        lista_off = np.arange(0, size, 20)

        list_corridas = []

        for num in lista_off:
            offset = f'&offset={num}'
            url = f'https://api.utmb.world/search/races-qualifiers?lang=en&dateMin=1999-12-31&dateMax=2025-12-30{offset}'
            page = requests.get(url)
            races_dict = page.json()['races']

            for race_dict in races_dict:
                corrida = {
                    "id": race_dict['id'],
                    "Corrida": race_dict["eventName"],
                    "uri": race_dict["uriResults"]
                }
                list_corridas.append(corrida)

        return list_corridas
    
    def corrida(self, uri: str):
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
    
    def createCorridasTable(self):
        engine = db.create_engine('sqlite:///utmb.sqlite', connect_args={'timeout': 30})
        connection = engine.connect()
        metadata = db.MetaData()

        corridas = db.Table('corridas', metadata,
                        db.Column('id', db.Integer(), primary_key=True),
                        db.Column('Corrida', db.String(255)),
                        db.Column('uri', db.String(255)),
                        db.Column('Title', db.String(255)),
                        db.Column('City / Country', db.String(255)),
                        db.Column('Day', db.String(255)),
                        db.Column('Month', db.String(255)),
                        db.Column('Year', db.String(255)),
                        db.Column('Race Category', db.String(255)),
                        db.Column('Distance', db.String(255)),
                        db.Column('Elevation Gain', db.String(255)))
        
        metadata.create_all(engine)

        return connection, corridas
    
    def insertCorridas(self, list_corridas, connection, corridas):

        for dic in tqdm(list_corridas):    

            dic.update(self.corrida(dic['uri']))

            stmt = insert(corridas).values(dic)
            stmt.compile()
            connection.execute(stmt)
            connection.commit()
        
    def create(self, size):
        list_corridas = self.corridas_total(size)
        connection, corridas = self.createCorridasTable()
        
        return list_corridas, connection, corridas

    def run(self, list_corridas, connection, corridas):
            
            self.insertCorridas(list_corridas, connection, corridas)