import requests
from bs4 import BeautifulSoup
import pandas as pd
import json
import warnings
warnings.filterwarnings('ignore')
import sqlalchemy as db
from sqlalchemy import insert
from tqdm import tqdm

class Webscraping:

    def __init__(self):

        self.url = f'https://utmb.world/utmb-index'
        self.url_utmb_brazil = 'https://api.utmb.world/search/runners?category=general&sex=&ageGroup=&nationality=BR&limit=1000000&offset=0&search='

    def infos(self, uri:str):
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
    
    def runnersBr(self):

        runners = requests.get(self.url_utmb_brazil)
        runners_br_df = pd.DataFrame(runners.json() ["runners"])
        runners_br_df = runners_br_df.drop(columns=['picture', 'ip'])
        return runners_br_df, runners

    def createRunnersTable(self):
        engine = db.create_engine('sqlite:///utmb.sqlite', connect_args={'timeout': 30})
        connection = engine.connect()
        metadata = db.MetaData()

        corredores = db.Table('corredores', metadata,
                        db.Column('id', db.Integer(), primary_key=True),
                        db.Column('ageGroup', db.String(255)),
                        db.Column('fullname', db.String(255)),
                        db.Column('uri', db.String(255)),
                        db.Column('nationality', db.String(255)),
                        db.Column('sex', db.String(255)),
                        db.Column('Club', db.String(255)),
                        db.Column('Team', db.String(255)),
                        db.Column('Sponsor(s)', db.String(255)),
                        db.Column('Description', db.String(255)),
                        db.Column('Geral', db.String(255)),
                        db.Column('20K', db.String(255)),
                        db.Column('50K', db.String(255)),
                        db.Column('100K', db.String(255)),
                        db.Column('100m', db.String(255)))
        
        metadata.create_all(engine)
        query = db.insert(corredores)
        connection.execute(query)

        return connection, corredores

    def insertRunners(self, runners_br_df, runners, connection, corredores, size):
        
        for i in tqdm(range (size)):    
            dic = runners.json()["runners"][i]
            dic.pop('picture')
            dic.pop('ip')
            dic.update(self.infos(runners_br_df['uri'][i]))
            stmt = insert(corredores).values(dic)
            stmt.compile()
            connection.execute(stmt)
            connection.commit()

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

    def corredorCorrida(uri: str):

        url = f'https://api.utmb.world/races/{uri}/results?lang=en&offset=0&limit=10000'
        page = requests.get(url)
        return list(page.json()['results'])
    
    def create(self):
        runners_br_df, runners = self.runnersBr()
        connection, corredores = self.createRunnersTable()
        return runners_br_df, runners, connection, corredores

    def run(self, runners_br_df, runners, connection, corredores, size):
            
            self.insertRunners(runners_br_df, runners, connection, corredores, size)

