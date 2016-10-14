#!/usr/bin/python
# -*- coding: UTF-8 -*-
# Author: Glenn Abastillas

from packages.Parse.Parse import Parse
from packages.Parse.Extractor import Extractor
from packages.Document.Spreadsheet import Spreadsheet
import os

#=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*
#=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*

dataFolder   = "/Users/ducrix/Documents/Research/Python/data"
outputFolder = "/Users/ducrix/Documents/Research/Python/output"
os.chdir(dataFolder)

folderList = os.listdir(".")

#=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*
#=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*

s = Spreadsheet()
t = ""

for f in folderList:
    if os.path.isfile(f):
        if f.split(".")[-1] == "txt":
            fin = open(f, "r")
            t   += fin.read()
            fin.close()

p = Parse(t)
e = Extractor(t)

#=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*
#=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*

bigrams = []

for w in e.getWordList():
    bigrams.append([w])

#=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*
#=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*
"""
bigrams = []

for w in e.getWordSet(asList = True):
    bigrams += e.getPairs(w, includeCount = True)
"""
#=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*
#=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*
os.chdir(outputFolder)
if len(bigrams) > 0:
    s.set_spreadsheet_from_list(bigrams)
    s.save_spreadsheet("_BIG_FILE_DEAL")
else:
    print "No pairs found."