'''
Created on Feb 22, 2013

@author: u5682
'''

from datetime import datetime
import os, sys, pickle

import subprocess

from time import sleep


import xml.dom.minidom
from xml.dom.minidom import Node

class DistributedTask(object):
	'''
	classdocs
	'''

	def __init__(self, fileName = None):
		'''
		Constructor
		'''
		self.creationDate = datetime.now()

		if fileName == None:
	
			self.executable = ""
			self.arguments = []
	
			self.outputPath = ""
			self.outputFile = ""
	
			self.errorPath = ""
			self.inputPath = ""
	
			self.inputSandbox = ""
			self.outputSandbox = ""
	
			self.workingDirectory = ""
	
			self.requirements = ""
	
			self.inputFiles = []
			self.outputFiles = []
	
			self.jobName = ""
		
			self.nativeSpecification = ""

		else:
			self.fromXML(fileName)

		
	
	def fromXML(self, fileName):
		
		#primerp rseamos el fichero
		doc = xml.dom.minidom.parse(fileName)
		self.executable = obtainText(doc, 'executable')
		self.arguments = obtainTextList(doc, 'arguments', 'argument')

		self.outputPath = obtainText(doc, 'outputPath')
		self.outputFile = obtainText(doc, 'outputFile')

		self.errorPath = obtainText(doc, 'errorPath')
		self.inputPath = obtainText(doc, 'inputPath')

		self.inputSandbox = obtainText(doc, 'inputSandbox')
		self.outputSandbox = obtainText(doc, 'outputSandbox')

		self.workingDirectory = obtainText(doc, 'workingDirectory')

		self.requirements = obtainText(doc, 'requirements')

		self.inputFiles = obtainTextList(doc, 'inputFiles', 'inputFile')
		self.outputFiles = obtainTextList(doc, 'outputFiles', 'outputFile')

		self.jobName = obtainText(doc, 'jobName')
	
		self.nativeSpecification = obtainText(doc, 'nativeSpecification')


		#y ahora creamos un objeto nuevo con la informacion obtenida

	def getArguments(self):
		argumentList = []
		for arg in self.arguments:
			argumentList.append(arg.encode('ascii','ignore'))
		return argumentList

	def getInputFiles(self):
		inputFileList = []
		for inputF in self.inputFiles:
			inputFileList.append(inputF.text)
		return inputFileList
	
	def getOutputFiles(self):
		outputFileList = []
		for outputF in self.outputFiles:
			outputFileList.append(outputF.text)
		return outputFileList
	
			
			
	def outputFilesExist(self):
		for outputF in self.outputFiles:
			requiredFile = self.taskInfo.workingDirectory + "/" + outputF.text
			if  not os.path.exists(requiredFile):
				print("OUTPUT FILE MISSING: " + requiredFile)
				return False
		return True
		
		
	
		
def obtainText(node, tagName):
	L = node.getElementsByTagName(tagName)
	auxText = ""
	for node2 in L:
		for node3 in node2.childNodes:
			if node3.nodeType == Node.TEXT_NODE:
				auxText +=node3.data
	return auxText


def obtainTextList(node, fatherTagName, sonTagName):
	L = node.getElementsByTagName(fatherTagName)
	auxTextArray = []
	for node2 in L:
		L2 = node.getElementsByTagName(sonTagName)
		for node3 in L2:
			for node4 in node3.childNodes:
				if node4.nodeType == Node.TEXT_NODE:
					auxTextArray.append(node4.data)

	return auxTextArray

