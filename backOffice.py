import time
import os.path
import os           #to enable folders to be made
import re
import sys          #to check passed argument to program

centralServicesFile = "centralServices.txt"
validServicesFile = "validServices.txt"
summaryFile = "transactionSummary.txt"

#global lists
pendingValidServices = []                       #pending valid services file
pendingCentralServices = []

def printLog(fileName, contents):
    #create file if it does exist
    if not os.path.isfile(fileName):
        f = open(fileName, "w")
        f.close()
    #open for appending to log file
    f = open(fileName, "a")
    f.write(contents)
    f.close()
    print(contents)
    return

def initVariables():
    global pendingValidServices
    global pendingCentralServices
    #clear out variables from previous operations
    pendingValidServices=[]
    pendingCentralServices=[]

# TODO - servicenumbers, servicenames, and dates are as described above for the TransactionSummaryFile
def checkInputService(line):
    # check line is not greater than 63 characters
    if len(line) > 63:
        print('Error \n line: {} \n Line Longer than 63 characters, breaking constraint'.format(line))
        return False

    inputs = line.split(' ')

    # check items are seperated by one space
    if len(inputs) != 5:
        print('Error \n line: {} \n Line is not seperated by exactly one space between items'.format(line))
        return False

    # {service number, service capacity, sold tickets, service name, service date}
    # check service number
    if (str(inputs[0])[0] == "0") or (len(inputs[0]) !=5 ):
        print('Error \n line: {} \n The service number must be between 1 and 4 decimal digits'.format(line))
        return False
    # check that service capacities are 1 to 4 decimal digits
    if (len(str(inputs[1])) < 1) or (len(str(inputs[1])) > 4) or not str(inputs[1]).isdigit():
        print('Error \n line: {} \n The service capacity must be between 1 and 4 decimal digits'.format(line))
        return False
    # check service capacities is not greater than 1000
    if int(inputs[1]) > 1000:
        print('Error \n line: {} \n Service Capacity must not be greater than 1000'.format(line))
        return False
    if int(inputs[1]) <= 0:
        print('Error \n line: {} \n Service Capacity must not be less than or equal to 0'.format(line))
        return False
    # check the number of tickets sold is not greater than the service capacity
    if int(inputs[2]) > int(inputs[1]):
        print('Error \n line: {} \n The number of tickets sold cannot be greater than the service capacity'.format(line))
        return False

    # check service name is valid
    if not validServiceName(inputs[3]):
        print("'Error \n line: {} \n The service name contains a char other than a-Z or single quote".format(line))

    # check the service date is valid
    if not validServiceDate(inputs[4]):
        print("'Error \n line: {} \n The service date is not valid".format(line))
        return False

    return True

#number of tickets sold for service
def ticketsSold(serviceNum):
    global pendingCentralServices
    try:
        cF = open(centralServicesFile, "r")         #open file for reading
    except:
        print("Error: Back office not run yet, no centralServicesFile")
        return 0
    lines = cF.readlines()                      #saves lines
    cF.close()
    for line in lines:
        lineComp = line.split(" ")
        #if this line is for the service number
        if str(serviceNum) in lineComp[0]:
            #return capacity
            return int(lineComp[2])
    #search pending services to be addec
    for line in pendingCentralServices:                      
        lineComp = line.split(" ")
        #if this line is for the service number
        if str(serviceNum) in lineComp[0]:
            #return capacity
            return int(lineComp[2])
    print("Error: Service number used to find service ticketsSold, not found")
    return 0

def serviceCapacity(serviceNum):
    global pendingCentralServices
    try:
        cF = open(centralServicesFile, "r")         #open file for reading
    except:
        print("Error: Back office not run yet, no centralServicesFile")
        return 0
    lines = cF.readlines()                      #saves lines
    cF.close()
    for line in lines:                      
        lineComp = line.split(" ")
        #if this line is for the service number
        print("servicenum in service capacity is: ", serviceNum)
        if str(serviceNum) in lineComp[0]:
            #return capacity
            return int(lineComp[1])
    for line in pendingCentralServices:                      
        lineComp = line.split(" ")
        #if this line is for the service number
        if str(serviceNum) in lineComp[0]:
            #return capacity
            return int(lineComp[1])
    print("Error: Service number used to find service capacity not found")
    return 0

#When a service is asked to be removed from front end, the front end handles
# it immediately by removing it from the physical file so it can not be used
# later in that session. Services created are also not able to be used until the
# next login so if a service is created then removed in the same session it will only
# exist in the pending valid services file and pending central services.
# we remove a service from the two pending lists
def removeService(serviceNumber, serviceName):
    index = 0
    removedPV = False
    removedPC = False
    removedCF = False

    if ticketsSold(serviceNumber) > 0:
        print("Error: Cannot delete a service with tickets sold for it")
        return
    for line in pendingCentralServices:
        lineComp = line.split(" ")
        if str(serviceNumber) == lineComp[0]:
            print("1")
            if str(serviceName) == lineComp[3]:
                print("2")
                del pendingCentralServices[index]
                removedPC = True
                #if names match can remove from pending valid services file also
                for pvsLine in pendingValidServices:
                    if str(serviceNumber) in pvsLine:
                        del  pendingValidServices[index]
                        removedPV = True
                    index += 1
            else:
                #if the names did not match the service needs to be added back into the valid services file for the 
                #front end to use. The service is delete from validServicesFile immediately by front end even if names dont
                #match. We must add it back.
                pendingValidServices.append(serviceNumber)
                print("Error: Cannot delete service. Service names did not match")
        index += 1
    index = 0

    #remove from central services file
    cF = open(centralServicesFile, "r")       #open file for reading
    lines = cF.readlines()                  #saves lines
    cF.close()                                  
    cF = open(centralServicesFile, "w+")       #open file for writing
    for line in lines:
        lineComp = line.split(" ")                      
        if lineComp[0] == str(serviceNumber):              #write line if not the one to delete
            #if service name matches
            if lineComp[3] == serviceName:
                removedCF = True
            else: 
                #already removed from valid services list but names didnt match so must add it back to valid services list
                if serviceNumber not in pendingValidServices:
                    print("Error: Could not remove service, names did not match")
                    pendingValidServices.append(serviceNumber)
                cF.write(line)
        else:
            cF.write(line)
    cF.close()

    
    if removedPV and removedPC:
        print("removed the service successfully")
    elif removedPC and not removedPV:
        print("removed from the pendingCentralServices file only")
    elif removedPV and not removedPC:
        print("removed from the pendingValidServices file only")
    elif removedCF:
        print("removed service from central services file")
    else:
        print("service not removed")
    return

def exchangeTickets(sourceService,destinationService,numberOfTickets):
    if( not inValidServices(sourceService) or not inValidServices(destinationService)):
        print("Error: One of the services is missing from the valid services file")
        return
    #reduce tickets sold for source
    modifyTicketsSold(sourceService,int(numberOfTickets)*-1)
    #increase tickets sold for destination
    modifyTicketsSold(destinationService,numberOfTickets)
    return


def modifyTicketsSold(serviceNumber, ticketsDiff):
    cF = open(centralServicesFile, "r")         #open file for reading
    lines = cF.readlines()                      #saves lines
    cF.close()
    index = 0

    for line in lines:                      
        lineComp = line.split(" ")
        if str(serviceNumber) in lineComp[0]:
            if int(lineComp[2])+ticketsDiff > serviceCapacity(serviceNumber) or int(lineComp[2])+ticketsDiff < 0:
                print("Error, invalid tickets sold value being created. Over service capcity or negative")
            else:
                ticketsSold = int(lineComp[2]) + ticketsDiff
                if len(str(ticketsSold)) == 2:
                    ticketsSold = "00" + str(ticketsSold)
                elif len(str(ticketsSold)) == 1:
                    ticketsSold = "000" + str(ticketsSold)
                lineComp[2] = ticketsSold
                line = " ".join(lineComp)
                #save the modifed line at its index
                lines[index] = line
        index += 1

    cF = open(centralServicesFile, "w")         #open for writing
    cF.write(lines)
    cF.close()
    return

#returns false for all dates that are outside a valid range
#true if a valid date
# 1980 to 2999
def validServiceDate(date):
    #check if the date is not the right lenght or contains a letter
    #if len(str(date)) != 8 or bool(re.search('[a-zA-Z]', str(date))):
    #    print("Error:Invalid date string length")
    #    return False
    #cretae a numeric list of the date values
    date = date.strip(' \t\n\r')
    dL = list(date)
    t = 0
    for x in dL:
        dL[t] = int(x)
        t += 1


    if dL[0] > 2 or dL[0] < 1:                                              #check illegal years (X000MMDD)
        print("Error: Invalid Date year \"thousand\"")
        return False
    if dL[0] == 1 and (dL[1] < 9 or (dL[1] == 9 and dL[2] < 8)):            #check illegal years in 20th centry (19XXMMDD)
        print("Error: Invalid Date century")
        return False
    if dL[4] > 1 or dL[4] < 0 or (dL[4] == 1 and dL[5] > 2) or (dL[4] == 0 and dL[5] == 0):     #check illegal monthes (YYYYXXDD)
        print("Error: Invalid Date month")
        return False
    if dL[6] > 3 or dL[6] < 0 or (dL[6] == 3 and dL[7] > 1) or (dL[6] == 0 and dL[7] == 0):      #check illegal day (YYYYMMXX)
        print("Error: Invalid Date day")
        return False
    #illegal day for respective month value
    #Jan, Mar, May, July, Aug, Oct, Dec, can not have more than 31 se
    if ((dL[4] == 0 and dL[5] == 1) or (dL[4] == 0 and dL[5] == 3) or (dL[4] == 0 and dL[5] == 5) or (dL[4] == 0 and dL[5] == 7) or (dL[4] == 0 and dL[5] == 8) or (dL[4] == 1 and dL[5] == 0) or (dL[4] == 1 and dL[5] == 2)) and (dL[6] >= 3 and dL[7] > 1):
        print("Error: Invalid Date day over month limit")
        return False 
    #Apr, June, Sept, Nov, can not have more than 30 days
    if ((dL[4] == 0 and dL[5] == 4) or (dL[4] == 0 and dL[5] == 6) or (dL[4] == 0 and dL[5] == 9) or (dL[4] == 1 and dL[5] == 1)) and (dL[6] >= 3 and dL[7] > 0):
        print("Error: Invalid Date day for Apr, June, Sept, Nov")
        return False 
    #Feb, disregarding leap years...
    if (dL[4] == 0 and dL[5] == 2) and (dL[6] >= 2 and dL[7] > 8):
        print("Error: Invalid Date day for leap years")
        return False
    return True

def inValidServices(service):
    global validServicesFile
    servicesFile = open(validServicesFile,"r")
    lines = servicesFile.readlines()
    servicesFile.close()
    for line in lines:
        line = re.sub(r"[\n\t\s]*", "", line)
        if str(service) == str(line):
            servicesFile.close()
            return True
    return False

def inPendingCentralService(service):
    for item in pendingCentralServices:
        if service == item.split(" ")[0]:
            return True
    return False

#returns true if the passed service number (as a string), 
#is in the valid services file, false otherwise
def validServiceNum(service):
    if str(service)[0]=="0" or len(service) != 5:
        print("Invalid service number")
        return False
    return True

# Parameter: String service_name
# Return: Booleam True/False
# Ture if service name in range a-z or A-z or single quote
# False otherwise
def validServiceName(service_name):
    if len(service_name) < 3 or len(service_name) >39:
        print("Invalid service name length")
        return False
    return True

def readServices():
    services = {}
    lastServiceNumber = 0  #to check that the input file has service numbers in order
    if not os.path.isfile(centralServicesFile):
        file_contents = open(centralServicesFile, 'w+')
    else:
        file_contents = open(centralServicesFile, 'r')
    for line in file_contents:
        verify = checkInputService(line)
        if not verify:
            pass

        inputs = line.split(' ')

        if int(inputs[0]) < lastServiceNumber:
            print('Warning - Input Service Number is less than last')
            #does nothing but prints the warning
            #TODO - maybe this needs to be a hard constraint and stop the reading

        inputs[0] = int(inputs[0])
        services[int(inputs[0])] = inputs

    #check that the services are in order of accending service number
    #since its a dict it doesnt have an order

    file_contents.close()
    return services

def readTransactionFile():
    transactions = []
    file_contents = open(summaryFile, 'r')

    for line in file_contents:
        transactions.append(line)

    file_contents.close()
    return transactions

#writes the new services to the valid services file.
def writePendingServicesList():
    global pendingValidServices
    global validServicesFile
    #open the services file with the "append" argument so older services 
    #persist in the file after logout and re-login
    #if there is a valid services file

    if os.path.exists(validServicesFile):
        with open(validServicesFile, 'r+') as sF:
            content = sF.read()
            lines = content.splitlines()
            #If there is more than just the default 00000 service number in the list
            #add the new content above
            if len(pendingValidServices) > 0:
                sF.seek(0, 0)
                sF.write('\n'.join(pendingValidServices) + '\n' + content)
    else:
        sF = open(validServicesFile,"w+")
        sF.write('\n'.join(pendingValidServices))
        sF.write('00000')

    sF.close()
    return

def writeCentralServicesList():
    global pendingCentralServices
    global centralServicesFile
    #open the services file with the "append" argument so older services 
    #persist in the file after logout and re-login
    #if there is a valid services file
    if os.path.exists(centralServicesFile):
        with open(centralServicesFile, 'r+') as cF:
            content = cF.read()
            lines = content.splitlines()
            #If there is more than just the default 00000 service number in the list
            #add the new content above
            if len(pendingCentralServices) > 0:
                cF.seek(0, 0)
                cF.write('\n'.join(pendingCentralServices) + '\n' + content)
    else:
        cF = open(centralServicesFile,"w+")
        cF.write('\n'.join(pendingCentralServices))
        cF.write('00000')

    cF.close()
    return

def applyTransactions(services, transactions):
    global pendingCentralServices
    global pendingValidServices

    for line in transactions:
        transaction = line.split(' ')

        serviceNumber = transaction[1].strip(' \t\n\r')
        numberOfTickets = transaction[2].strip(' \t\n\r')
        destinationService = transaction[3].strip(' \t\n\r')
        serviceName = transaction[4].strip(' \t\n\r')
        serviceDate = transaction[5].split('\n')[0].strip(' \t\n\r')

        if transaction[0] == 'CRE':
            print("Creating Service")
            printLog(logFile, "Creating Service ")
	    # check the data to make sure its valid
            if not inValidServices(serviceNumber) and validServiceNum(serviceNumber) and validServiceName(serviceName) and validServiceDate(serviceDate):
                if serviceNumber in pendingValidServices:
                    printLog(logFile, "Error: Already a valid service")
                    print("Error: Already a valid service")
                else:
                    printLog(logFile, serviceNumber + " pend to valid services")
                    pendingValidServices.append(serviceNumber)
                if inPendingCentralService(serviceNumber):
                    printLog(logFile, "Error: Already in centralServicesFile")
                    print("Error: Already in centralServicesFile")
                else:
                    printLog(logFile, serviceNumber + " pend to central services")
                    pendingCentralServices.append(serviceNumber + " 0030" + " 0000" + " " + serviceName + " " + serviceDate)
            else:
                printLog(logFile, "Invalid details for new service")
                print("Invalid details for new service")

        elif transaction[0] == 'DEL':
            print("Deleting Service")
            printLog(logFile, "Deleting Service ")
            #check that the data is valid
            if validServiceNum(serviceNumber) and validServiceName(serviceName):
                printLog(logFile, serviceNumber + " are deleted")
                removeService(serviceNumber, serviceName)
            else:
                printLog(logFile, "Error: Invalid details for service deletion")
                print("Error: Invalid details for service deletion")

        elif transaction[0] == 'SEL':
            print("Selling tickets for Service")
            printLog(logFile, "Selling tickets for Service ")
            if validServiceNum(serviceNumber) and inValidServices(serviceNumber):
                #positve value becuase adding to number of tickets sold
                modifyTicketsSold(serviceNumber, int(numberOfTickets))
                printLog(logFile, serviceNumber + " are sold")
            else:
                printLog(logFile, "Error: Invalid details for service selling")
                print("Error: Invalid details for service selling")

        elif transaction[0] == 'CAN':
            print("Canceling tickets Service")
            printLog(logFile, "Canceling tickets Service ")
            if validServiceNum(serviceNumber):
                #negative number of tickets becuase removing from number of tickets sold
                modifyTicketsSold(serviceNumber, int(numberOfTickets)*-1)
                printLog(logFile, serviceNumber + " are canceled")
            else:
                printLog(logFile, "Error: Invalid details for ticket cancel")
                print("Error: Invalid details for ticket cancel")

        elif transaction[0] == 'CHG':
            print("Changing tickets for Service")
            printLog(logFile, "Changing tickets for Service ")
            if validServiceNum(serviceNumber) and validServiceNum(destinationService):
                printLog(logFile, serviceNumber + " are changed")
                exchangeTickets(serviceNumber,destinationService,numberOfTickets)
            else:
                printLog(logFile, "Error: Invalid details for service deletion")
                print("Error: Invalid details for service deletion")

        elif transaction[0] == 'EOS':
            printLog(logFile, "End of transactions ")
            print("End of transactions")
            pass
        else:
            printLog(logFile, "ERROR: unrecongized transaction code ")
            print('ERROR: unrecongized transaction code: {}'.format(transaction[0]))

def main():
    printLog("test.txt", "hello\nTest")
    while True:
        initVariables()
        lock = True
        # wait animation until a transaction summary is detected
        while lock:
            print("QIES Backend - Team DJANGO")
            for x in range (0,6):
                if os.path.isfile(summaryFile):
                    lock = False
                b = "Waiting for frontend to complete" + "." * x
                print(b, end="\r")
                time.sleep(0.17)
            os.system('cls||clear')


        TransactionSummaryLines = readTransactionFile()
        servicesInformation = readServices()

        applyTransactions(servicesInformation,TransactionSummaryLines)

        writePendingServicesList()
        writeCentralServicesList()

        #so the front end can create a new one to trigger new transaction operations
        print("Back Office Work Completed")
        time.sleep(2)
        os.remove(summaryFile)

main()
