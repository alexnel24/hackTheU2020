from galileoRequestFunctions import refresh
from comboFunctions import showCoachFromDatabase
from comboFunctions import loopThroughPlayersInDF
from comboFunctions import createPlayer
from webScrapeFunctions import validGameDate
from webScrapeFunctions import wonGame
from comboFunctions import rewardCoach
from csvDatabaseManager import getDataFrame
from webScrapeFunctions import playerAmountEarnedOrLost
from comboFunctions import playerMakesMoney
from galileoRequestFunctions import getCardHolderAccountId
from webScrapeFunctions import playerOwesCoach
from comboFunctions import playerPaysCoachForTurnovers


def killProgram():
    exit()


def showOptions():
    print("'exit' - kills program")
    print("'options' - shows available commands")
    print("'refresh' - refreshes your Galileo authorization code")
    print("'listTeam' - displays players and coach who have Galileo cards")
    print("'trackPlayer' - add a player to be tracked and makes them a Galileo cardholder")
    print("'payTeam' - initiate payment through Galileo to players and coach cards")

    print("")


def requestRefresh():
    refresh()


def showTeam():
    print("")
    print("Current Coach:")
    showCoachFromDatabase()
    print("")
    print("Players:")
    loopThroughPlayersInDF()


def trackPlayer():
    getPlayerString = input("Player's name: ")
    print("processing")
    createPlayer(getPlayerString)

def processPay():
    getDate = input("Date of Game [format = 'YYYY-MM-DD': ")
    if len(getDate) != 10:
        print("improper date format")
        return
    if len(getDate.split("-")) != 3:
        print("improper date format")
        return
    if len(getDate.split("-")[0]) != 4 or len(getDate.split("-")[1]) != 2 or len(getDate.split("-")[2]) != 2:
        print("improper date format")
        return
    print("processing")

    # VALID DATE?
    if validGameDate(getDate) is False:
        return

    if wonGame(getDate):
        print("The Jazz won on " + getDate)
        rewardCoach()
    else:
        print("The Jazz lost on " + getDate)

    df = getDataFrame()
    for item, row in df.iterrows():
        if row['player/coach'] == 'player':
            owedToPlayer = playerAmountEarnedOrLost(row['name'], getDate)
            if owedToPlayer != 0:
                playerMakesMoney(row['id'], owedToPlayer)
            amountOwedToCoach = playerOwesCoach(row['name'], getDate)
            if amountOwedToCoach != 0:
                playerPaysCoachForTurnovers(row['id'], amountOwedToCoach)



