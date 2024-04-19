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
        self.list_remove = ['name', 'category', 'themeColor', 'themeColorIsDark', 'logoWs', 'url', 'distance', 'elevationGain', 'hasResults', 'startDate', 'startCountry', 'startPlace', 'year', 'level', 'nbStones']
    
    def corrida(self, uri: str):
        
        url = f'https://utmb.world/utmb-index/races/{uri}'
        page = requests.get(url)
        soup = BeautifulSoup(page.content, 'html.parser')

        lista_infos = ['Title', 'City / Country', 'Day', 'Month', 'Year', 'Race Category', 'Distance', 'Elevation Gain']
        dict_infos = {i: None for i in lista_infos}

        try:
            dict_infos['Title'] = soup.find('h1', class_='race-header_rh_race_title__COtYd').text
            infos = soup.find_all('div', class_='race-header_rh_stat_wrapper__1aSTO')
            dict_infos['City / Country'] = infos[0].find('span', class_='race-header_rh_start_point__n5N_D').text
            dict_infos['Day'] = infos[1].find('span', class_='font-18').text.split()[0][:-2]
            dict_infos['Month'] = infos[1].find('span', class_='font-18').text.split()[1]
            dict_infos['Year'] = infos[1].find('span', class_='font-18').text.split()[2]
            dict_infos['Race Category'] = infos[2].find('div',class_='pi-category-logo_container__1zLvC').find('img')['alt']
            dict_infos['Distance'] = infos[3].find('span', class_='font-18').text.split()[0]
            dict_infos['Elevation Gain'] = infos[4].find('span', class_='font-18').text.split()[0]
        except:
            pass

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
    
    def insertCorridas(self, connection, corridas):

        with open('corridas_total.json', 'r') as f:
            list_corridas = list(json.load(f))
            
        for dic in tqdm(list_corridas):  

            for key in self.list_remove:
                dic.pop(key)

            dic.update(self.corrida(dic['uriResults']))

            try:
                stmt = insert(corridas).values(dic)
                stmt.compile()
                connection.execute(stmt)
                connection.commit()
            except:
                pass
            
        
    def create(self):
        connection, corridas = self.createCorridasTable()
        
        return connection, corridas

    def run(self, connection, corridas):
            
            self.insertCorridas(connection, corridas)