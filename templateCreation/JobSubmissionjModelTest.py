'''
Created on Nov 19, 2012

QUEREMOS MANDAR UNAS 5.000 TAREAS DE PROTTEST, QUE SI SE MANDAN A LA VEZ
HACEN QUE SE SATURE EL SISTEMA DE COLAS Y CASCA. POR ESO AQUI LAS MANDAMOS
POCO A POCO, QUE NO HAYA MAS DE 1000 A LA VEZ

LA IDEA ES METER ESTE METODO EN EL CRONTAB Y QUE SE DESPIERTE UNA VEZ POR HORA


@author: u5682
'''

from datetime import datetime
import os, sys, pickle

import subprocess

from time import sleep


import xml.dom.minidom
from xml.dom.minidom import Node

from DRMAA import *
class GridTask(object):
	'''
	classdocs
	'''

	def __init__(self):
		'''
		Constructor
		'''
		self.gwID = "-1"
		self.status = "WAITING"
		self.hostID = -1		 
		self.creationDate = datetime.now()
		self.arguments = []
		self.inputFiles = []
		self.outputFiles = []
		self.taskInfo = ""
		self.executable = ""
		self.jobName = ""
		self.outputPath = ""
		self.inputPath = ""
		self.errorPath = ""
		
				
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
		
		
	def submit(self):
		
		(result, jt, error)=drmaa_allocate_job_template()

		if result != DRMAA_ERRNO_SUCCESS:
			print >> sys.stderr, "drmaa_allocate_job_template() failed: %s" % (error)
			sys.exit(-1)
	   
		(result, error)=drmaa_set_attribute(jt, DRMAA_WD, self.workingDirectory)
		if result != DRMAA_ERRNO_SUCCESS:
			print >> sys.stderr, "Error setting job template attribute: %s" % (error)
			sys.exit(-1)
		else:
			print ("	wordking directory: " + self.workingDirectory)
			
		   
		(result, error)=drmaa_set_attribute(jt, DRMAA_JOB_NAME, self.jobName)


		executable = self.executable
		
		if not (executable.startswith("/")):		
			print("	relative route for executable, considering that it is located at working directory")
			executable = "./" + executable

		(result, error)=drmaa_set_attribute(jt, DRMAA_REMOTE_COMMAND, executable)

		os.chmod(self.workingDirectory + "/" + self.executable,0777)
		
		(result, error)=drmaa_set_vector_attribute(jt, DRMAA_V_ARGV, self.getArguments())
	  
		if result != DRMAA_ERRNO_SUCCESS:
			print >> sys.stderr,"Error setting remote command arguments: %s" % (error)
			sys.exit(-1)
	 
	  
		if len(self.inputPath) > 0:
			print ("	input path: " + self.inputPath)
			(result, error)=drmaa_set_attribute(jt, DRMAA_INPUT_PATH, self.inputPath)
		
		if len(self.outputPath) > 0:
			print ("	outputPath path: " + self.outputPath)
			(result, error)=drmaa_set_attribute(jt, DRMAA_OUTPUT_PATH,self.outputPath)
		
		if len(self.errorPath) > 0:
			print ("	errorPath path: " + self.errorPath)
			(result, error)=drmaa_set_attribute(jt, DRMAA_ERROR_PATH,self.errorPath)
				
		
		if self.nativeSpecification != None:
			(result, error)=drmaa_set_attribute(jt, DRMAA_NATIVE_SPECIFICATION,self.nativeSpecification)
 
		(result, job_id, error)=drmaa_run_job(jt)
		
		if result != DRMAA_ERRNO_SUCCESS:
			print ("drmaa_run_job() failed: %s" % (error))
			sys.exit(-1)
		
		print ("Job successfully submited ID: %s" % (job_id))		
		
		
		
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
		

def readRunningTasks():
	submittedTasks = subprocess.check_output(["/opt/pbs/bin/qstat","-u u5682"])
	numberOfSubmittedTasks = len(submittedTasks.split("\n"))
	print ("tasks running or submitted: " + str(numberOfSubmittedTasks))
	return numberOfSubmittedTasks

if __name__ == '__main__':

	instancesOfProttest = [   
'/home/u5682/workspace/jModelTest2/test/guindon100_1/all_grid_tasks',
'/home/u5682/workspace/jModelTest2/test/example.phy_1/all_grid_tasks',
'/home/u5682/workspace/jModelTest2/test/guindon100_1/all_grid_tasks',
'/home/u5682/workspace/jModelTest2/test/guindon40_1/all_grid_tasks',
'/home/u5682/workspace/jModelTest2/test/HIV08.fasta_1/all_grid_tasks',
'/home/u5682/workspace/jModelTest2/test/HIVpol.groupM.nex_1/all_grid_tasks',
'/home/u5682/workspace/jModelTest2/test/primate-mtDNA.nex_1/all_grid_tasks',
'/home/u5682/workspace/jModelTest2/test/rokas.phy_1/all_grid_tasks',
'/home/u5682/workspace/jModelTest2/test/small.fas_1/all_grid_tasks',
'/home/u5682/workspace/jModelTest2/test/VertCOII.nex_1/all_grid_tasks',
'/home/u5682/workspace/jModelTest2/test/guindon100_2/all_grid_tasks',
'/home/u5682/workspace/jModelTest2/test/example.phy_2/all_grid_tasks',
'/home/u5682/workspace/jModelTest2/test/guindon100_2/all_grid_tasks',
'/home/u5682/workspace/jModelTest2/test/guindon40_2/all_grid_tasks',
'/home/u5682/workspace/jModelTest2/test/HIV08.fasta_2/all_grid_tasks',
'/home/u5682/workspace/jModelTest2/test/HIVpol.groupM.nex_2/all_grid_tasks',
'/home/u5682/workspace/jModelTest2/test/primate-mtDNA.nex_2/all_grid_tasks',
'/home/u5682/workspace/jModelTest2/test/rokas.phy_2/all_grid_tasks',
'/home/u5682/workspace/jModelTest2/test/small.fas_2/all_grid_tasks',
'/home/u5682/workspace/jModelTest2/test/VertCOII.nex_2/all_grid_tasks',
'/home/u5682/workspace/jModelTest2/test/guindon100_3/all_grid_tasks',
'/home/u5682/workspace/jModelTest2/test/example.phy_3/all_grid_tasks',
'/home/u5682/workspace/jModelTest2/test/guindon100_3/all_grid_tasks',
'/home/u5682/workspace/jModelTest2/test/guindon40_3/all_grid_tasks',
'/home/u5682/workspace/jModelTest2/test/HIV08.fasta_3/all_grid_tasks',
'/home/u5682/workspace/jModelTest2/test/HIVpol.groupM.nex_3/all_grid_tasks',
'/home/u5682/workspace/jModelTest2/test/primate-mtDNA.nex_3/all_grid_tasks',
'/home/u5682/workspace/jModelTest2/test/rokas.phy_3/all_grid_tasks',
'/home/u5682/workspace/jModelTest2/test/small.fas_3/all_grid_tasks',
'/home/u5682/workspace/jModelTest2/test/VertCOII.nex_3/all_grid_tasks',
'/home/u5682/workspace/jModelTest2/test/guindon100_4/all_grid_tasks',
'/home/u5682/workspace/jModelTest2/test/example.phy_4/all_grid_tasks',
'/home/u5682/workspace/jModelTest2/test/guindon100_4/all_grid_tasks',
'/home/u5682/workspace/jModelTest2/test/guindon40_4/all_grid_tasks',
'/home/u5682/workspace/jModelTest2/test/HIV08.fasta_4/all_grid_tasks',
'/home/u5682/workspace/jModelTest2/test/HIVpol.groupM.nex_4/all_grid_tasks',
'/home/u5682/workspace/jModelTest2/test/primate-mtDNA.nex_4/all_grid_tasks',
'/home/u5682/workspace/jModelTest2/test/rokas.phy_4/all_grid_tasks',
'/home/u5682/workspace/jModelTest2/test/small.fas_4/all_grid_tasks',
'/home/u5682/workspace/jModelTest2/test/VertCOII.nex_4/all_grid_tasks',
'/home/u5682/workspace/jModelTest2/test/guindon100_5/all_grid_tasks',
'/home/u5682/workspace/jModelTest2/test/example.phy_5/all_grid_tasks',
'/home/u5682/workspace/jModelTest2/test/guindon100_5/all_grid_tasks',
'/home/u5682/workspace/jModelTest2/test/guindon40_5/all_grid_tasks',
'/home/u5682/workspace/jModelTest2/test/HIV08.fasta_5/all_grid_tasks',
'/home/u5682/workspace/jModelTest2/test/HIVpol.groupM.nex_5/all_grid_tasks',
'/home/u5682/workspace/jModelTest2/test/primate-mtDNA.nex_5/all_grid_tasks',
'/home/u5682/workspace/jModelTest2/test/rokas.phy_5/all_grid_tasks',
'/home/u5682/workspace/jModelTest2/test/small.fas_5/all_grid_tasks',
'/home/u5682/workspace/jModelTest2/test/VertCOII.nex_5/all_grid_tasks',
'/home/u5682/workspace/jModelTest2/test/guindon100_6/all_grid_tasks',
'/home/u5682/workspace/jModelTest2/test/example.phy_6/all_grid_tasks',
'/home/u5682/workspace/jModelTest2/test/guindon100_6/all_grid_tasks',
'/home/u5682/workspace/jModelTest2/test/guindon40_6/all_grid_tasks',
'/home/u5682/workspace/jModelTest2/test/HIV08.fasta_6/all_grid_tasks',
'/home/u5682/workspace/jModelTest2/test/HIVpol.groupM.nex_6/all_grid_tasks',
'/home/u5682/workspace/jModelTest2/test/primate-mtDNA.nex_6/all_grid_tasks',
'/home/u5682/workspace/jModelTest2/test/rokas.phy_6/all_grid_tasks',
'/home/u5682/workspace/jModelTest2/test/small.fas_6/all_grid_tasks',
'/home/u5682/workspace/jModelTest2/test/VertCOII.nex_6/all_grid_tasks',
'/home/u5682/workspace/jModelTest2/test/guindon100_7/all_grid_tasks',
'/home/u5682/workspace/jModelTest2/test/example.phy_7/all_grid_tasks',
'/home/u5682/workspace/jModelTest2/test/guindon100_7/all_grid_tasks',
'/home/u5682/workspace/jModelTest2/test/guindon40_7/all_grid_tasks',
'/home/u5682/workspace/jModelTest2/test/HIV08.fasta_7/all_grid_tasks',
'/home/u5682/workspace/jModelTest2/test/HIVpol.groupM.nex_7/all_grid_tasks',
'/home/u5682/workspace/jModelTest2/test/primate-mtDNA.nex_7/all_grid_tasks',
'/home/u5682/workspace/jModelTest2/test/rokas.phy_7/all_grid_tasks',
'/home/u5682/workspace/jModelTest2/test/small.fas_7/all_grid_tasks',
'/home/u5682/workspace/jModelTest2/test/VertCOII.nex_7/all_grid_tasks',
'/home/u5682/workspace/jModelTest2/test/guindon100_8/all_grid_tasks',
'/home/u5682/workspace/jModelTest2/test/example.phy_8/all_grid_tasks',
'/home/u5682/workspace/jModelTest2/test/guindon100_8/all_grid_tasks',
'/home/u5682/workspace/jModelTest2/test/guindon40_8/all_grid_tasks',
'/home/u5682/workspace/jModelTest2/test/HIV08.fasta_8/all_grid_tasks',
'/home/u5682/workspace/jModelTest2/test/HIVpol.groupM.nex_8/all_grid_tasks',
'/home/u5682/workspace/jModelTest2/test/primate-mtDNA.nex_8/all_grid_tasks',
'/home/u5682/workspace/jModelTest2/test/rokas.phy_8/all_grid_tasks',
'/home/u5682/workspace/jModelTest2/test/small.fas_8/all_grid_tasks',
'/home/u5682/workspace/jModelTest2/test/VertCOII.nex_8/all_grid_tasks',
'/home/u5682/workspace/jModelTest2/test/guindon100_9/all_grid_tasks',
'/home/u5682/workspace/jModelTest2/test/example.phy_9/all_grid_tasks',
'/home/u5682/workspace/jModelTest2/test/guindon100_9/all_grid_tasks',
'/home/u5682/workspace/jModelTest2/test/guindon40_9/all_grid_tasks',
'/home/u5682/workspace/jModelTest2/test/HIV08.fasta_9/all_grid_tasks',
'/home/u5682/workspace/jModelTest2/test/HIVpol.groupM.nex_9/all_grid_tasks',
'/home/u5682/workspace/jModelTest2/test/primate-mtDNA.nex_9/all_grid_tasks',
'/home/u5682/workspace/jModelTest2/test/rokas.phy_9/all_grid_tasks',
'/home/u5682/workspace/jModelTest2/test/small.fas_9/all_grid_tasks',
'/home/u5682/workspace/jModelTest2/test/VertCOII.nex_9/all_grid_tasks',
'/home/u5682/workspace/jModelTest2/test/guindon100_0/all_grid_tasks',
'/home/u5682/workspace/jModelTest2/test/example.phy_0/all_grid_tasks',
'/home/u5682/workspace/jModelTest2/test/guindon100_0/all_grid_tasks',
'/home/u5682/workspace/jModelTest2/test/guindon40_0/all_grid_tasks',
'/home/u5682/workspace/jModelTest2/test/HIV08.fasta_0/all_grid_tasks',
'/home/u5682/workspace/jModelTest2/test/HIVpol.groupM.nex_0/all_grid_tasks',
'/home/u5682/workspace/jModelTest2/test/primate-mtDNA.nex_0/all_grid_tasks',
'/home/u5682/workspace/jModelTest2/test/rokas.phy_0/all_grid_tasks',
'/home/u5682/workspace/jModelTest2/test/small.fas_0/all_grid_tasks',
'/home/u5682/workspace/jModelTest2/test/VertCOII.nex_0/all_grid_tasks']


	instancetoSubmit = 0
	
	pickleLastsubmittedTask = 'numberOfSubmittedTasks'
	
	if os.path.exists(pickleLastsubmittedTask):
		myFile = open(pickleLastsubmittedTask, "rb")
		instancetoSubmit = pickle.load(myFile)
		print("Last submitted instance:" + str(instancetoSubmit))
		

	submittedTasks =  subprocess.check_output(["/opt/pbs/bin/qstat","-u u5682"])

	numberOfSubmittedTasks = len(submittedTasks.split("\n"))-1
	
	while instancetoSubmit < len (instancesOfProttest):
	
		while numberOfSubmittedTasks < 300:
			
			taskList=[]
			#read file with the task info
			for xmlFile in open(instancesOfProttest[instancetoSubmit], 'r'):
				xmlFile = xmlFile.strip()
				auxTask = GridTask()
				auxTask.fromXML(xmlFile)
				taskList.append(auxTask)
			
		
			(result, error)=drmaa_init(None)
		
			if result != DRMAA_ERRNO_SUCCESS:
				print >> sys.stderr, "drmaa_init() failed: %s" % (error)
				sys.exit(-1)
			else:
				print "drmaa_init() success"
		
			#submit tasks	  
			for task in taskList:
				task.submit()
			
			(result, error)=drmaa_exit()
		
			if result != DRMAA_ERRNO_SUCCESS:
				print >> sys.stderr, "drmaa_exit() failed: %s" % (error)
				sys.exit(-1)
			else:
				print ("drmaa_exit() success")
	
	
			#store information about the submitted instance
			instancetoSubmit+=1
			fileName = open(pickleLastsubmittedTask, 'wb')
			pickle.dump(instancetoSubmit, fileName)
			fileName.close()
				
				
			#update task info
			sleep(10) #this is necesary so the qstat call returns a valid result
			numberOfSubmittedTasks =  readRunningTasks()
			
		print("Let's have a one minute nap")
		sleep (60)
		numberOfSubmittedTasks =  readRunningTasks()
