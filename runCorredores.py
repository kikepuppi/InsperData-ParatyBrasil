from corredores import Corredores

def main():
    webscraping = Corredores()
    create = webscraping.create()
    webscraping.run(create[0], create[1], create[2], create[3], 1000)

if __name__ == '__main__':
    main()