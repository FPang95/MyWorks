# functions for webscraping
from bs4 import BeautifulSoup as soup
import numpy as np


def get_teams(webpage, owner, tier):
    # function that takes the webpage, team owner and tier as arguments, returns list of sorted pokemon team
    # non-random battles have teams shown in the start
    if "Random" not in tier:
        teams = webpage.findAll('div', {"class": "chat battle-history"})
        clean_team = teams[owner].em.text.strip("-*").split(" / ")

    # random battles don't reveal pokemon unlessed used. This will grab all pokemon that have been revealed
    else:
        team = []
        moves = webpage.findAll('div', {"class": "battle-history"})
        for poke in moves:
            if (owner == 0) and ("sent out" in poke.text):
                poke = poke.strong.text
                poke = poke.strip("()!")
                team.append(poke)
            elif (owner == 1) and ("Go!" in poke.text):
                poke = poke.strong.text
                poke = poke.strip("()!")
                team.append(poke)

        #remove duplicates of pokemon in team
        clean_team = list(set(team))

    clean_team.sort()

    return clean_team


def winOrLose(webpage):
    # function that returns outcome of the match
    winner = webpage.findAll('div', {"class": "battle-history"})[-1].strong.text
    if "Data Tester" in winner or "PokeLog" in winner:
        return "Win"
    else:
        return "Loss"


def getElo(webpage, tier):
    # function that will get rank change if one is shown
    if "Unrated" not in tier:
        rankings = webpage.findAll('div', {"class":"chat"})[-1].text.split(": ")[-1]
        ratings = webpage.findAll('div', {"class": "chat"})
        for elo in ratings:
            if ("Data Tester's rating" in elo.text) or ("PokeLog's rating" in elo.text):
                return elo.text.split(": ")[-1]

    # if unranked match or rank could not be obtained, returns nan
        if rankings[0]!="1" and rankings[0]!="2":
            return np.nan
    else:
        return np.nan


def pokemonDown(webpage):
    # counts number of pokemon that have been defeated by each person
    moves = webpage.findAll('div', {"class": "battle-history"})
    mypokefaints = 0
    opppokefaints = 0
    for move in moves:
        if len(move["class"])==1:
            if "fainted" in move.text:
                if "opposing" in move.text:
                    opppokefaints+=1
                else:
                    mypokefaints+=1

    return [mypokefaints, opppokefaints]



def moveList(webpage):
    # makes and returns list of all moves used in game
    moves = webpage.findAll('div', {"class": "battle-history"})
    total_moves=[]
    for move in moves:
        if len(move["class"])==1:
            if " used " in move.text:
                action = move.text.split(" used ")[-1]
                total_moves.append(action[:len(action)-1])

    # alphabetizes the moves
    total_moves.sort()
    return total_moves


def efficacy(webpage):
    # tracks how many moves were super effective and not very effective
    moves = webpage.findAll('div', {"class": "battle-history"})
    supercount = 0
    ineffcount = 0
    for move in moves:
        if len(move["class"])==1:
            if "It's not very effective" in move.text:
                ineffcount += 1
            elif "It's super effective" in move.text:
                supercount += 1

    return [ineffcount, supercount]


def moveType(webpage, statuslist):
    offense = 0
    status = 0
    moves = webpage.findAll('div', {"class": "battle-history"})
    for move in moves:
        if len(move["class"])==1:
            if "used" in move.text:
                if move.strong != None:
                    if move.strong.text in statuslist:
                        status += 1

                    elif move.strong.text not in statuslist:
                        offense += 1

    return [offense, status]