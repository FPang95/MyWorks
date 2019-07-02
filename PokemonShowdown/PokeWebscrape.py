import re, os
from bs4 import BeautifulSoup as soup
from urllib.request import urlopen as uReq
import numpy as np
import PokeFunctions as pf

# name: Pokelog, password: DataTest

path = '/Users/frankpang/PycharmProjects/PokeBattles/Pokelog/'
files = []
for r, d, f in os.walk(path):
    for file in f:
        if '.html' in file:
            files.append(file)


filename = "Poke_log.csv"
f = open(filename, 'w')
headers = "Tier,My Team/Pokemon Revealed,Opponent's Team/Pokemon Revealed,Win/Loss,Own Pokemon Down,Opponent " \
          "Pokemon Down,My Moves Used,Opponent's Moves Used,Super effective,Not very effective," \
          "My Attacking Moves,My Status Moves,Opponent's Attacking Moves,Opponent's Status Moves,Turns,Rank\n"
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


for pokefile in files:
    my_url = 'file:///Users/frankpang/PycharmProjects/PokeBattles/Pokelog/'+pokefile

    # opening up connection and grabbing the page
    uClient = uReq(my_url)
    page_html = uClient.read()
    uClient.close()

    page_soup = soup(page_html, "html.parser")

    # gives tier
    tier = page_soup.find('div', {"class":"wrapper replay-wrapper"}).h1.strong.string

    moves = page_soup.findAll('div',{"class":"battle-history"})

    # gives win or loss
    outcome = pf.winOrLose(page_soup)


    # gives rank
    elo = pf.getElo(page_soup, tier)

    # gives teams
    myteam = '|'.join(pf.get_teams(page_soup, 0, tier))
    opteam = '|'.join(pf.get_teams(page_soup, 1, tier))

    # gives turns
    turns = len(page_soup.findAll('h2',{"class":"battle-history"}))

    # gives how many pokemon on each side were defeated
    own_poke_faints, opp_poke_faints = pf.pokemonDown(page_soup)

    # gives number of effective and ineffective moves used
    ineffective, effective = pf.efficacy(page_soup)

    # gives type of moves used
    myoffense, mystatus = pf.moveType(page_soup, status_move, 0)

    oppoffense, oppstatus = pf.moveType(page_soup, status_move, 1)

    # give comprehensive list of all moves used
    my_moves_list = "|".join(pf.moveList(page_soup,0))
    opp_moves_list = "|".join(pf.moveList(page_soup,1))

    #move_counter = {x: total_moves.count(x) for x in total_moves}
    #str_counter = str(move_counter)
    #new_counter = str_counter.replace(", ", " | ")

    f.write(tier + "," + myteam + "," + opteam + "," + outcome + "," + str(own_poke_faints) + "," +
            str(opp_poke_faints) + "," + my_moves_list + "," + opp_moves_list + "," + str(effective) +
            "," + str(ineffective) + "," + str(myoffense) + "," + str(mystatus) + "," + str(oppoffense)
            + "," + str(oppstatus) + "," + str(turns) + "," + str(elo) + "\n")

f.close()
