import time
import os.path
import os           #to enable folders to be made
import re
import sys          #to check passed argument to program

centralServicesFile = "centralServices.txt"
validServicesFile = "validServices.txt"
mergedTransactionSummaryFile = "transactionSummary.txt"

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

    # check that service capacities and number of tickets are 1 to 4 decimal digits

    if (len(str(inputs[1])) < 1) or (len(str(inputs[1])) > 4) or not str(inputs[1]).isdigit():
        print('Error \n line: {} \n The service capacity must be between 1 and 4 decimal digits'.format(line))
        return False
    if (len(str(inputs[2])) < 1) or (len(str(inputs[2])) > 4) or not str(inputs[2]).isdigit():
        print('Error \n line: {} \n The number of tickets must be between 1 and 4 decimal digits'.format(line))
        return False

    # check service capacities is not greater than 1000
    if int(inputs[1]) > 1000:
        print('Error \n line: {} \n Service Capacity must not be greater than 1000'.format(line))
        return False
    # check the number of tickets sold is not greater than the service capacity
    if int(inputs[2]) > int(inputs[1]):
        print('Error \n line: {} \n The number of tickets sold cannot be greater than the service capacity'.format(line))
        return False

    return True

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
def validServiceNum(service):
    global validServicesFile
    if service[0]=="0" or len(service) != 5 or [int(x) for x in str(service)][0] == 0:
        return false
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

def validServiceName(serviceName):
    if len(serviceName) < 3 or len(serviceName) > 39:
        return False
    else:
        return True

def readServices(file):
    services = {}
    lastServiceNumber = 0  #to check that the input file has service numbers in order
    file_contents = open(file, 'r')
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
    file_contents = open(file, 'r')

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


def applyTransactions(services, transactions):
    for line in transactions:
        transaction = line.split(' ')
        validData = True

        if transaction[0] == 'CRE':

            serviceNumber = transaction[1]
            serviceName = transaction[4]
            serviceDate = transaction[5].split('\n')[0]

            #TODO - check the data to make sure its valid
            # Set valid Data false if not

            if validData:
            	pendingValidServices.append(serviceNumber)
            	pendingCentralServices.append(serviceNumber + " 0030" + " 0000" + " " + serviceName + " " + serviceDate)


        elif transaction[0] == 'DEL':

            serviceNumber = transaction[1]
            serviceName = transaction[4]

            #TODO - check that the data is valid

            try:
                services.pop(int(serviceNumber))
            except:
                print('Warning - Serivce {}, does not exist. Cannot delete'.format(serviceNumber))


        elif transaction[0] == 'SEL':
            sourceService = transaction[1]
            numberOfTickets = transaction[2]

            try:
                services[int(sourceService)][2] = services[int(sourceService)][2] + numberOfTickets
            except:
                print('ERROR - service number does not exist')
                pass

        elif transaction[0] == 'CAN':

            sourceService = transaction[1]
            numberOfTickets = transaction[2]

            try:

                change = services[int(sourceService)][2] - numberOfTickets
                if change >= 0 :
                    services[int(sourceService)][2] = change
                else:
                    print('ERROR - number of tickets cannot be below 0')
                    pass
            except:
                print('ERROR - service number does not exist')
                pass

        elif transaction[0] == 'CHG':

            sourceService = transaction[1]
            numberOfTickets = transaction[2]
            destinationService = transaction[3]

            try:
                number_of_tickets_sold = services[int(sourceService)][2]
                change = number_of_tickets_sold - numberOfTickets
                if change >= 0:
                    services[int(sourceService)][2] = change
                else:
                    print('ERROR - number of tickets cannot be below 0')
                    pass

                services[int(destinationService)][2] = services[int(destinationService)][2] + numberOfTickets
            except:
                print('ERROR - service number does not exist')
                pass

        elif transaction[0] == 'EOS':
            pass
        else:
            print('ERROR - unrecongized transaction code: {}'.format(transaction[0]))

def main():

	initVariables()

	# wait animation until a transaction summary is detected
	while True:
		print("QIES Backend - Team DJANGO")
		for x in range (0,5):
			if os.path.isfile(mergedTransactionSummaryFile):
				break
			b = "Waiting for frontend day to end" + "." * x
			print(b, end="\r")
			time.sleep(0.17)
		os.system('cls||clear')

	TransactionSummaryLines = readTransactionFile()
	servicesInformation = readServices()

	applyTransactions(servicesInformation,TransactionSummaryLines)

	writePendingServicesList()
	writePendingServicesList()

	#so the front end can create a new one to trigger new transaction operations
	os.remove(mergedTransactionSummaryFile)

main()