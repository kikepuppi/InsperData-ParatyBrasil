from corredorcorrida import CorredorCorrida
import sqlalchemy as db
from tqdm import tqdm

def get_uris():

    engine = db.create_engine('sqlite:///utmb.sqlite')
    connection = engine.connect()
    metadata = db.MetaData()
    corridas = db.Table('corridas', metadata, autoload_with=engine)

    query = db.select(corridas.columns['uri']) 
    ResultProxy = connection.execute(query)
    ResultSet = ResultProxy.fetchall()

    list_result = [result[0].strip() for result in ResultSet]

    query = db.select(corridas.columns['id-corrida']) 
    ResultProxy = connection.execute(query)
    ResultSet = ResultProxy.fetchall()

    list_ids = [result[0] for result in ResultSet]

    return list_result, list_ids
    

def main():

    uris, ids = get_uris()

    corredorcorrida = CorredorCorrida()
    create = corredorcorrida.create()

    for i,uri in enumerate(tqdm(uris)):
        id = ids[i]
        corredorcorrida.run(create[0], create[1], uri, id)


if __name__ == '__main__':
    main()