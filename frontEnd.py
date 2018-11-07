#Team DJANGO
#CMPE/CISC 327
#October 2018

import time
import os.path
import os           #to enable folders to be made
import re
import sys          #to check passed argument to program

user_type = 0 # 0 -> not loggedin | 1 -> agent | 2 -> planner
validServicesFile = "validServices.txt"         #file name for valid services file
summaryFile = "transactionSummary.txt"          #file name for transaction summary file
pendingSummaryFile = []                         #pending transaction summary file
pendingValidServices = []                       #pending valid services file
canceledTickets = 0 #number of tickets an agent has canceled in the current session
changedTickets = 0  #number of tickets an agent has changed in the current session

#adds a service to the pending services file array,
#to be added to the file on logout
def addToPendingServicesList(serviceNum):
    global pendingValidServices
    pendingValidServices.append(str(serviceNum))

#writes the new services to the valid services file.
def writePendingServicesList():
    global pendingValidServices
    global validServicesFile
    #open the services file with the "append" argument so older services 
    #persist in the file after logout and re-login
    if os.path.exists(validServicesFile):
        with open(validServicesFile, 'r+') as sF:
            content = sF.read()
            sF.seek(0, 0)
            sF.write('\n'.join(pendingValidServices) + '\n' + content)
    else:
        sF = open(validServicesFile,"w+")
        sF.write('\n'.join(pendingValidServices))
        sF.write('00000')

    sF.close()
    return

#adds transaction details to pending transaction summary array
def addToPendingSummaryFile(transCode, sNum1, numTickets, sNum2, sName, sDate):
    global pendingSummaryFile
    #create the transaction summary line
    line = transCode + " " + str(sNum1) + " " + str(numTickets) + " " + str(sNum2) + " " + sName + " " + str(sDate)
    pendingSummaryFile.append(line)
    return

#writes the pending summary text file
def writePendingSummaryFile():
    global summaryFile
    global pendingSummaryFile
    #opens summary file with argument "w+" so a blank summaryFile is created 
    #if it already exists it is overwritten with a blank one
    sF = open(summaryFile,"w+")
    sF.write('\n'.join(pendingSummaryFile))
    sF.close()
    return

#writes the pending summary text file
def writePendingSummaryFileTestingMode():
    global testNum
    global pendingSummaryFile
    global inputTestFile
    global testId

    summaryFile = inputTestFile.replace("input","output")
    #opens summary file with argument "w+" so a blank summaryFile is created 
    #if it already exists it is overwritten with a blank one

    #check to see if we are dealing with a full path, if we are get summary file relative path name
    if "\\" in summaryFile:
        summaryFile = summaryFile.rsplit('\\',1)[1]

    #make a folder for test ID number
    outputDirName = "Outputs/" + testId
    if not os.path.exists(outputDirName):
        os.makedirs(outputDirName)

    sF = open(outputDirName+"/"+summaryFile,"a+")
    sF.write('\n'.join(pendingSummaryFile))
    sF.close()
    return

def makePendingSummaryFileTestingMode():
    global testNum
    global inputTestFile
    global testId

    summaryFile = inputTestFile.replace("input","output")
    #opens summary file with argument "w+" so a blank summaryFile is created 
    #if it already exists it is overwritten with a blank one

    #check to see if we are dealing with a full path, if we are get summary file relative path name
    if "\\" in summaryFile:
        summaryFile = summaryFile.rsplit('\\',1)[1]

    #make a folder for test ID number
    outputDirName = "Outputs/" + testId
    if not os.path.exists(outputDirName):
        os.makedirs(outputDirName)

    sF = open(outputDirName+"/"+summaryFile,"w+")

#returns false for all dates that are outside a valid range
#true if a valid date
def validServiceDate(date):
    #check if the date is not the right lenght or contains a letter
    if len(str(date)) != 8 or bool(re.search('[a-zA-Z]', str(date))):
        return False
    #cretae a numeric list of the date values
    dL = [int(x) for x in str(date)]
    if dL[0] > 2 or dL[0] < 1:                                              #check illegal years (X000MMDD)
        return False
    if dL[0] == 1 and (dL[1] < 9 or (dL[1] == 9 and dL[2] < 8)):            #check illegal years in 20th centry (19XXMMDD)
        return False
    if dL[4] > 1 or dL[4] < 0 or (dL[4] == 1 and dL[5] > 2) or (dL[4] == 0 and dL[5] == 0):     #check illegal monthes (YYYYXXDD)
        return False
    if dL[6] > 3 or dL[6] < 0 or (dL[6] == 3 and dL[7] > 1) or (dL[6] == 0 and dL[7] == 0):      #check illegal day (YYYYMMXX)
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

#returns true if the passed service number (as a string), 
#is in the valid services file, false otherwise
def isValidService(service):
    global validServicesFile
    service = re.sub(r"[\n\t\s]*", "", service)
    servicesFile = open(validServicesFile,"r")
    lines = servicesFile.readlines()
    for line in lines:
        line = re.sub(r"[\n\t\s]*", "", line)
        if service == line:
            servicesFile.close()
            return True
    servicesFile.close()
    return False

#TODO: number of tickets available for that service number
def ticketsAvailable(serviceNum):
    return 9999

def initVariables():
    #initialize variables to be empty on login
    global pendingSummaryFile
    global pendingValidServices
    global canceledTickets
    global changedTickets
    pendingSummaryFile = []
    pendingValidServices = []
    canceledTickets = 0
    changedTickets =0

def initServiceFile():
    #Check the valid services file exists, if it does not
    #an empty txt file is created to be populated
    #r+ Opens a file for both writing and reading.
    #if the file does not exist, it creates a new file for reading and writing
    #This ensures 00000 is at the end of the file always
    with open(validServicesFile, 'r+') as f:
        content = f.read()
        lines = content.splitlines()
        #if empty:
        if os.stat(validServicesFile).st_size == 0:
            f.write("00000")
        #contents in valid serivces file
        else:
            last_line = re.sub('\n','',lines[len(lines)-1])
            if not last_line == '00000':
                f.seek(0, 0)
                f.write(content + '\n' + '00000')
    f.close()

#waits for user to type login, then goes to login() function
def wait_for_login():
    while True:
        login_command = input("").lower()
        if login_command == "login":
            break
        elif login_command == "shutdown" or login_command == "exit" or login_command == "end" or login_command == "q" or login_command == "quit":
            exit()
        else:
            print("You cannot do other things without first logging in")
    return login()

#sets up new login environment and asks who the user is
def login():
    global user_type
    global validServicesFile
    global testMode
    global commandNumber
    global numberCommands
    global testLines
    
    initServiceFile()

    while True:
        if testMode:
            if commandNumber >= numberCommands:
                    print("All test commands done for test case Id: {word}".format(word=testId))
                    writePendingSummaryFileTestingMode()
                    exit()
            userInput = testLines[commandNumber]
            commandNumber += 1
        else:
            userInput = str(input("Please enter \"agent\" or \"planner\" to login:\n")).lower()
        if userInput == "agent":
            user_type = 1 # set user_type to agent
            #addToPendingSummaryFile("Agent Login", "xxxxx", "xxxx", "xxxxx", "xxxxxx", "xxxxxxxx")
            print("Login successfully as agent")
            return user_type
        elif userInput == "planner":
            user_type = 2 # set user_type to planner
            #addToPendingSummaryFile("Planner Login", "xxxxx", "xxxx", "xxxxx", "xxxxxx", "xxxxxxxx")
            print("Login successfully as planner")
            return user_type
        else:
            print("unknown username")

#Adds a service to the services list after successful creation, and subsequent logout
def createService():
    global testMode
    global commandNumber
    global numberCommands
    global testLines

    if user_type != 2:
        print("Invalid operation for user")
        return
    while True:
        if testMode:
            if commandNumber >= numberCommands:
                    print("All test commands done for test case Id: {word}".format(word=testId))
                    writePendingSummaryFileTestingMode()
                    exit()
            serviceNum = testLines[commandNumber].lower().replace(" ","")
            commandNumber += 1
        else:
            serviceNum = input("What is the service number?")
        #service must not already be in valid service list and
        #service number must be 5 characters and not begin with 0
        if isValidService(serviceNum) or len(serviceNum) != 5 or [int(x) for x in str(serviceNum)][0] == 0:
            print("Invalid new service number")
        else:
            break
    while True:
        if testMode:
            if commandNumber >= numberCommands:
                    print("All test commands done for test case Id: {word}".format(word=testId))
                    writePendingSummaryFileTestingMode()
                    exit()
            serviceDate = testLines[commandNumber].lower().replace(" ","")
            commandNumber += 1
        else:
            serviceDate = input("What is the service date in YYYYMMDD format?")
        if not validServiceDate(serviceDate) or bool(re.search('[a-zA-Z]', str(serviceDate))):
            print("Invalid service date")
        else:
            break
    while True:
        if testMode:
            if commandNumber >= numberCommands:
                    print("All test commands done for test case Id: {word}".format(word=testId))
                    writePendingSummaryFileTestingMode()
                    exit()
            serviceName = testLines[commandNumber].lower().replace(" ","")
            commandNumber += 1
        else:
            serviceName = input("What is the service name?")
        if len(serviceName) < 3 or len(serviceName) > 39:
            print("Invalid service name")
        else:
            break
    addToPendingServicesList(serviceNum)
    addToPendingSummaryFile("CRE", serviceNum, "xxxx", "xxxxx", serviceName, serviceDate)
    return

#
def deleteService():
    global testMode
    global testLines
    global commandNumber
    global numberCommands
    global testId

    if user_type == 1:
        print("Invalid operation for user")
        return

    #get input
    if testMode:
        if commandNumber >= numberCommands:
                print("All test commands done for test case Id: {word}".format(word=testId))
                writePendingSummaryFileTestingMode()
                exit()
        serviceNum = testLines[commandNumber].lower().replace(" ","")
        commandNumber += 1
    else:
        serviceNum = input("What is the service number?")
    if testMode:
        if commandNumber >= numberCommands:
                print("All test commands done for test case Id: {word}".format(word=testId))
                writePendingSummaryFileTestingMode()
                exit()
        serviceName = testLines[commandNumber].lower().replace(" ","")
        commandNumber += 1
    else:
        serviceName = input("What is the service name?")

    #check the input, service number must be 5 characters and not begin with 0
    if not isValidService(serviceNum) or (len(serviceNum) != 5 or [int(x) for x in str(serviceNum)][0] == 0):
        print("Invalid service number")
        return
    if len(serviceName) < 3 or len(serviceName) > 39:
        print("Invalid service name")
        return

    #finds the service number in the valid services file and
    #re-writes the services file without the one being removed
    sF = open(validServicesFile, "r")       #open file for reading
    lines = sF.readlines()                  #saves lines
    sF.close()                                  
    sF = open(validServicesFile, "w")       #open file for writing
    for line in lines:                      
        if line != serviceNum:              #write line if not the one to delete
            sF.write(line)
    sF.close()

    addToPendingSummaryFile("DEL", serviceNum, "xxxx", "xxxxx", serviceName, "xxxxxxxx")
    return

#sells a umber tickets for a valid service number
def sellTicket():
    global testMode
    global testLines
    global numberCommands
    global commandNumber

    #get input
    if testMode:
        if commandNumber >= numberCommands:
                print("All test commands done for test case Id: {word}".format(word=testId))
                writePendingSummaryFileTestingMode()
                exit()
        serviceNum = testLines[commandNumber].lower().replace(" ","")
        commandNumber += 1
    else:
        serviceNum = input("What is the service number?")
        
    if testMode:
        if commandNumber >= numberCommands:
                print("All test commands done for test case Id: {word}".format(word=testId))
                writePendingSummaryFileTestingMode()
                exit()
        numTickets = testLines[commandNumber].lower().replace(" ","")
        commandNumber += 1
    else:
        numTickets = int(input("How many tickets are being sold?"))

    #check input
    if bool(re.search('[a-zA-Z]', str(numTickets))) or numTickets < 0 or ticketsAvailable(serviceNum) < numTickets or len(str(numTickets)) > 4:
        print("Invalid number of tickets")
        return
    if not isValidService(serviceNum):
        print("Not a valid service number")
        return

    addToPendingSummaryFile("SEL", serviceNum, numTickets, "xxxxx", "xxxxxx", "xxxxxxxx")
    return

#cancels a number of tickets for a service
def cancelTicket():
    global testMode
    global testLines
    global commandNumber
    global numberCommands
    global canceledTickets
    global user_type

    #get input
    if testMode:
        if commandNumber >= numberCommands:
                print("All test commands done for test case Id: {word}".format(word=testId))
                writePendingSummaryFileTestingMode()
                exit()
        serviceNum = testLines[commandNumber].lower().replace(" ","")
        commandNumber += 1
    else:
        serviceNum = input("What is the service number?")
    if testMode:
        if commandNumber >= numberCommands:
                print("All test commands done for test case Id: {word}".format(word=testId))
                writePendingSummaryFileTestingMode()
                exit()
        numTickets = testLines[commandNumber].lower().replace(" ","")
        commandNumber += 1
    else:
        numTickets = int(input("How many tickets would you like to cancel?"))

    #check input
    if user_type == 1 and numTickets > 10:
        print("Agent can cancel a max of 10 tickets")
        return
    elif numTickets < 0 or bool(re.search('[a-zA-Z]', str(numTickets))):
        print("Invalid number of tickets")
        return
    elif user_type == 1 and ((numTickets + canceledTickets) > 20):
        print("Agent can cancel a max of 20 tickets per session")
        return
    if not isValidService(serviceNum):
        print("Not a valid service number")
        return

    canceledTickets += int(numTickets)
    
    addToPendingSummaryFile("CAN", serviceNum, numTickets, "xxxxx", "xxxxxx", "xxxxxxxx")
    return  

#exchanges a number of tickets from one service number ot another
def changeTicket():
    global testMode
    global testLines
    global commandNumber
    global numberCommands
    global changedTickets
    global user_type

    # get input
    if testMode:
        if commandNumber >= numberCommands:
                print("All test commands done for test case Id: {word}".format(word=testId))
                writePendingSummaryFileTestingMode()
                exit()
        currentService = testLines[commandNumber].lower().replace(" ","")
        commandNumber += 1
    else:
        currentService = input("What is the current service number?")
    if testMode:
        if commandNumber >= numberCommands:
                print("All test commands done for test case Id: {word}".format(word=testId))
                writePendingSummaryFileTestingMode()
                exit()
        newService = testLines[commandNumber].lower().replace(" ","")
        commandNumber += 1
    else:
        newService = input("What is the new service number?")
    if testMode:
        if commandNumber >= numberCommands:
                print("All test commands done for test case Id: {word}".format(word=testId))
                writePendingSummaryFileTestingMode()
                exit()
        numTickets = testLines[commandNumber].lower().replace(" ","")
        commandNumber += 1
    else:
        numTickets = int(input("How many tickets would you like to change?"))

    #check input
    if user_type == 1 and numTickets > 20:
        print("An Agent can change a max of 20 tickets per session")
        return
    elif numTickets < 0 or bool(re.search('[a-zA-Z]', str(numTickets))):
        print("Invalid number of tickets")
        return
    elif user_type == 1 and ((numTickets + changedTickets) > 20):
        print("An Agent can change a max of 20 tickets per session")
        return
    if currentService == newService:
        print("Not a different service number")
        return
    if not isValidService(newService):
        print("Not a valid service number" + newService)
        return
    if not isValidService(currentService):
        print("Not a valid service number" + currentService)
        return

    if user_type == 1:
        changedTickets += numTickets
    addToPendingSummaryFile("CHG", currentService, numTickets, newService, "xxxxxx", "xxxxxxxx")
    return

#logs user out of current session
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

#QIES interface loop
def main():
    global user_type
    global numberCommands
    global commandNumber
    global inputTestFile
    global testMode
    global testLines
    global testId
    user_type = 0
    testMode = False
    commandNumber = -1
    numberCommands = 0
    firstTestModeSession = False

    #check if passed a testing file
    if(len(sys.argv) == 2 and ".txt" in str(sys.argv[1])):
        firstTestModeSession = True
        testMode = True
        inputTestFile = sys.argv[1]
        #get testId number of the input test file
        if "\\" in inputTestFile:
            testId = inputTestFile.rsplit('\\',1)[1]
            testId = testId.rsplit('_',4)
            testId= str(testId[1]) + "." + str(testId[2])
        print("\n*TESTING MODE*, using test file ID: {word}\n".format(word=testId))
        #We iterate the test number every time there is a login
        outputDirName = "Outputs"
        if not os.path.exists(outputDirName):
            os.makedirs(outputDirName)
        #open test file and then close after stripping new line characters
        with open(inputTestFile) as f: testLines = [line.rstrip('\n') for line in f]
        commandNumber = 0
        numberCommands = len(testLines)
    elif(len(sys.argv) > 2):
        print("Error: Can only accept 1 test file, *running in non testing mode*\n")

    #infinite program user input loop
    while True:
        #if all test inputs done
        if commandNumber >= numberCommands:
            print("All test commands done for test case Id: {word}\n".format(word=testId))
            writePendingSummaryFileTestingMode()
            exit()
        #clear out old values from previous login session
        if(not testMode):
            initVariables()
        #start a spending summary file so even after a test logout the same transaction summary file is appended to by subsequent commands
        if(firstTestModeSession):
            initVariables()
            makePendingSummaryFileTestingMode()
            firstTestModeSession = False

        print("QIES Interface - Team DJANGO")

        if (not testMode):
            wait_for_login()

        while True:
            #get command
            if testMode:
                #if all test inputs done
                if commandNumber >= numberCommands:
                    print("All test commands done for test case Id: {word}".format(word=testId))
                    writePendingSummaryFileTestingMode()
                    exit()
                service = testLines[commandNumber].lower().replace(" ","")
                commandNumber += 1
            else:
                service = input("Type a command (sell ticket, cancel ticket, change ticket, create service, delete service, or logout):\n").lower().replace(" ","")
            
            #command switch
            if service == "logout":
                logout()
                break
            elif service == "login":
                if testMode and user_type == 0:
                    login()
                elif user_type == 1:
                    print("Already logged in as Agent")
                elif user_type == 2:
                    print("Already logged in as Planner")
                else:
                    print("Error: UNKNOWN USER. Already logged in")
            elif user_type != 1 and user_type != 2:
                print("Error: Not logged into valid user yet")
            elif service == "sellticket":
                sellTicket()
            elif service == "cancelticket":
                cancelTicket()
            elif service == "changeticket":
                changeTicket()
            elif service == "createservice":
                createService()
            elif service == "deleteservice":
                deleteService()
            elif service == "shutdown" or service == "exit" or service == "end" or service == "q" or service == "quit":
                exit()

main()
