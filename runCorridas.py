from corridas import Corridas

def main():
    webscraping = Corridas()
    create = webscraping.create(5)
    webscraping.run(create[0], create[1], create[2])

if __name__ == '__main__':
    main()