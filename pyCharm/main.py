from csvDatabaseManager import addToDatabaseCSV
from userFunctions import killProgram
from userFunctions import showOptions
from userFunctions import requestRefresh
from userFunctions import showTeam
from userFunctions import trackPlayer
from userFunctions import  processPay

print("Hi HackTheU Judges!")

print("Type 'options' for list of commands")
incoming = input("command: ")

while incoming != exit:
    if incoming == "exit":
        killProgram()

    elif incoming == 'options':
        showOptions()

    elif incoming == 'refresh':
        requestRefresh()

    elif incoming == 'listTeam':
        showTeam()

    elif incoming == 'trackPlayer':
        trackPlayer()

    elif incoming == 'payTeam':
        processPay()

    else:
        print("command not recognized")

    print("")
    print("Type 'options' for list of commands")
    incoming = input("command: ")
