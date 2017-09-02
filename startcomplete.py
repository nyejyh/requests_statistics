#!/usr/bin/env python

# Calculate for requests started, requests completed.
# Written by Jason Huang

# Import libraries
from __future__ import division
import os
import re

class Lister() :

    # obtain the said directory
    def __init__(self, directory) :
        self.directory = directory

    # compile the first directory
    def findDirectory(self) :
        reqFileCount = 0 # running counter for total files
        reqStartCount = 0 # running counter for started requests
        reqFinishCount = 0 # running counter for finished requests
        reqFailCount = 0 # requests did not start or finish
        # os.listdir() returns the names of each directory.
        fDir = os.listdir(self.directory)
        # os.path.abspath returns normalized absolutized version of the path.
        # os.path.join join 1 or more path components intelligently.
        for z in range(len(fDir)):
            fileCount = 0 # running counter files per folder
            startCount = 0 # running counter req started per folder
            finishCount = 0 # running counter req finish per folder
            failCount = 0 # running counter req fail per folder

            sDir = os.listdir(os.path.abspath(os.path.join("/data/logstash/" +
            fDir[z])))

            # reading test
            for i in range(len(sDir)):
                filename = sDir[i]
                cracktext = open("/data/logstash/%s/%s" % (fDir[z], filename), "r")
                fileCount += 1 # how many files per folder
                reqFileCount += 1 # the total file count

                with cracktext :
                    # Define variables
                    threshold = 500 # expected combination of contents and extras
                    crackedLine = (cracktext.readline()).split() # cut up line to list
                    totalByte = crackedLine[12] # the total byte from list
                    # Find the anchor
                    for count, elem in enumerate(crackedLine) :
                        if elem == ("ABORT") :
                            anchor = count
                        elif elem == ("SUCCESS") :
                            anchor = count
                        elif elem == ("PARTIAL") :
                            anchor = count 
                    progressBar = crackedLine[anchor + 1] # always after anchor    
                    # Pull out 3 parts of the progressBar to calculate
                    firstProgress = re.findall(r"(\d+)-", progressBar)
                    secondProgress = re.findall(r"(\d+)/", progressBar)
                    finalProgress = re.findall(r"/(\d+)", progressBar)
                    # Calculations 
                    compProgress = int(finalProgress[0]) - int(secondProgress[0])
                    diffProgress = int(secondProgress[0]) - int(firstProgress[0])
                    # Count the requests started, # of times firstProgress is zero
                    if firstProgress[0] == "0" and totalByte > threshold :
                        reqStartCount += 1
                        startCount += 1
                    elif compProgress == 1 and totalByte > diffProgress :
                        reqFinishCount += 1
                        finishCount += 1
                    elif compProgress != 1 :
                        reqFailCount += 1
                        failCount += 1
                    else :
                        raise ValueError("None of the counters changed.")
                    cracktext.close()

            startCalc = "{0:.0f}%".format(startCount / fileCount)
            finishCalc = "{0:.0f}%".format(finishCount / fileCount)
            failCalc = "{0:.0f}%".format(failCount / fileCount)

            print fDir[z] + ": %s files, %s (%s) started, %s (%s) finish, %s (%s) fail." % \
            (fileCount, startCount, startCalc, finishCount, finishCalc, failCount, failCalc)
        
        try :
            StartCalc = float(reqStartCount / reqFileCount)
            FinishCalc = float(reqFinishCount / reqFileCount)
            FailCalc = float(reqFailCount / reqFileCount)
        except ZeroDivisionError :
            StartCalc = 0
            FinishCalc = 0
            FailCalc = 0
        print "Total requests started: %s (%.2f%%)" % (reqStartCount, StartCalc)
        print "Total requests completed is: %s (%.2f%%)" % (reqFinishCount, FinishCalc)
        print "Total requests failing is: %s (%.2f%%)" % (reqFailCount, FailCalc)

def main() :
    HEADDIR = Lister("/data/logstash/")
    HEADDIR.findDirectory()

if __name__ == "__main__" :
    main()
