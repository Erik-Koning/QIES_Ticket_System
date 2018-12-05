import os
import os.path
from os import walk

#rootDir = os.getcwd()

def getTransactionSummaryFileArray():
    toReturn = []
    allFiles = next(os.walk('.'))[2]
    for f in allFiles:
        if "transactionSummary" in f and ".txt" in f:
            toReturn.append(f)
            
    return toReturn
    

def mergeTransactionSummaryFiles(rootDir):
    #global rootDir
    filenames = getTransactionSummaryFileArray()
    with open(rootDir + '\\dailyTransactionSummaryFile.txt', 'w') as outfile:
        for fname in filenames:
            with open(fname) as infile:
                outfile.write(infile.read() + '\n')

mergeTransactionSummaryFiles(os.getcwd())
