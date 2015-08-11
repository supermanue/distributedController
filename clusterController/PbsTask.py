'''
Created on Feb 22, 2013

@author: u5682
'''


from DistributedTask import DistributedTask
import ShellExecution
import os

class PBSTask(object):
	'''
	classdocs
	'''


	def __init__(self, distributedTask):
		'''
		Constructor
		'''
	
		self.task = distributedTask
		
		
		

	def submit(self):
		
		arguments = ' '.join(self.task.arguments)
		
		currentDir = os.getcwd()
		os.chdir(self.task.workingDirectory)
		commandToExecute = "/opt/pbs/bin/qsub -l walltime=23:59:00 -v "  +\
			"working_directory=" + self.task.workingDirectory + \
			",executable="+ self.task.executable +\
			",arguments=\"'"+arguments+"'\" " + \
			currentDir + "/clusterController/clusterControllerScript.sh"
		
		
		print ("Submitting task to PBS")
		output = ShellExecution.execute(commandToExecute)
		#print ("	" + self.task.workingDirectory + "/" + self.task.executable + " " + arguments)
		#print ("	" + output)
		
		os.chdir(currentDir)
		