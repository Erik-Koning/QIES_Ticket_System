
import os, os.path, sys
import filecmp
from shutil import copy2


results = ""
total_tests = 0
correct_tests = 0


testsPath = os.getcwd() + '\\Testing'
resultPath = os.getcwd() + '\\Outputs'
rootDir = os.getcwd()

def writeOutputFile():
    file = os.getcwd() + "\\Master_Results.txt"
    global results
    results += "\n\nCorrect Test Cases: " + str(correct_tests) + "/" + str(total_tests)

    f = open(file, "w")
    f.write(results)
    f.close()

def printFiles(dir):
    for file in os.listdir(dir):
        if os.path.isdir(dir + "/" + file):
            printFiles(dir + "/" + file)
        else:
            printFiles(dir + "/" + file)


def testcase(fullPath):
    global total_tests, correct_tests
    global reportResults

    #parse out the directory numberes to use them for file location
    dirOfTest = fullPath.rsplit('\\',1)[0]
    inputTest = fullPath.rsplit('\\',1)[1]

    pretext = inputTest.rsplit('_',2)[0]

    outputFile = inputTest.replace("input","output")
    expectedOutputFile = pretext + "_ouput_transaction_summary.txt"
    servicesList = pretext + "_services_file.txt"
    testId = fullPath.rsplit('\\',2)[1]
    outputFilePath = rootDir + "\\" + "Outputs" + "\\" + testId + "\\" + outputFile
    expectedOutputFilePath = dirOfTest + "\\" + expectedOutputFile

    #move services list to root for front end to use for this test
    #This will overwrite the current valid services list
    copy2(dirOfTest + "\\" + servicesList, rootDir)

    #run the test case using the files
    os.system('python a2.py ' + fullPath) #havnt tested

    #compare the result file with the files
    #sample result directory result_path + 1.Login + 1.1 + results.txt
    result = filecmp.cmp(expectedOutputFilePath, outputFilePath)
    
    reportResults.write("Test: " + testId + "," + str(result))
    return

#run all tests for test files below the argument dir
def runTesting(testsPath):
    global reportResults

    testReultsPath = rootDir + "\\" + "testReults.csv"
    reportResults = open(testReultsPath,"w+")
    reportResults.write("Test,Result,Discription\n")
    for root, dirs, files in os.walk(testsPath):
        for f in files:
            #it is an input test "flie"
            if "input_f" in f:
                fullPath = os.path.join(root,f)
                testcase(fullPath)

    reportResults.close()
    return
#printFiles(test_path)
runTesting(testsPath)
#print output file for all of testing
writeOutputFile()