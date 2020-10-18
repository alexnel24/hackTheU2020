from csvDatabaseManager import addToDatabaseCSV
from csvDatabaseManager import getCardholderID
from csvDatabaseManager import coachInDatabaseID

print("")
print("TESTING addToDatabaseCSV:")
addToDatabaseCSV(8, "fake name1", "player")
addToDatabaseCSV(15, "whatever", "THIS SHOULD BREAK IT")
addToDatabaseCSV(15, "whatever", "player")
addToDatabaseCSV(5073, "fakeQuin Snyder", "coach")
addToDatabaseCSV(6808, "Mike Conley", "player")
addToDatabaseCSV(42, "New Coach", "coach")

print("")
print("TESTING getCardHolderID:")
print(getCardholderID("fake name1"))
print(getCardholderID("doesn't exist"))
print(getCardholderID("Mike Conley"))

print("")
print("TESTING coachInDatabase:")
assert coachInDatabaseID() == 5073


