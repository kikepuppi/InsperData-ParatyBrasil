from corridas import Corridas

def main():
    webscraping = Corridas()
    create = webscraping.create()
    webscraping.run(create[0], create[1])

# if __name__ == '__main__':
#     main()


def to_csv():
    webscraping = Corridas()
    webscraping.to_csv()


to_csv()
