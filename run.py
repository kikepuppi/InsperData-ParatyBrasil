from webscraping import Webscraping

def main():
    webscraping = Webscraping()
    create = webscraping.create()
    webscraping.run(create[0], create[1], create[2], create[3], 1000)

if __name__ == '__main__':
    main()