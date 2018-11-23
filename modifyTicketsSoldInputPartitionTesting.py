import time
import os.path
import os           #to enable folders to be made
import re
import sys          #to check passed argument to program
import filecmp
from shutil import copy2

rootDir = os.getcwd()
testReultsPath = rootDir + '\\backEndResults.txt'
testsPath = os.getcwd() + '\\ticketCancelation_testing'
testLogFile = "modifyTicketsSoldLog.txt"
testingLogNameFile = "logFileName.txt"
resultsFile = "testingResults.txt"
previousLogLength = 0

def calculateResult(testName):
    global reportResults
    global previousLogLength
    log = open(testLogFile, "r")
    logLines = log.readlines()
    log.close()
    #there was an error log on the previous test
    reportResults.write(testName + ",")
    if len(logLines) > previousLogLength:
        for i in range(previousLogLength,len(logLines)):
            reportResults.write(logLines[i])
        previousLogLength = len(logLines)
    #no error
    else:
        reportResults.write("PASS")
    reportResults.write("\n")


#engine that sends the correct files to backend and activates the tests
def test():
    global rootDir
    global reportResults

    # set log file name for backend to use
    f = open(testingLogNameFile,"w")
    f.write(testLogFile)
    f.close()

    #make results file
    reportResultsFile = testLogFile.rsplit('.',1)[0] + "RESULTS.txt"
    reportResults = open(reportResultsFile, "w")
    reportResults.write("Test,Result,Discription\n")

    #go over each testing directory in testsPath and copy over the necessary files to run the back end from that testing folder
    for root, dirs, files in os.walk(testsPath):
        for d in dirs:
            testingDir = testsPath + "\\" + d
            for root, dirs, files in os.walk(testingDir):
                #if another layer of directories (in case of applyTransactions Testing)
                if len(dirs) > 0:
                    for d2 in dirs:
                        testingDir2 = testingDir + "\\" + d2
                        for root, dirs, files in os.walk(testingDir2):
                            if len(dirs) > 0:
                                print("Error: Not traversing further folders")
                            else:
                                #move summary file to end of list
                                index = files.index("transactionSummary.txt")
                                files.append(files.pop(index))
                                print("running test:\n"+testingDir2)
                                for file in files:
                                    copy2(testingDir2 + "\\" + file,rootDir)
                                    #wait a second for backend to output its stuff
                                time.sleep(5)
                                testName = testingDir2.rsplit('\\',1)[1]
                                calculateResult(testName)
                else:
                    #move summary file to end of list
                    index = files.index("transactionSummary.txt")
                    files.append(files.pop(index))
                    print("running test:\n"+testingDir)
                    for file in files:
                        copy2(testingDir + "\\" + file,rootDir)
                        #wait a second for backend to output its stuff
                    time.sleep(5)
                    testName = testingDir.rsplit('\\',1)[1]
                    calculateResult(testName)
    reportResults.close()



                



test()