import requests
import config
from random import randint
import json


url = "https://sandbox.galileo-ft.com/instant/v1"


def random_with_N_digits(n):
    range_start = 10 ** (n - 1)
    range_end = (10 ** n) - 1
    return randint(range_start, range_end)


def createCardholder(nameString, dobString):
    postURL = url + "/cardholders"
    headers = {'Authorization': config.access_token, 'Content-Type': 'application/json'}

    address = {"city": "Salt Lake City", "state": "UT", "street": "1420 500 W", "zip_code": "84115"}
    agreements = [12020, 12021, 12022]
    firstName = nameString.split(' ')[0]
    fakeSSN = str(random_with_N_digits(9))
    identification = {"date_of_birth": dobString, "id": fakeSSN, "id_type": "ssn"}
    income = {"amount": "o200k", "frequency": "biweekly", "occupation": "entertainment", "source": "employment"}
    lastName = nameString.split(' ')[1]
    email = firstName + lastName + "@utahjazz.com"
    fakeMobile = str(random_with_N_digits(10))
    productID = 19482

    payload = {
        "cardholder": {"address": address,
                       "agreements": agreements,
                       "email": email,
                       "first_name": firstName,
                       "identification": identification,
                       "income": income,
                       "last_name": lastName,
                       "mobile": fakeMobile},
        "product_id": productID}

    payloadJson = json.dumps(payload)

    response = requests.request("POST", postURL, headers=headers, data=payloadJson)
    if response.status_code == 201:
        print("successfully made cardholder: " + nameString)
        return response.json()['cardholder_id']
    else:
        print("could not make cardholder in Galileo for: " + nameString)
        print("TRY REFRESHING AUTHORIZATION CODE")
        print(response.status_code)
        print(response.text.encode('utf8'))




def getCardholder(cardholderID):
    getURL = url + "/cardholders/" + str(cardholderID) + "/accounts"
    headers = {'Authorization': config.access_token}
    print(headers)
    response = requests.get(getURL, headers=headers)
    if response.status_code != 200:
        print("cardholder not found in Galileo dashboard, try refreshing Authorization key OR check dashboard to see if they are present and active")
        return None
    print(response.text.encode('utf8'))


def refresh():
    postURL = url + "/refresh"
    tempUsername = config.username
    tempPassword = config.password
    tempRefresh = config.refresh
    payload = {'username': tempUsername, 'password': tempPassword}
    headers = {'Authorization': tempRefresh}
    # print(payload)
    # print(headers)
    response = requests.request("POST", postURL, headers=headers, data=payload)
    # print(response.status_code)
    if response.status_code == 201:
        print("authorization code successfully REFRESHED")
    else:
        print("ERROR REFRESHING AUTHORIZATION CODE")
    # print(response.json()['access_token'])
    newAccess = response.json()['access_token']
    # print(response.text.encode('utf8'))
    fileObject = open("config.py", "w")
    fileObject.write("username = '" + tempUsername + "'\n")
    fileObject.write("password = '" + tempPassword + "'\n")
    fileObject.write("access_token = 'Bearer " + newAccess + "'\n")
    fileObject.write("refresh = '" + tempRefresh + "'\n")
    fileObject.close()


def getCardHolderAccountId(cardHolderNumber):
    getURL = url + "/cardholders/" + str(cardHolderNumber) + "/accounts"
    headers = {'Authorization': config.access_token}
    response = requests.get(getURL, headers=headers)
    if response.status_code == 200:
        return response.json()['accounts'][0]['account_id']
    else:
        print("error getting cardHolderAccountID")
        print("TRY REFRESHING AUTHENTICATION CODE")
        return None


def transferMoney(sourceAccountID, destinationAccountID, amount):
    postURL = url + "/transfers"
    payload = {
        "amount": amount,
        "destination_account_id": destinationAccountID,
        "source_account_id": sourceAccountID
    }
    payloadJson = json.dumps(payload)
    headers = {'Authorization': config.access_token, 'Content-Type': 'text/plain'}

    response = requests.request("POST", postURL, headers=headers, data = payloadJson)
    if response.status_code != 201:
        print("transfer from account: " + str(sourceAccountID) + " to account: " + str(destinationAccountID) + " was unsuccessful")
        print("Response Error Code: " + str(response.status_code))
        print(response.text.encode('utf8'))


def getPlayerCurrentBalance(playerCardHolderID):
    getURL = url + "/cardholders/" + str(playerCardHolderID) + "/accounts"
    headers = {'Authorization': config.access_token}
    payload = {}
    response = requests.get(getURL, headers=headers, data=payload)
    if response.status_code == 200:
        return response.json()['accounts'][0]['balance']
    else:
        print("error getting balance")
        print("TRY REFRESHING AUTHENTICATION CODE")
        return None


