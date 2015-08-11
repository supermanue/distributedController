'''
Created on Feb 22, 2013

@author: u5682
'''

import os, sys, pickle
from time import sleep
from PbsTask import PBSTask
from DistributedTask import DistributedTask
import ShellExecution

class Controller(object):
	
	def __init__(self):
		self.instancetoSubmit = 0
		self.pickleLastsubmittedTask = '/home/u5682/workspace/distributedToolbox/clusterController/numberOfSubmittedTasks'
		
		if os.path.exists(self.pickleLastsubmittedTask):
			myFile = open(self.pickleLastsubmittedTask, "rb")
			self.instancetoSubmit = pickle.load(myFile)


	def	increaseInstanceToSubmit(self):
		self.instancetoSubmit+=1
		fileName = open(self.pickleLastsubmittedTask, 'wb')
		pickle.dump(self.instancetoSubmit, fileName)
		fileName.close()
	
	
	
	
	def numberOfRunningTasks(self):
		
		userName = os.getenv('USER')
		
		commandToExecute = "/opt/pbs/bin/qstat -n1 -u " + userName + " | wc -l"
		runningTasks = int(ShellExecution.execute(commandToExecute).strip()) -6 #6 = header and stuff
		
		print ("Running tasks: " + str(runningTasks))
		
		return runningTasks 
		
	
	
	def parseTaskGroup(self, taskGroupLocation):
		
		taskList = []
		for xmlFile in open(taskGroupLocation, 'r'):
			myTask = DistributedTask(xmlFile.strip())
			myPBSTask = PBSTask(myTask)
			taskList.append(myPBSTask)
		return taskList


if __name__ == '__main__':
	
	
	maxQueuedTasks=200
	
	print ("WELCOME TO PBS SUBMITER")
	print ("Number of max queued tasks: " + str(maxQueuedTasks))

	if len(sys.argv)!=2:
		print ("USAGE: pbsMultipleTasks <fileWithTaskGroups>")
		sys.exit()
	
	taskIDsFile = open(sys.argv[1], 'r')
	taskIDs = taskIDsFile.readlines()
	
	
	myController = Controller()
	print("Last submitted instance:" + str(myController.instancetoSubmit))


	while myController.instancetoSubmit < len (taskIDs):
	
		while myController.numberOfRunningTasks() < maxQueuedTasks:
			
			task = taskIDs[myController.instancetoSubmit].strip()
			taskList = myController.parseTaskGroup(task)
			
			print ("Submitting task group number " + str(myController.instancetoSubmit))
			for task in taskList:
				task.submit()
				sys.exit()
			#store information about the submitted instance
			myController.increaseInstanceToSubmit()
							
			#update task info
			sleep(10) #this is necesary so the qstat call returns a valid result
			
		print("Let's have a one minute nap")
		sleep (60)