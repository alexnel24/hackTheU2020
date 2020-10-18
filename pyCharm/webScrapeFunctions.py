import urllib.request
from bs4 import BeautifulSoup
import pandas as pd
from datetime import date, datetime, timedelta
import os, ssl
import html5lib
if (not os.environ.get('PYTHONHTTPSVERIFY', '') and
getattr(ssl, '_create_unverified_context', None)):
    ssl._create_default_https_context = ssl._create_unverified_context


def getPlayersBday(stringNameParam):
    url = "https://www.basketball-reference.com/teams/UTA/2020.html"

    with urllib.request.urlopen(url) as response:
        html = response.read()
        html = html.decode('utf-8')

    with open('playersAtEndOfSeason.html', 'w') as new_file:
        new_file.write(html)

    soup = BeautifulSoup(open('playersAtEndOfSeason.html'), 'html5lib')
    birthdayLook = soup.find_all('td')

    countBool = False
    count = 0
    for tag in birthdayLook:
        if countBool:
            count += 1
            if count == 4:
                try:
                    dateAttempt = datetime.strptime(tag.string, "%B %d, %Y")
                    return dateAttempt.strftime("%Y-%m-%d")
                except:
                    print("Player is not currently on the roster or in the top 15 of players")
                    return "ErrorPlayerNotCurrent"
        if tag.string == stringNameParam:
            countBool = True
    print("Player could not be found, check https://www.basketball-reference.com/teams/UTA/2020.html to verify")
    return "ErrorNotFound"


def validGameDate(dateString):
    url = "https://www.basketball-reference.com/players/m/mitchdo01/gamelog/2020/"

    with urllib.request.urlopen(url) as response:
        html = response.read()
        html = html.decode('utf-8')

    with open('DonovanGameLog2019to2020.html', 'w') as new_file:
        new_file.write(html)

    soup = BeautifulSoup(open('DonovanGameLog2019to2020.html'), 'html5lib')

    gameTags = soup.find_all('td')

    for tag in gameTags:
        # print(tag)
        # print(tag.string)
        for k, v in tag.attrs.items():
            # print(k)
            # print(v)
            if v == 'date_game':
                if tag.string == dateString:
                    return True
    print("no game found for date: " + dateString)
    print("MUST BE 2019-2020 REGULAR SEASON GAME FOR UTAH JAZZ")
    return False

def wonGame(dateString):
    if not validGameDate(dateString):
        print("no game was found on this date")
        return None

    url = "https://www.basketball-reference.com/players/m/mitchdo01/gamelog/2020/"

    with urllib.request.urlopen(url) as response:
        html = response.read()
        html = html.decode('utf-8')

    with open('DonovanGameLog2019to2020.html', 'w') as new_file:
        new_file.write(html)

    soup = BeautifulSoup(open('DonovanGameLog2019to2020.html'), 'html5lib')

    gameTags = soup.find_all('td')

    booleanFoundCorrectDate = False

    for tag in gameTags:

        for k, v in tag.attrs.items():
            if v == 'date_game':
                if tag.string == dateString:
                    booleanFoundCorrectDate = True
                    # print("*****FOUND DATE!*****")
                if tag.string != dateString:
                    booleanFoundCorrectDate = False
            if booleanFoundCorrectDate:
                if v == 'game_result':
                    result =  tag.string
                    if result.split(' ')[0] == 'W':
                        return True
                    elif result.split(' ')[0] == 'L':
                        return False
                    else:
                        return None
    return None

def playerAmountEarnedOrLost(playerNameString, gameDateString):
    url = "https://www.basketball-reference.com/players/"
    initial = playerNameString.split(" ")[1][0].lower()
    letterurl = url + "{}/".format(initial)

    with urllib.request.urlopen(letterurl) as response:
        html = response.read()
        html = html.decode('utf-8')
    with open('playersWithInitial.html', 'w') as new_file:
        new_file.write(html)
    soup = BeautifulSoup(open('playersWithInitial.html'), 'html5lib')

    playerLocate = soup.find_all('a', href=True)
    for tag in playerLocate:
        if tag.string == playerNameString:
            indHTML = tag.get('href')

    playerPage = "https://www.basketball-reference.com" + indHTML

    with urllib.request.urlopen(playerPage) as response:
        html = response.read()
        html = html.decode('utf-8')
    with open('playerHTML.html', 'w') as new_file:
        new_file.write(html)
    soup = BeautifulSoup(open('playerHTML.html'), 'html5lib')

    yearsPlayed = soup.find_all('a')

    for tag in yearsPlayed:
        if tag.string == '2019-20':
            if 'gamelog' in tag.get('href'):
                finalHTML = "https://www.basketball-reference.com" + tag.get('href')

    with urllib.request.urlopen(finalHTML) as response:
        html = response.read()
        html = html.decode('utf-8')
    with open('gamelog.html', 'w') as new_file:
        new_file.write(html)
    soup = BeautifulSoup(open('gamelog.html'), 'html5lib')

    gameTags = soup.find_all('td')

    booleanFoundCorrectDate = True
    toReturn = 0
    for tag in gameTags:
        for k, v in tag.attrs.items():
            if v == 'date_game':
                if tag.string == gameDateString:
                    booleanFoundCorrectDate = True
                if tag.string != gameDateString:
                    booleanFoundCorrectDate = False
            if v == 'reason' and booleanFoundCorrectDate:
                print(playerNameString + " did not play in the game on " + gameDateString)
                print("")
                return 0
            if booleanFoundCorrectDate:
                if v == 'pts':
                    print(playerNameString + " gets $" + str(tag.string) + " for scoring on " + gameDateString)
                    toReturn += int(tag.string)
                if v == 'pf':
                    print(playerNameString + " loses $" + str(tag.string) + " for fouls on " + gameDateString)
                    toReturn -= int(tag.string)
                if v == 'trb':
                    print(playerNameString + " gets $" + str(tag.string) + " for rebounds on " + gameDateString)
                    toReturn += int(tag.string)
                if v == 'ast':
                    print(playerNameString + " gets $" + str(tag.string) + " for assists on " + gameDateString)
                    toReturn += int(tag.string)
                if v == 'stl':
                    print(playerNameString + " gets $" + str(tag.string) + " for steals on " + gameDateString)
                    toReturn += int(tag.string)
                if v == 'blk':
                    print(playerNameString + " gets $" + str(tag.string) + " for blocks on " + gameDateString)
                    toReturn += int(tag.string)
    if toReturn > 0:
        print(playerNameString + " MADE $" + str(toReturn) + " TOTAL for the game on " + gameDateString)
        print("")
        return toReturn
    else :
        print(playerNameString + " DID NOT make any money for the game on " + gameDateString)
        print("")
        return 0



def playerOwesCoach(playerNameString, gameDateString):
    url = "https://www.basketball-reference.com/players/"
    initial = playerNameString.split(" ")[1][0].lower()
    letterurl = url + "{}/".format(initial)

    with urllib.request.urlopen(letterurl) as response:
        html = response.read()
        html = html.decode('utf-8')
    with open('playersWithInitial.html', 'w') as new_file:
        new_file.write(html)
    soup = BeautifulSoup(open('playersWithInitial.html'), 'html5lib')

    playerLocate = soup.find_all('a', href=True)
    for tag in playerLocate:
        if tag.string == playerNameString:
            indHTML = tag.get('href')

    playerPage = "https://www.basketball-reference.com" + indHTML

    with urllib.request.urlopen(playerPage) as response:
        html = response.read()
        html = html.decode('utf-8')
    with open('playerHTML.html', 'w') as new_file:
        new_file.write(html)
    soup = BeautifulSoup(open('playerHTML.html'), 'html5lib')

    yearsPlayed = soup.find_all('a')

    for tag in yearsPlayed:
        if tag.string == '2019-20':
            if 'gamelog' in tag.get('href'):
                finalHTML = "https://www.basketball-reference.com" + tag.get('href')

    with urllib.request.urlopen(finalHTML) as response:
        html = response.read()
        html = html.decode('utf-8')
    with open('gamelog.html', 'w') as new_file:
        new_file.write(html)
    soup = BeautifulSoup(open('gamelog.html'), 'html5lib')

    gameTags = soup.find_all('td')

    booleanFoundCorrectDate = True

    for tag in gameTags:
        for k, v in tag.attrs.items():
            if v == 'date_game':
                if tag.string == gameDateString:
                    booleanFoundCorrectDate = True
                if tag.string != gameDateString:
                    booleanFoundCorrectDate = False
            if v == 'reason' and booleanFoundCorrectDate:
                # print(playerNameString + " did not play in the game on " + gameDateString)
                return 0
            if booleanFoundCorrectDate:
                if v == 'tov':
                    if int(tag.string) != 0:
                        print(playerNameString + " OWES THE COACH $" + str(tag.string) + " for turnovers on " + gameDateString)
                        print("")
                        return int(tag.string)
                    else:
                        print("")
                        return 0
    print("")
    return 0

