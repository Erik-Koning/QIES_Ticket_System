

import os, sys
import filecmp


results = ""
total_tests = 0
correct_tests = 0

#TODO - change to dynamic paths
test_path = "C:/Users/K.S/Desktop/CISC327/CISC327_A3/CMPE 327 Assignment 1/CMPE 327 Project/Testing"
result_path = "C:/Users/K.S/Desktop/CISC327/CISC327_A3/CMPE 327 Assignment 1/CMPE 327 Project/Results"


def printFiles(dir):
    for file in os.listdir(dir):
        if os.path.isdir(dir + "/" + file):
            printFiles(dir + "/" + file)
        else:
            printFiles(dir + "/" + file)


def testcase(dir):
    global total_tests, correct_tests

    #parse out the directory numberes to use them for file location
    end_of_dir = dir.rsplit('/',1)[1]
    type, number = end_of_dir.rsplit('.', 1)
    pretext = "test_case_" + type + "_" + number

    #collect the three files
    input_file = pretext + "_input_file.txt"
    output_transaction_summary_file = pretext + "_output_transaction_summary.txt"
    services_file = pretext + "_services_file.txt"

    #run the test case using the files
    os.system('python a2.py ' + services_file + ' ' + input_file) #havnt tested

    #compare the result file with the files
    #sample result directory result_path + 1.Login + 1.1 + results.txt
    test_type = dir.rsplit('/',2)[1]
    result_file = result_path + "/" + test_type + "/" + end_of_dir + "/results.txt"
    result = filecmp.cmp(output_transaction_summary_file, result_file)

    #report on results
    total_tests += 1
    if result:
        correct_tests += 1


def runTesting(dir):
    for file in os.listdir(dir):
        if os.path.isdir(dir + "/" + file):
            runTesting(dir + "/" + file)
        else:
            testcase(dir)
            break


#printFiles(test_path)
runTesting(test_path)

#print output file for all of testing
