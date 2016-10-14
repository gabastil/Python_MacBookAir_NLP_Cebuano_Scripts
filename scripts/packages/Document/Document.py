#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# Name:     Document.py
# Version:  1.0.0
# Author:   Glenn Abastillas
# Date:     September 09, 2015
#
# Purpose: Allows the user to:
#           1.) Read in a document (.txt)
#           2.) Find a word in the loaded document (.txt)
#           3.) Save results of word search along with leading and trailing text whose length is controlled by the user.
#
# To see the script run, go to the bottom of this page.
#
# This class is directly inherited by the following classes:
#   - DocumentPlus.py
# 
# Updates:
# 1. [2016/02/29] - changed wording of notes in line 16 from '... class is used in the following ...' to '... class is directly inherited by the following ...'.
# 2. [2016/03/25] - removed methods: 	__pad(), find(), saveFile()
# 3. [2016/03/25] - revised methods: 	load(): changed to initialize(), save(): took place of saveFile() - made static, open(): took place of openFile() - made static, toString(), reset(), setSavePath()
# 4. [2016/03/25] - added 	methods: 	getSavePath(), getFilePath(), getDocument(), setFilePath()
# - - - - - - - - - - - - -
"""	creates a manipulable document object from a text file.

The Document class is used to represent text files as objects for further
use by other classes. This is a base class and does not inherit from other
classes. Two methods exist in this class that can be used as static methods:
(1) open(doc): open a specified document and (2) save().

"""
__author__      = "Glenn Abastillas"
__copyright__   = "Copyright (c) September 9, 2015"
__credits__     = "Glenn Abastillas"

__license__     = "Free"
__version__     = "1.0.0"
__maintainer__  = "Glenn Abastillas"
__email__       = "a5rjqzz@mmm.com"
__status__      = "Deployed"

class Document(object):

	def __init__(self, filePath = None, savePath = None):
		""" constructor for this class with two parameters
			@param	filePath: input file
			@param	savePath: output location
		"""
		
		self.filePath = filePath	# Store a String of the file path
		self.savePath = savePath	# Store a String of the save path
		
		self.textFile = list()		# Store a list of lines from initialized file
		self.dataList = list()		# [DEPRECATE] remove - only used in asString() and reset()?
		
		self.loaded   = False		# Is this object initialized

		if filePath is not None:
			self.initialize(filePath)
			
	def initialize(self, filePath=None):
		"""	opens indicated file and loads it into memory
			@param filePath: path to file to load
		"""
		self.textFile = self.open(self.filePath).split()
		self.filePath = filePath
		self.loaded   = True

	def open(self, filePath=None, splitLines=False, splitTabs=False):
		"""	opens an indicated text file for processing
			@param	filePath: path of file to load.
			@return	String of opened text file
		"""
		with open(filePath, 'r') as fileIn1:

			readFile = fileIn1.read()

			if splitLines==False and splitTabs==False:
				return readFile

			if splitLines==True and splitTabs==True:
				return [line.split('\t') for line in readFile.splitlines()]

			if splitLines==True:
				return readFile.splitlines()

			if splitTabs==True:
				return readFile.split('\t')

	def save(self, savePath=None, saveContent=None, saveType='w'):
		"""	write content out to a file
			@param	savePath: name of the file to be saved
			@param	saveContent: a string of the contents to be saved
			@param	saveType: indicate overwrite ('w') or append ('a')
		"""
		saveFile = open(savePath, saveType)
		saveFile.write(saveContent)
		saveFile.close()

	def getSavePath(self):
		"""	get the save path
			@return String of the save path
		"""
		return self.savePath

	def getFilePath(self):
		""" get the file path
			@return	String of the file path
		"""
		return self.filePath

	def getDocument(self):
		"""	Get the file as lines in a list
			@return	List of lines from initialized file
		"""
		return self.textFile

	def setSavePath(self, savePath):
		"""	set the location for saved files
			@param	savePath: location to store saved files
		"""
		self.savePath = savePath

	def setFilePath(self, filePath):
		"""	set this object to a new file
			@param	filePath: location to new file
		"""
		self.initialize(filePath)

	def toString(self, textType = "text", returnToString = False):
		"""	prints the loaded text file or the data list onto the screen.
			@param	textType: indicate 'text' or 'data'
			@param	returnToString: return a String
			@return	String of the printed document
		"""

		if self.loaded:
			if textType == "text":
				print(self.textFile)
			elif textType == "data":
				print(str(self.dataList))
			else:
				print("Not a valid option.")
		else:
			print("No file loaded.")

		if returnToString:
			if textType == "text":
				return self.textFile
			elif textType == "data":
				return str(self.dataList)
			else:
				return None

	def reset(self):
		"""	reset all data in this class
		"""
		
		self.filePath = None	# Clear string
		self.savePath = None	# Clear string

		self.textFile = list()	# Assign to empty list
		self.dataList = list()	# Assign to empty list

		self.loaded   = False	# Reset state to False (i.e., not loaded)

if __name__ == "__main__":
	""" run as a script if this file is run as a stand-alone program
	"""
	
	d = Document("../../../data/test.txt")
	print d.getDocument()
