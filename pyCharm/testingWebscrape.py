from webScrapeFunctions import getPlayersBday
from webScrapeFunctions import validGameDate
from webScrapeFunctions import wonGame
from webScrapeFunctions import playerAmountEarnedOrLost
from webScrapeFunctions import playerOwesCoach

# print("")
# print("TESTING getPlayersBday")
# assert getPlayersBday("Joe Ingles") == "1987-10-02"
# assert getPlayersBday("Donovan Mitchell") == "1996-09-07"
# assert getPlayersBday("Jordan Clarkson") == "1992-06-07"
# assert getPlayersBday("Royce O'Neale") == "1993-06-05"
# assert getPlayersBday("Dante Exum") == "ErrorPlayerNotCurrent"
# assert getPlayersBday("Dennis Lindsey") == "ErrorNotFound"
# print("ALL getPlayersBday TESTS PASSED!")


# print("")
# print("TESTING validGameDate")
# assert validGameDate("dont matter") is False
# assert validGameDate("2019-11-03") is True
# assert validGameDate("2020-11-03") is False
# assert validGameDate("2020-03-03") is False
# assert validGameDate("2020-03-02") is True
# assert validGameDate("2020-06-03") is False
# assert validGameDate("2020-08-03") is True
# assert validGameDate("2020-01-12") is True
# assert validGameDate("2020-08-17") is False #only works on regular season games during 2019-2020 season
# print("ALL validGameDate TESTS PASSED!")

print("")
print("TESTING wonGame")
assert wonGame("2020-08-05") is True
assert wonGame("2020-08-08") is False
assert wonGame("2020-08-10") is False
assert wonGame("2020-01-12") is True
assert wonGame("2020-06-06") is None
assert wonGame("2020-08-03") is False
print("ALL wonGame TESTS PASSED!")

print("")
print("TESTING playerAmountEarnedOrLost")
playerAmountEarnedOrLost("Joe Ingles", "2020-08-03")
playerOwesCoach("Joe Ingles", "2020-08-03")

playerAmountEarnedOrLost("Donovan Mitchell", "2020-01-12")