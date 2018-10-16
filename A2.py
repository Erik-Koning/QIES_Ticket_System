#Team DJANGO
#CMPE/CISC 327
#October 2018

import os.path
import re

user_type = 0 # 0 -> not loggedin | 1 -> agent | 2 -> planner
validServicesFile = "vServices.txt"             #file name for our valid services
summaryFile = "transactionSummaryFile.txt"      #
pendingSummaryFile = []
pendingValidServices = []
canceledTickets = 0 #number of tickets an agent has canceled in the current session
changedTickets = 0  #number of tickets an agent has changed in the current session

def addToPendingServicesList(serviceNum):
    global pendingValidServices
    pendingValidServices.append(str(serviceNum))

def writePendingServicesList():
    global pendingValidServices
    global validServicesFile
    servicesFile = open(validServicesFile,"a")
    servicesFile.write('\n'.join(pendingValidServices))
    servicesFile.close()
    return

def addToPendingSummaryFile(transCode, sNum1, numTickets, sNum2, sName, sDate):
    global pendingSummaryFile
    #create the transaction summary line
    line = transCode + " " + str(sNum1) + " " + str(numTickets) + " " + str(sNum2) + " " + sName + " " + str(sDate)
    pendingSummaryFile.append(line)
    return

def writePendingSummaryFile():
    global summaryFile
    global pendingSummaryFile
    #Create a blank summaryFile
    #if it already exists it is overwritten with a blank one
    sF = open(summaryFile,"w+")
    sF.write('\n'.join(pendingSummaryFile))
    sF.close()
    return

def removeValidService(serviceNum):
    sF = open(validServicesFile, "r")
    lines = sF.readlines()
    sF.close()

    sF = open(validServicesFile, "w")
    for line in lines:
        if line != serviceNum:
            sF.write(line)
    sF.close()
    return

def validServiceDate(date):
    #check if the date is not the right lenght or contains a letter
    if len(str(date)) != 8 or bool(re.search('[a-zA-Z]', str(date))):
        return False
    #cretae a numeric list of the date values
    dL = [int(x) for x in str(date)]
    if dL[0] > 2 or dL[0] < 1:
        return False
    if dL[4] > 1 or dL[4] < 0 or (dL[4] == 1 and dL[5] > 2):
        return False
    if dL[6] > 3 or dL[6] < 0 or (dL[6] == 3 and dL[7] > 1):
        return False
    #illegal day for respective month value
    #Jan, Mar, May, July, Aug, Oct, Dec, can not have more than 31 days
    if ((dL[4] == 0 and dL[5] == 1) or (dL[4] == 0 and dL[5] == 3) or (dL[4] == 0 and dL[5] == 5) or (dL[4] == 0 and dL[5] == 7) or (dL[4] == 0 and dL[5] == 8) or (dL[4] == 1 and dL[5] == 0) or (dL[4] == 1 and dL[5] == 2)) and (dL[6] >= 3 and dL[7] > 1):
        return False 
    #Apr, June, Sept, Nov, can not have more than 30 days
    if ((dL[4] == 0 and dL[5] == 4) or (dL[4] == 0 and dL[5] == 6) or (dL[4] == 0 and dL[5] == 9) or (dL[4] == 1 and dL[5] == 1)) and (dL[6] >= 3 and dL[7] > 0):
        return False 
    #Feb, disregarding leap years...
    if (dL[4] == 0 and dL[5] == 2) and (dL[6] >= 2 and dL[7] > 8):
        return False
    return True

def wait_for_login():
    while True:
        login_command = input("").lower()
        if login_command == "login":
            break
        else:
            print("You cannot do other things without first logging in")
    return login()

def login():
    global user_type
    global validServicesFile
    #Check the valid services file exists, if it does not
    #an empty txt file is created to be populated
    #a+ Opens a file for both appending and reading.
    #if the file does not exist, it creates a new file for reading and writing
    servicesFile = open(validServicesFile,"a+")
    servicesFile.close()

    #initialize variables
    global pendingSummaryFile
    global pendingValidServices
    global canceledTickets
    global changedTickets
    pendingSummaryFile = []
    pendingValidServices = []
    canceledTickets = 0
    changedTickets =0

    while True:
        userInput = str(input("Please enter \"agent\" or \"planner\" to login:\n")).lower()
        if userInput == "agent":
            user_type = 1 # set user_type to agent
            addToPendingSummaryFile("Agent Login", "xxxxx", "xxxx", "xxxxx", "xxxxxx", "xxxxxxxx")
            addToPendingSummaryFile("", "", "", "", "", "")
            print("Login successfully as agent")
            return user_type
        elif userInput == "planner":
            user_type = 2 # set user_type to planner
            addToPendingSummaryFile("Planner Login", "xxxxx", "xxxx", "xxxxx", "xxxxxx", "xxxxxxxx")
            addToPendingSummaryFile("", "", "", "", "", "")
            print("Login successfully as planner")
            return user_type
        else:
            print("unknown username") # no way to get here

def createService():
    if user_type != 2:
        print("Invalid operation for user")
        return
    while True:
        serviceNum = input("What is the service number?")
        #service must not already be in valid service list and
        #service number must be 5 characters and not begin with 0
        if isValidService(serviceNum) or len(serviceNum) != 5 or [int(x) for x in str(serviceNum)][0] == 0:
            print("Invalid new service number")
        else:
            break
    while True:
        serviceDate = input("What is the service date in YYYYMMDD format?")
        if not validServiceDate(serviceDate) or bool(re.search('[a-zA-Z]', str(serviceDate))):
            print("Invalid service date")
        else:
            break
    while True:
        serviceName = input("What is the service name?")
        if len(serviceName) < 3 or len(serviceName) > 39:
            print("Invalid service name")
        else:
            break
    addToPendingServicesList(serviceNum)
    addToPendingSummaryFile("CRE", serviceNum, "xxxx", "xxxxx", serviceName, serviceDate)
    return

def deleteService():
    if user_type == 1:
        print("Invalid operation for user")
        return

    while True:
        serviceNum = input("What is the service number?")
        #service number must be 5 characters and not begin with 0
        if isValidService(serviceNum) and (len(serviceNum) == 5 or [int(x) for x in str(date)][0] == 0):
            break
        else:
            print("Invalid service number")

    while True:
        serviceName = input("What is the service name?")
        if len(serviceName) < 3 or len(serviceName) > 39:
            print("Invalid service name")
        else:
            break

    removeValidService(serviceNum)
    addToPendingSummaryFile("DEL", serviceNum, "xxxx", "xxxxx", serviceName, serviceDate)
    return


def sellTicket():
    while True:
        serviceNum = input("What is the service number?")
        if not isValidService(serviceNum):
            print("Not a valid service number")
        else:
            break
    while True:
        numTickets = int(input("How many tickets are being sold?"))
        if bool(re.search('[a-zA-Z]', str(numTickets))) or numTickets < 0 or ticketsAvailable(serviceNum) < numTickets:
            print("Invalid number of tickets")
        else:
            break

    addToPendingSummaryFile("SEL", serviceNum, numTickets, "xxxxx", "xxxxxx", "xxxxxxxx")
    return

def cancelTicket():
    global canceledTickets
    global user_type
    while True:
        serviceNum = input("What is the service number?")
        if not isValidService(serviceNum):
            print("Not a valid service number")
        else:
            break
    while True:
        numTickets = int(input("How many tickets would you like to cancel?"))
        if user_type == 1 and numTickets > 10:
            print("Agent can cancel a max of 10 tickets")
        elif numTickets < 0 or bool(re.search('[a-zA-Z]', str(numTickets))):
            print("Invalid number of tickets")
        elif user_type == 1 and ((numTickets + canceledTickets) > 20):
            print("Agent can cancel a max of 20 tickets per session")
        else:
            break
    if user_type == 1:
        canceledTickets += numTickets
    
    addToPendingSummaryFile("CAN", serviceNum, numTickets, "xxxxx", "xxxxxx", "xxxxxxxx")
    return  

def changeTicket():
    global changedTickets
    global user_type

    while True:
        currentService = input("What is the current service number?")
        if not isValidService(serviceNum):
            print("Not a valid service number")
        else:
            break
    while True:
        newService = input("What is the new service number?")
        if not isValidService(serviceNum):
            print("Not a valid service number")
        else:
            break
    if currentService == newService:
        print("Not a different service number")
        return
    while True:
        numTickets = int(input("How many tickets would you like to change?"))
        if user_type == 1 and numTickets > 20:
            print("An Agent can change a max of 20 tickets per session")
        elif numTickets < 0 or bool(re.search('[a-zA-Z]', str(numTickets))):
            print("Invalid number of tickets")
        elif user_type == 1 and ((numTickets + changedTickets) > 20):
            print("An Agent can change a max of 20 tickets per session")
        else:
            break
    if user_type == 1:
        changedTickets += numTickets
    addToPendingSummaryFile("CHG", currentService, numTickets, newService, "xxxxxx", "xxxxxxxx")
    return

def logout():
    global user_type
    addToPendingSummaryFile("EOS", "xxxxx", "xxxx", "xxxxx", "xxxxxx", "xxxxxxxx")
    
    #we merge these lists at the end becuase the added services in this session
    #cannot be accessed untill a new session starts. And the summary file is not
    #finalized until after official logout
    writePendingServicesList()
    writePendingSummaryFile()
    user_type = 0
    print("Logout successfully")
    return


def isValidService(service):
    global validServicesFile
    servicesFile = open(validServicesFile,"r")
    lines = servicesFile.readlines()
    for line in lines:
        if service == line:
            return True
    servicesFile.close()
    return False

def ticketsAvailable(serviceNum):
    return 9999

def main():
    global user_type

    while True:
        print("QIES Interface - Team DJANGO")
        wait_for_login()

        while True:
            service = input("Type a command (sell ticket, cancel ticket, change ticket, create service, delete service, or logout):\n").lower()
            if service == "login":
                if user_type == 1:
                    print("Already logged in as Agent")
                if user_type == 2:
                    print("Already logged in as Planner")
                else:
                    print("Error: UNKNOWN USER. Already logged in")
            elif user_type != 1 and user_type != 2:
                print("Error: Not logged into valid user yet")
            elif service == "sell ticket":
                sellTicket()
            elif service == "cancel ticket":
                cancelTicket()
            elif service == "change ticket":
                changeTicket()
            elif service == "create service":
                createService()
            elif service == "delete service":
                deleteService()
            elif service == "logout":
                logout()
                break
            elif service == "shutdown":
                return

main()