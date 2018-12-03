import os
import os.path
from os import walk

rootDir = os.getcwd()
testDir = rootDir + '\\merge_testing'

def getTransactionSummaryFileArray():
    global testDir
    print(testDir)
    toReturn = []
    for root, dirs, files in os.walk(testDir):
        print(root)
        for f in files:
            print(f)
            if "transactionSummary" in f and ".txt" in f:
                print(f)
                toReturn.append(f)
    return toReturn
    

def main():
    filenames = getTransactionSummaryFileArray()
    with open('dailyTransactionSummaryFile.txt', 'w') as outfile:
        for fname in filenames:
            print(fname)
            with open(fname) as infile:
                outfile.write(infile.read())

main()
