'''
Created on Aug 20, 2012

@author: Manuel Rodriguez Pascual, <manuel.rodriguez.pascual@gmail.com>

	This file is part of gridwayController.

	gridwayController is free software: you can redistribute it and/or modify
	it under the terms of the GNU General Public License as published by
	the Free Software Foundation, either version 3 of the License, or
	(at your option) any later version.

	gridwayController is distributed in the hope that it will be useful,
	but WITHOUT ANY WARRANTY; without even the implied warranty of
	MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
	GNU General Public License for more details.

	You should have received a copy of the GNU General Public License
	along with gridwayController.  If not, see <http://www.gnu.org/licenses/>.
'''

from Argument import Argument
from InputFile import InputFile
from OutputFile import OutputFile
from TaskInfo import TaskInfo
from Host import Host
from datetime import datetime
import os

import xml.dom.minidom
from xml.dom.minidom import Node

from sqlalchemy import *
from sqlalchemy.orm import relationship, backref

from base import Base


class GridTask(Base):
	'''
	classdocs
	'''
	__tablename__ = 'gridTasks'
	id = Column(Integer, primary_key=True)
	templateLocation = Column(String)
	gwID = Column(String)
	hostID = Column(Integer, ForeignKey('hosts.id'))
	taskGroupID=Column(Integer, ForeignKey('taskGroups.id'))
	status = Column(String)
	

	creationDate = Column(DateTime)
	submissionDate = Column(DateTime)

	executionStartDate = Column(DateTime)
	endDate = Column(DateTime)
	
	retryNumber = Column(Integer)
	arguments = relationship("Argument", order_by="Argument.id", backref="gridTask")
	inputFiles = relationship("InputFile", order_by="InputFile.id", backref="gridTask")
	outputFiles = relationship("OutputFile", order_by="OutputFile.id", backref="gridTask")
	taskInfo = relationship("TaskInfo", uselist=False, backref="gridTask")

	host = relationship("Host", backref="gridTasks")
	taskGroup = relationship("TaskGroup",  backref="gridTasks")

	def __init__(self):
		'''
		Constructor
		'''
		self.gwID = "-1"
		self.status = "WAITING"
		self.hostID = -1		 
		self.creationDate = datetime.now()
		self.retryNumber = 0
		self.taskGroupID=-1
			
	def __repr__(self):
		solution = "<gridTask (" +  str(self.id) + ")>\n"
		solution += "	" + self.taskInfo.__repr__()+ "\n"
		solution +="	<Arguments>"
		for argument in self.arguments:
				solution += "		" + argument.__repr__()+ "\n"
		solution +="	</Arguments>"+ "\n"
		
		solution +="	<InputFiles>"+ "\n"
		for inputF in self.inputFiles:
				solution += "		" + inputF.__repr__()+ "\n"
		solution +="	</InputFiles>"+ "\n"
		
		solution +="	<OutputFiles>"+ "\n"
		for outputF in self.outputFiles:
				solution += "		" + outputF.__repr__()+ "\n"
		solution +="	</OutputFiles>"   + "\n"	 
		solution += "</gridTask>" 
		
		return solution
		
	
	def fromXML(self, taskGroup, fileName):
		
		#primerp rseamos el fichero
		doc = xml.dom.minidom.parse(fileName)
		executable = obtainText(doc, 'executable')
		arguments = obtainTextList(doc, 'arguments', 'argument')

		outputPath = obtainText(doc, 'outputPath')
		outputFile = obtainText(doc, 'outputFile')

		errorPath = obtainText(doc, 'errorPath')
		inputPath = obtainText(doc, 'inputPath')

		inputSandbox = obtainText(doc, 'inputSandbox')
		outputSandbox = obtainText(doc, 'outputSandbox')

		workingDirectory = obtainText(doc, 'workingDirectory')

		requirements = obtainText(doc, 'requirements')

		inputFiles = obtainTextList(doc, 'inputFiles', 'inputFile')
		outputFiles = obtainTextList(doc, 'outputFiles', 'outputFile')

		jobName = obtainText(doc, 'jobName')
	
		nativeSpecification = obtainText(doc, 'nativeSpecification')


		#y ahora creamos un objeto nuevo con la informacion obtenida
		
		self.templateLocation = fileName
		
		self.gwID = -1
				
		self.taskInfo = TaskInfo(executable, outputPath, outputFile,
				 errorPath, inputPath,
				 inputSandbox, outputSandbox,
				 workingDirectory, requirements,
				 jobName, nativeSpecification)

		
		self.arguments = [Argument(argString)
						for argString in arguments]

			
		self.inputFiles = [InputFile(inputString)
						 for inputString in inputFiles]

		self.outputFiles = [OutputFile(outputString)
						for outputString in outputFiles]

		self.taskGroupID = taskGroup
		
	def getArguments(self):
		argumentList = []
		for arg in self.arguments:
			argumentList.append(arg.text)
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
	
			
	def inputFilesExist(self):
		for inputF in self.inputFiles:
			requiredFile = self.taskInfo.workingDirectory + "/" + inputF.text
			if  not os.path.exists(requiredFile):
				print (requiredFile + " is in Huelva")
				return False
		return True
	
			
	def outputFilesExist(self, showMissingFiles = False):
		for outputF in self.outputFiles:
			requiredFile = self.taskInfo.workingDirectory + "/" + outputF.text
			if  not os.path.exists(requiredFile):
				
				if showMissingFiles: 
					print (requiredFile + " is in Huelva")
				return False
		return True
		
	def showErrorMessage(self, errorMessage):
		print(" Error: " + errorMessage)
		print ("	task " + str (self.id))
		if self.gwID != None:
			print ("	gwID "  + self.gwID)
		if self.host != None:
			print ("	host = " + self.host.hostname)




		
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


def loadGridTasks(indexFile):
	gridTaskList = []
	for xmlFile in open(indexFile, 'r'):
		xmlFile = xmlFile.strip()
		auxTask = GridTask()
		auxTask.fromXML(xmlFile)
		gridTaskList.append(auxTask)
		
	return gridTaskList 
		

def dbDesign(metadata):
	return Table('gridTasks', metadata, 
		Column('id', Integer, primary_key=True),
		Column('templateLocation', String(512)),
		Column('gwID', String(256)),
		Column('hostID', Integer),
		Column('status', String(256)),
		Column('lastUpdated', TIMESTAMP, 
			   server_default=text('CURRENT_TIMESTAMP'),
			   server_onupdate=text('CURRENT_TIMESTAMP')),
		Column("creationDate", DateTime),
		Column("submissionDate", DateTime),
		Column("executionStartDate", DateTime),
		Column("endDate", DateTime),	
		Column("retryNumber", Integer), 
		Column("taskGroupID", Integer)	

		)		