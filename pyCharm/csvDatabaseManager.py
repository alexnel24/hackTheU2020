import pandas as pd


# VOID FUNCTION
# Parameters:
# galileoIdNumber (int) : this is the int that comes from Galileo for the cardholder
# nameString (String) : this is the name of the player or coach
# playerOrCoachString : this must be either "player" or "coach" [sanitized to only accept these two]
def addToDatabaseCSV(galileoIdNumber, nameString, playerOrCoachString):
    if galileoIdNumber is None:
        return
    if playerOrCoachString != "player" and playerOrCoachString != "coach":
        print("must put 'player or coach as third parameter'")
        return
    if len(nameString.split(' ')) <= 1:
        print("name must have a first and last name")
        return
    fileName = "cardHolderList.csv"

    if getCardholderID(nameString) is not None:
        print(nameString + " already exists in database")
        return

    if coachInDatabaseID() is not None and playerOrCoachString == "coach":
        print("THERE IS A COACH ALREADY IN THE DATABASE, YOU CANNOT ADD ANOTHER ONE")
        return
    try:
        df =pd.read_csv("cardHolderList.csv")
    except:
        df = pd.DataFrame(columns=['id', 'name', 'player/coach'])
    df = df.append({'id': galileoIdNumber, 'name': nameString, 'player/coach': playerOrCoachString}, ignore_index=True)
    df.to_csv(fileName, index=False)
    print(playerOrCoachString + " " + nameString + " successfully added to csvDatabase")


#  RETURNS int OR None
# Parameters:
# nameString (String) : this is the name of the player or coach
# if found in database the cardholder id will be returned OTHERWISE None
def getCardholderID(nameString):
    fileName = "cardHolderList.csv"
    try:
        df = pd.read_csv(fileName)
    except:
        return None
    for index, line in df.iterrows():
        if line['name'] == nameString:
            return line['id']
    return None


def coachInDatabaseID():
    try:
        df = pd.read_csv("cardHolderList.csv")
    except:
        return None
    for index, row in df.iterrows():
        if row['player/coach'] == "coach":
            return row['id']
    return None


def getDataFrame():
    return pd.read_csv("cardHolderList.csv")
