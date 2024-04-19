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


class CorredorCorrida:

    def __init__(self):
        pass

    def corredorcorrida(self, uri):
        url = f'https://api.utmb.world/races/{uri}/results?lang=en&offset=0&limit=10000'
        response = requests.get(url)

        if response.status_code == 200:
            results = response.json().get('results', [])
            
            id_corrida = uri.split('.')[0]
            
            list_corrida = [{
                'id_corrida': id_corrida,
                'id_corredor': result.get('runnerUri', '').split('.')[0],
                'time': result.get('time', ''),
                'rank': result.get('rank', '')
            } for result in results]
            
            return list_corrida
        
        else:
            print(f"Failed to fetch data for {uri}. Status code: {response.status_code}")
            return []
        
    def createCorredorCorridaTable(self):

        engine = db.create_engine('sqlite:///utmb.sqlite', connect_args={'timeout': 30})
        connection = engine.connect()
        metadata = db.MetaData()

        corredorcorrida = db.Table('corredor-corrida', metadata,
                        db.Column('id-corrida', db.Integer(), primary_key=True),
                        db.Column('id-corredor', db.Integer(), primary_key=True),
                        db.Column('time', db.String(255)),
                        db.Column('rank', db.String(255)))
        
        metadata.create_all(engine)

        return connection, corredorcorrida

    def insertCorredorCorrida(self, connection, corredorcorrida, list_corrida):

        for corredor in tqdm(list_corrida):

            try:
                stmt = insert(corredorcorrida).values(corredor)
                stmt.compile()
                connection.execute(stmt)
                connection.commit()
            except:
                pass

    def create(self):

        connection, corredorcorrida = self.createCorredorCorridaTable()
        return connection, corredorcorrida
    
    def run(self, connection, corredorcorrida, uri):
    
        list_corrida = self.corredorcorrida(uri)
        self.insertCorredorCorrida(connection, corredorcorrida, list_corrida)

