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

def initVariables():
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
    if len(str(inputs[1])) != 5 or not str(inputs[1]).isdigit():
        print('Error \n line: {} \n The service capacity must be between 1 and 4 decimal digits'.format(line))
        return False

    # check that service capacities are 1 to 4 decimal digits
    if (len(str(inputs[2])) < 1) or (len(str(inputs[2])) > 4) or not str(inputs[2]).isdigit():
        print('Error \n line: {} \n The number of tickets must be between 1 and 4 decimal digits'.format(line))
        return False
    # check service capacities is not greater than 1000
    if int(inputs[2]) > 1000:
        print('Error \n line: {} \n Service Capacity must not be greater than 1000'.format(line))
        return False
    if int(inputs[2]) <= 0:
        print('Error \n line: {} \n Service Capacity must not be less than or equal to 0'.format(line))
        return False

    # check the number of tickets sold is not greater than the service capacity
    if int(inputs[3]) > int(inputs[2]):
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
    lines = sF.readlines()                      #saves lines
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
    lines = sF.readlines()                      #saves lines
    cF.close()
    for line in lines:                      
        lineComp = line.split(" ")
        #if this line is for the service number
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
#it immediately by removing it from the physical file so it can not be used
# later in that session. Services created are also not able to be used until the
# next login so if a service is created then removed in the same session it will only
# exist in the pending valid services file and pending central services.
# we remove a service from the two pending lists
def removeService(serviceNumber, serviceName):
    index = 0
    removedPV = False
    removedPC = False

    if ticketsSold(serviceNum) > 0:
        print("Error: Cannot delete a service with tickets sold for it")
        return
    for line in pendingCentralServices:
        lineComp = line.split(" ")
        if str(serviceNumber) in lineComp[0]:
            if serviceName == lineComp[3]:
                del pendingCentralServices[index]
                removedPC = True
            else:
                print("Error: Cannot delete service. Service names did not match")
        index += 1
    index = 0
    for line in pendingValidServices:
        if str(serviceNumber) in line:
            del  pendingValidServices[index]
            removedPV = True
        index += 1
    
    if removedPV and removedPC:
        print("removed the service successfully")
    elif removedPC and not removedPV:
        print("removed from the pendingCentralServices file only")
    elif removedPV and not removedPC:
        print("removed from the pendingValidServices file only")
    else:
        print("service not removed")

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
    lines = sF.readlines()                      #saves lines
    cF.close()

    cF = open(centralServicesFile, "w")         #open for writing
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
        cF.write(line)
    cF.close()

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

def inValidServices(service):
    global validServicesFile
    servicesFile = open(validServicesFile,"r")
    lines = servicesFile.readlines()
    for line in lines:
        line = re.sub(r"[\n\t\s]*", "", line)
        if service == line:
            servicesFile.close()
            return True
    servicesFile.close()
    return False

#returns true if the passed service number (as a string), 
#is in the valid services file, false otherwise
def validServiceNum(service):
    if service[0]=="0" or len(service) != 5 or [int(x) for x in str(service)][0] == 0:
        return false
    return False

# Parameter: String service_name
# Return: Booleam True/False
# Ture if service name in range a-z or A-z or single quote
# False otherwise
def validServiceName(service_name):
    if len(service_name) < 3 or len(service_name) >39:
        return False
    for aChar in service_name:
        if ord(aChar) not in range(65, 91) and ord(aChar) not in range(97, 123) and ord(aChar) != 39:
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
    print(pendingValidServices)
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
    print(pendingCentralServices)
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

        serviceNumber = transaction[1]
        numberOfTickets = transaction[2]
        destinationService = transaction[3]
        serviceName = transaction[4]
        serviceDate = transaction[5].split('\n')[0]

        if transaction[0] == 'CRE':
            print("Creating Service")
            # check the data to make sure its valid
            if not inValidServices(serviceNumber) and validServiceNum(serviceNumber) and validServiceName(serviceName) and validServiceDate(serviceDate):
                pendingValidServices.append(serviceNumber)
                pendingCentralServices.append(serviceNumber + " 0030" + " 0000" + " " + serviceName + " " + serviceDate)

        elif transaction[0] == 'DEL':
            print("Deleting Service")
            #check that the data is valid
            if validServiceNum(serviceNumber) and validServiceName(serviceName):
                removeService(serviceNumber, serviceName)

        elif transaction[0] == 'SEL':
            print("Selling tickets for Service")
            if validServiceNum(sourceService) and inValidServices(sourceService):
                #positve value becuase adding to number of tickets sold
                modifyTicketsSold(sourceService, int(numberOfTickets))

        elif transaction[0] == 'CAN':
            print("Canceling tickets Service")
            if validServiceNum(sourceService):
                #negative number of tickets becuase removing from number of tickets sold
                modifyTicketsSold(sourceService, int(numberOfTickets)*-1)

        elif transaction[0] == 'CHG':
            print("Changing tickets for Service")
            if validServiceNum(sourceService) and validServiceNum(destinationService):
                exchangeTickets(sourceService,destinationService,numberOfTickets)

        elif transaction[0] == 'EOS':
            print("End of transactions")
            pass
        else:
            print('ERROR - unrecongized transaction code: {}'.format(transaction[0]))

def main():
    while True:
        initVariables()
        lock = True
        # wait animation until a transaction summary is detected
        while lock:
            print("QIES Backend - Team DJANGO")
            for x in range (0,6):
                if os.path.isfile(summaryFile):
                    lock = False
                b = "Waiting for frontend day to end" + "." * x
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
        time.sleep(20)
        os.remove(summaryFile)

main()
