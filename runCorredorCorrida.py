from corredorcorrida import CorredorCorrida
import requests
import sqlalchemy as db

def get_uris():

    engine = db.create_engine('sqlite:///utmb.sqlite')
    connection = engine.connect()
    metadata = db.MetaData()
    corridas = db.Table('corredores', metadata, autoload_with=engine)

    query = db.select(corridas.columns['uri']) 
    ResultProxy = connection.execute(query)
    ResultSet = ResultProxy.fetchall()

    list_result = [result[0].strip() for result in ResultSet]

    return list_result
    


def main():

    uris = get_uris()

    corredorcorrida = CorredorCorrida()
    create = corredorcorrida.create()

    for uri in uris:
        corredorcorrida.run(create[0], create[1], uri)


if __name__ == '__main__':
    main()