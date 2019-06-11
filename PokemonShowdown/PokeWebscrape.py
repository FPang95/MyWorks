import re, os
from bs4 import BeautifulSoup as soup
from urllib.request import urlopen as uReq

#Pokelog, password: DataTest

path = '/Users/frankpang/PycharmProjects/PokeBattles/Pokelog/'
files = []
for r, d, f in os.walk(path):
    for file in f:
        if '.html' in file:
            files.append(file)


filename = "Poke_log.csv"
f = open(filename, 'w')
headers = "Tier, My Team/Pokemon Revealed, Opponent's Team/Pokemon Revealed, Win/Loss, Own Pokemon Down, Opponent " \
          "Pokemon Down, Moves used, Super effective, Not very effective, Total Moves, Attacking Moves, " \
          "Status Moves, Turns, Rank\n"
f.write(headers)

###
# Makes list of all non-offense moves
status_url = 'file:///Users/frankpang/PycharmProjects/PokeBattles/Status%20move%20-%20Bulbapedia,' \
             '%20the%20community-driven%20Poke%CC%81mon%20encyclopedia.html'
uClient = uReq(status_url)
status_html = uClient.read()
uClient.close()

page_soup = soup(status_html, "html.parser")
moves = page_soup.find_all('td',{"width":"100px"})

status_move = [x.text.strip() for x in moves]
###


for myfile in files:
    my_url = 'file:///Users/frankpang/PycharmProjects/PokeBattles/Pokelog/'+myfile

    # opening up connection and grabbing the page
    uClient = uReq(my_url)
    page_html = uClient.read()
    uClient.close()

    page_soup = soup(page_html, "html.parser")

    #gives tier
    tier = page_soup.find('div', {"class":"wrapper replay-wrapper"}).h1.strong.string
    #name1 = page_soup.findAll('div', {"class":"chat"})[0].text
    #name2 = page_soup.findAll('div', {"class":"chat"})[1].text

    winner = page_soup.findAll('div', {"class": "battle-history"})[-1].strong.text
    moves = page_soup.find_all('div',{"class":"battle-history"})

    if "Data Tester" in winner or "PokeLog" in winner:
        outcome = "Win"
    else:
        outcome = "Loss"


    #gives
    if "Unrated" not in tier:
        rankings = page_soup.findAll('div', {"class":"chat"})[-1].text.split(": ")[-1]
        ratings = page_soup.findAll('div', {"class": "chat"})
        for elo in ratings:
            if ("Data Tester's rating" in elo.text) or ("PokeLog's rating" in elo.text):
                elo = elo.text.split(": ")[-1]
                break

        if rankings[0]!="1" and rankings[0]!="2":
            elo = "N/A"

        if "Random" not in tier:
            teams = page_soup.findAll('div', {"class": "chat battle-history"})

            myteam = teams[0].em.text.split(" / ")
            opteam = teams[1].em.text.split(" / ")
            myteam.sort()
            opteam.sort()
            myteam = '|'.join(myteam)
            opteam = '|'.join(opteam)

        else:
            myteam = []
            opteam = []
            for poke in moves:
                if "sent out" in poke.text:
                    poke = poke.text.split()
                    poke = poke[-1].strip("()!")
                    opteam.append(poke)
                elif "Go!" in poke.text:
                    poke = poke.text.split()
                    poke = poke[-1].strip("()!")
                    myteam.append(poke)

            myteam = list(set(myteam))
            opteam = list(set(opteam))
            myteam.sort()
            opteam.sort()
            myteam = '|'.join(myteam)
            opteam = '|'.join(opteam)
    else:
        myteam = []
        opteam = []
        for poke in moves:
            if "sent out" in poke.text:
                poke = poke.text.split()
                poke = poke[-1].strip("()!")
                opteam.append(poke)
            elif "Go!" in poke.text:
                poke = poke.text.split()
                poke = poke[-1].strip("()!")
                myteam.append(poke)

        myteam = list(set(myteam))
        opteam = list(set(opteam))
        myteam.sort()
        opteam.sort()
        myteam = '|'.join(myteam)
        opteam = '|'.join(opteam)
        elo = "N/A"


    turns = len(page_soup.findAll('h2',{"class":"battle-history"}))

    # only if not random battle or unrated random battle
    #for line in moves:
    #    print(team.em)

    #for team in teams:
    #    gang = team.em.text.split(" / ")
    #    gang.sort()

    own_poke_faints = 0
    opp_poke_faints = 0

    ineffective = 0
    effective = 0

    offense = 0
    status = 0

    total_moves = []

    for move in moves:
        if len(move["class"])==1:
            if "fainted" in move.text:
                if "opposing" in move.text:
                    opp_poke_faints+=1
                else:
                    own_poke_faints+=1
            if " used " in move.text:
                action = move.text.split(" used ")[-1]
                total_moves.append(action[:len(action)-1])

            if "It's not very effective" in move.text:
                ineffective+=1
            elif "It's super effective" in move.text:
                effective+=1

            if "used" in move.text:
                if move.strong != None:
                    if move.strong.text in status_move:
                        status += 1

                    elif move.strong.text not in status_move:
                        offense += 1

    totalmoves = status + offense
    move_counter = {x: total_moves.count(x) for x in total_moves}
    str_counter = str(move_counter)
    new_counter = str_counter.replace(", ", " | ")



    f.write(tier + "," + myteam + "," + opteam + "," + outcome + "," + str(own_poke_faints) + "," +
            str(opp_poke_faints) + "," + new_counter + "," + str(effective) + "," + str(ineffective) + "," +
            str(totalmoves) + "," + str(offense) + "," + str(status) + "," + str(turns) + "," + str(elo) + "\n")


f.close()
