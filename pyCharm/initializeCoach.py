from csvDatabaseManager import addToDatabaseCSV
from galileoRequestFunctions import createCardholder

newId = createCardholder("Quin Snyder", "1980-02-12")
# newId = 5080
if newId != None:
    addToDatabaseCSV(newId, "Quin Snyder", "coach")