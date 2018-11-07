import time
import os.path
import os           #to enable folders to be made
import re
import sys          #to check passed argument to program

new_central_services_file = "centralServices.txt"
new_valid_services_file = "validServices.txt"
mergedTransactionSummaryFile = "mergedTransactionSummary.txt"


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


def readTransactionFile(file):
    transactions = []
    file_contents = open(file, 'r')

    for line in file_contents:
        transactions.append(line)

    file_contents.close()
    return transactions


def applyTransactions(services, transactions):
    for line in transactions:
        transaction = line.split(' ')

        if transaction[0] == 'CRE':

            serviceNumber = transaction[1]
            serviceName = transaction[4]
            serviceDate = transaction[5].split('\n')[0]

            #TODO - check the data to make sure its valid

            services[int(serviceNumber)] = [int(serviceNumber), 0, 0, serviceName, serviceDate] #TODO - check where you get service capacity from


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


def writeOuputFiles(services):
    valid_services_file = open(new_valid_services_file, 'w')
    central_services_file = open(new_central_services_file, 'w')

    for key in services:
        valid_services_file.write(str(key) + "\n")
        result = ""
        for info in services[key]:
            result += str(info) + " "
        central_services_file.write(result[:len(result)-1] + "\n") #write to file without last space

    central_services_file.close()
    valid_services_file.close()

def main():
	

if len(sys.argv) > 2:

    old_central_services_file = sys.argv[1]
    merged_transaction_summary_file = sys.argv[2]

    services = readServices(old_central_services_file)

    transactions = readTransactionFile(merged_transaction_summary_file)

    applyTransactions(services, transactions)

    writeOuputFiles(services)

else:
    print('Error - Incorrect call to backoffice.py. More input files are required')


main()