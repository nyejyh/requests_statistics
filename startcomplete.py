#!/usr/bin/env python

# Calculate for requests started, requests completed.
# Written by Jason Huang

# Import libraries
import os
import re

class Lister() :

    # obtain the said directory
    def __init__(self, directory) :
        self.directory = directory

    # compile the first directory
    def findDirectory(self) :
        reqStartCount = 0 # running counter for started requests
        reqFinishCount = 0 # running counter for finished requests
        reqFailCount = 0 # requests did not start or finish
        # os.listdir() returns the names of each directory.
        fDir = os.listdir(self.directory)
        # os.path.abspath returns normalized absolutized version of the path.
        # os.path.join join 1 or more path components intelligently.
        for z in range(len(fDir)):
            sDir = os.listdir(os.path.abspath(os.path.join("/data/logstash/" +
            fDir[z])))

            # reading test
            for i in range(len(sDir)):
                filename = sDir[i]
                cracktext = open("/data/logstash/%s/%s" % (fDir[z], filename), "r")

                with cracktext :
                    # Define variables
                    threshold = 500 # expected combination of contents and extras
                    crackedLine = (cracktext.readline()).split() # cut up line to list
                    print crackedLine
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
                    # Run tests
                    print firstProgress, secondProgress, finalProgress
                    # Calculations 
                    compProgress = int(finalProgress[0]) - int(secondProgress[0])
                    diffProgress = int(secondProgress[0]) - int(firstProgress[0])
                    # Count the requests started, # of times firstProgress is zero
                    if firstProgress[0] == "0" and totalByte > threshold :
                        reqStartCount += 1
                    elif compProgress == 1 and totalByte > diffProgress :
                        reqFinishCount += 1
                    elif compProgress != 1 :
                        reqFailCount += 1
                    else :
                        raise ValueError("None of the counters changed.")
                    print progressBar
                    print totalByte
                    print firstProgress
                    print secondProgress
                    print finalProgress
                    print "The difference between final and second is: %s" % compProgress
                    print "The calculated difference in progress is: %s" % diffProgress
                    print "The total requests started is: %s" % reqStartCount
                    print "The total requests completed is: %s" % reqFinishCount
                    print "The total requests failing is: %s" % reqFailCount
                    cracktext.close()

def main() :
    HEADDIR = Lister("/data/logstash/")
    HEADDIR.findDirectory()

if __name__ == "__main__" :
    main()
