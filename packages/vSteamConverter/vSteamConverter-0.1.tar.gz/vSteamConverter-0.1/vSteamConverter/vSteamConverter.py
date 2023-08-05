if __name__ == "__main__":
    class vSteamConverter():
        def gamesById(fileLocation, fileName, extension):
            from threading import Thread
            import requests,json,time

            print('Loading ... This can take a few minutes, we are loading all steam games for you :)')

            fileLocation = str(fileLocation) + "{}".format(fileName + extension)

            file = open(fileLocation, 'w+')

            def jogos(inicio, fim):
                for i in range(inicio, fim, 15):
                    porId = list()
                    dicionarioPorId = dict()
                    temp = list()
                    todosJogos = list()

                    url = "https://store.steampowered.com/contenthub/querypaginated/games/ConcurrentUsers/render/?query=&start={}&count=15&cc=BR&l=brazilian&v=5&".format(i)
                    r = requests.get(url)
                    rJson = (r.json())
                    HTML = (rJson["results_html"])

                    HTML = HTML.split('</a>')

                    for jogo in HTML:
                        temp.append(jogo.split('<div'))

                    for item in temp:
                        games = str(item).split('https')
                        for links in games:
                            if '/app/' in links:
                                inicio = links.find('/app/') + 5
                                links = links[inicio:]
                                fim = links.find('/?')
                                links = links[:fim]

                                temp = links.split('/')
                                id = temp[0]
                                game = temp[1].replace('_', ' ').lstrip(' ')
                                dicionarioPorId = {id: game}

                                porId.append(dicionarioPorId)

                    for ID in porId:
                        file.write('\t' + str(ID) + '\n')

            jogos1 = Thread(target=jogos, args=[0, 1000])
            jogos2 = Thread(target=jogos, args=[1000, 2000])
            jogos3 = Thread(target=jogos, args=[2000, 3000])
            jogos4 = Thread(target=jogos, args=[3000, 4000])
            jogos5 = Thread(target=jogos, args=[4000, 5000])
            jogos6 = Thread(target=jogos, args=[5000, 6000])
            jogos7 = Thread(target=jogos, args=[6000, 7000])
            jogos8 = Thread(target=jogos, args=[7000, 8000])
            jogos9 = Thread(target=jogos, args=[8000, 9000])
            jogos10 = Thread(target=jogos, args=[9000, 10000])
            jogos11 = Thread(target=jogos, args=[10000, 11000])
            jogos12 = Thread(target=jogos, args=[11000, 12000])
            jogos13 = Thread(target=jogos, args=[12000, 12175])

            jogos1.start()
            jogos2.start()
            jogos3.start()
            jogos4.start()
            jogos5.start()
            jogos6.start()
            jogos7.start()
            jogos8.start()
            jogos9.start()
            jogos10.start()
            jogos11.start()
            jogos12.start()
            jogos13.start()

        def idByGames(fileLocation,fileName,extension):
            from threading import Thread
            import requests,json,time


            print("Loading ... This can take a few minutes, we are loading all steam id's for you :)")

            fileLocation = str(fileLocation) + "{}".format(fileName + extension)

            file = open(fileLocation, 'w+')

            def jogos(inicio, fim):
                for i in range(inicio, fim, 15):
                    porJogo = list()
                    dicionarioPorJogo = dict()
                    temp = list()
                    todosJogos = list()

                    url = "https://store.steampowered.com/contenthub/querypaginated/games/ConcurrentUsers/render/?query=&start={}&count=15&cc=BR&l=brazilian&v=5&".format(
                        i)
                    r = requests.get(url)
                    rJson = (r.json())
                    HTML = (rJson["results_html"])

                    HTML = HTML.split('</a>')

                    for jogo in HTML:
                        temp.append(jogo.split('<div'))

                    for item in temp:
                        games = str(item).split('https')
                        for links in games:
                            if '/app/' in links:
                                inicio = links.find('/app/') + 5
                                links = links[inicio:]
                                fim = links.find('/?')
                                links = links[:fim]

                                temp = links.split('/')
                                id = temp[0]
                                game = temp[1].replace('_', ' ').lstrip(' ')
                                dicionarioPorJogo = {game: id}

                                porJogo.append(dicionarioPorJogo)

                    for GAME in porJogo:
                        file.write('\t' + str(GAME) + '\n')

            jogos1 = Thread(target=jogos, args=[0, 1000])
            jogos2 = Thread(target=jogos, args=[1000, 2000])
            jogos3 = Thread(target=jogos, args=[2000, 3000])
            jogos4 = Thread(target=jogos, args=[3000, 4000])
            jogos5 = Thread(target=jogos, args=[4000, 5000])
            jogos6 = Thread(target=jogos, args=[5000, 6000])
            jogos7 = Thread(target=jogos, args=[6000, 7000])
            jogos8 = Thread(target=jogos, args=[7000, 8000])
            jogos9 = Thread(target=jogos, args=[8000, 9000])
            jogos10 = Thread(target=jogos, args=[9000, 10000])
            jogos11 = Thread(target=jogos, args=[10000, 11000])
            jogos12 = Thread(target=jogos, args=[11000, 12000])
            jogos13 = Thread(target=jogos, args=[12000, 12175])

            jogos1.start()
            jogos2.start()
            jogos3.start()
            jogos4.start()
            jogos5.start()
            jogos6.start()
            jogos7.start()
            jogos8.start()
            jogos9.start()
            jogos10.start()
            jogos11.start()
            jogos12.start()
            jogos13.start()
