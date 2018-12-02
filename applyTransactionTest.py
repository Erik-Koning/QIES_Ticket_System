
import os, os.path, sys
import filecmp
from shutil import copy2
import difflib


results = "applyTransaction_Test_Reults.csv"
total_tests = 0
correct_tests = 0


testsPath = os.getcwd() + '\\applyTransactions_testing'
resultPath = os.getcwd() + '\\applyTransactions_outputs'
rootDir = os.getcwd()

#def writeOutputFile():
    #file = os.getcwd() + "\\Master_Results.txt"
    #global results
    #results += "\n\nCorrect Test Cases: " + str(correct_tests) + "/" + str(total_tests)

    #f = open(file, "w")
    #f.write(results)
    #f.close()

#def printFiles(dir):
    #for file in os.listdir(dir):
    #    if os.path.isdir(dir + "/" + file):
    #        printFiles(dir + "/" + file)
    #    else:
    #        printFiles(dir + "/" + file)
def showResults():
    reportResults = open(results,"r")
    for line in reportResults:
        line.replace(","," ")
        print(line)

def testcase(fullPath):
    global total_tests, correct_tests
    global reportResults

    #parse out the directory numberes to use them for file location
    dirOfTest = fullPath.rsplit('\\',1)[0]
    inputTest = fullPath.rsplit('\\',1)[1]

    pretext = inputTest.rsplit('_',2)[0]

    outputFile = "resultLogFile.txt"
    expectedOutputFile = "logFile.txt"
    validServicesList = "validServices.txt"
    centralServiceList = "centralServices.txt"
    testId = fullPath.rsplit('\\',2)[1]
    outputFilePath = rootDir + "\\" + "applyTransactions_outputs" + "\\" + testId + "\\" + outputFile
    expectedOutputFilePath = dirOfTest + "\\" + expectedOutputFile

    #move services list to root for front end to use for this test
    #This will overwrite the current valid services list
    #**********The copy function may take too long....
    print(dirOfTest)
    copy2(dirOfTest + "\\" + validServicesList, rootDir + "\\" + "validServices.txt")
    copy2(dirOfTest + "\\" + centralServiceList, rootDir + "\\" + "centralServices.txt")

    #run the test case using the files
    os.system('python backOffice.py ' + fullPath)

    #compare the result file with the files
    #sample result directory result_path + 1.Login + 1.1 + results.txt
    result = filecmp.cmp(expectedOutputFilePath, outputFilePath)
    
    expectedLinesFile = open(expectedOutputFilePath,"r+")
    outputLinesFile = open(outputFilePath,"r+")
    expectedLines = expectedLinesFile.read().strip().splitlines()
    outputLines = outputLinesFile.read().strip().splitlines()

    diffResult = ""
    for line in difflib.unified_diff(expectedLines, outputLines, fromfile='Expected', tofile='Resultant', lineterm=''):
        diffResult += line

    reportResults.write("Test: " + testId + "," + str(result) + "," + diffResult + "\n")
    return

#run all tests for test files below the argument dir
def runTesting(testsPath):
    global reportResults
    testReultsPath = rootDir + "\\" + results
    #reportResults = open(testReultsPath,"w+")
    #reportResults.write("Test,Result,Discription\n")
    for root, dirs, files in os.walk(testsPath):
        for f in files:
            #it is an input test "flie"
            if "transaction" in f:
                fullPath = os.path.join(root,f)
                print(fullPath)
                testcase(fullPath)

    #reportResults.close()
    return
#printFiles(test_path)
runTesting(testsPath)
#show results saved to .csv also in terminal output
showResults()
