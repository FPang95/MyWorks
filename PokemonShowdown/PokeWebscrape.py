import re, os
from bs4 import BeautifulSoup as soup
from urllib.request import urlopen as uReq
import numpy as np
import PokeFunctions as pf
import pandas as pd

# name: Pokelog, password: DataTest

path = '/Users/frankpang/PycharmProjects/PokeBattles/Pokelog/'
files = []
for r, d, f in os.walk(path):
    for file in f:
        if '.html' in file:
            files.append(file)


filename = "Poke_log.csv"
f = open(filename, 'w')
headers = "Tier,Win/Loss,My Team/Pokemon Revealed,Opponent's Team/Pokemon Revealed,My Team Typing," \
          "Opponent's Team Typing,Own Pokemon Down,Opponent Pokemon Down,My Moves Used,Opponent's Moves Used," \
          "Super effective,Not very effective,My Attacking Moves,My Status Moves,Opponent's Attacking Moves," \
          "Opponent's Status Moves,My Avg Total Stats,My Avg HP,My Avg Atk,My Avg Def,My Avg SpAtk," \
          "My Avg SpDef,My Avg Speed,Opponent Avg Total Stats,Opponent Avg HP,Opponent Avg Atk," \
          "Opponent Avg Def,Opponent Avg SpAtk,Opponent Avg SpDef, Opponent Avg Speed,Turns,Rank,Rank Range\n"
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

typing_df = pd.read_excel("Pokemon_list.xlsx")

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

    elorange = pf.binRankings(str(elo))

    myteamlist = pf.get_teams(page_soup, 0, tier)
    opteamlist = pf.get_teams(page_soup, 1, tier)
    # gives teams
    myteam = '|'.join(myteamlist)
    opteam = '|'.join(opteamlist)

    mytyping = '|'.join(pf.getTypings(typing_df, myteamlist))
    optyping = '|'.join(pf.getTypings(typing_df, opteamlist))

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
    my_moves_list = "|".join(pf.moveList(page_soup, 0))
    opp_moves_list = "|".join(pf.moveList(page_soup, 1))

    MyAvgTotal,  MyAvgHP, MyAvgAttack, MyAvgDefense, MyAvgSpAtk, MyAvgSpDef, MyAvgSpeed = pf.baseStats(typing_df, myteamlist)
    OpAvgTotal, OpAvgHP, OpAvgAttack, OpAvgDefense, OpAvgSpAtk, OpAvgSpDef, OpAvgSpeed = pf.baseStats(typing_df, opteamlist)

    # move_counter = {x: total_moves.count(x) for x in total_moves}
    # str_counter = str(move_counter)
    # new_counter = str_counter.replace(", ", " | ")

    f.write(tier + "," + outcome + "," + myteam + "," + opteam + "," + mytyping + "," + optyping + "," +
            str(own_poke_faints) + "," + str(opp_poke_faints) + "," + my_moves_list + "," + opp_moves_list + ","
            + str(effective) + "," + str(ineffective) + "," + str(myoffense) + "," + str(mystatus) + "," +
            str(oppoffense) + "," + str(oppstatus) + "," + str(MyAvgTotal).strip("[]") + "," + str(MyAvgHP).strip("[]")
            + "," + str(MyAvgAttack).strip("[]") + "," + str(MyAvgDefense).strip("[]") + "," +
            str(MyAvgSpAtk).strip("[]") + "," + str(MyAvgSpDef).strip("[]") + "," + str(MyAvgSpeed).strip("[]") + ","
            + str(OpAvgTotal).strip("[]") + "," + str(OpAvgHP).strip("[]") + "," + str(OpAvgAttack).strip("[]")
            + "," + str(OpAvgDefense).strip("[]") + "," + str(OpAvgSpAtk).strip("[]") + "," +
            str(OpAvgSpDef).strip("[]") + "," + str(OpAvgSpeed).strip("[]") + "," + str(turns) + "," + str(elo)
            + "," + str(elorange) + "\n")

f.close()
