from csvDatabaseManager import getCardholderID
from webScrapeFunctions import getPlayersBday
from galileoRequestFunctions import createCardholder
from csvDatabaseManager import addToDatabaseCSV
from csvDatabaseManager import coachInDatabaseID
from galileoRequestFunctions import getCardHolderAccountId
from galileoRequestFunctions import transferMoney
from galileoRequestFunctions import getPlayerCurrentBalance
from csvDatabaseManager import getDataFrame


def createPlayer(nameString):
    tempID = getCardholderID(nameString)
    if tempID is not None:
        print("player already found with id: " + str(tempID))
        return tempID
    dobInput = getPlayersBday(nameString)
    if dobInput != "ErrorPlayerNotCurrent" and dobInput != "ErrorNotFound":
        tempID = createCardholder(nameString, dobInput)
        addToDatabaseCSV(tempID, nameString, "player")


def rewardCoach():
    coachID = coachInDatabaseID()
    coachAccountID = getCardHolderAccountId(coachID)
    if coachAccountID is None:
        return
    winAmount = 5
    transferMoney(10568, coachAccountID, winAmount)
    print("successfully paid coach $" + str(winAmount) + " for winning")


# def playerPaysCoach(playerAccountID, amountOwed):
#     coachID = coachInDatabaseID()
#     if coachID is None:
#         print("Coach does not exist in csv database")
#         return
#     coachAccountID = getCardHolderAccountId(coachID)
#     if coachAccountID is None:
#         print("Coach does not exist in Galileo dashboard")
#         return
#     transferMoney(playerAccountID, coachAccountID, amountOwed)


def playerMakesMoney(playerCardholderID, amountToTransfer):
    playerAccountID = getCardHolderAccountId(playerCardholderID)
    if playerAccountID is None:
        return
    transferMoney(10568, playerAccountID, amountToTransfer)

# NEVER USED COULDNT GET BACK TO MAIN ACCOUNT
def playerPaysBackOwners(playerCardholderID, amountOwed):
    if (getPlayerCurrentBalance(playerCardholderID) - amountOwed) >= 0:
        transferMoney(getCardHolderAccountId(playerCardholderID), 10568, amountOwed)
    else:
        print("Player does not have enough to pay the owners back")


def playerPaysCoachForTurnovers(playerCardholderID, amountOwed):
    if getCardHolderAccountId(playerCardholderID) is None:
        return
    if (getPlayerCurrentBalance(playerCardholderID) - amountOwed) >= 0:
        coachID = coachInDatabaseID()
        if coachID is None:
            print("Coach does not exist in csv database")
            return
        coachAccountID = getCardHolderAccountId(coachID)
        if coachAccountID is None:
            print("Coach does not exist in Galileo dashboard")
            return
        transferMoney(getCardHolderAccountId(playerCardholderID), coachAccountID, amountOwed)
    else:
        print("Player does not have enough to pay the coach for turnovers")


def showCoachFromDatabase():
    df = getDataFrame()
    for index, row in df.iterrows():
        if row['player/coach'] == 'coach':
            print(row['name'])

def loopThroughPlayersInDF():
    df = getDataFrame()
    for index, row in df.iterrows():
        if row['player/coach'] == 'player':
            print(row['name'])