'''
Created on Feb 22, 2013

@author: u5682
'''

import os, sys


from DRMAA import *

from DistributedTask import DistributedTask

class DRMAAClass(object):
	'''
	classdocs
	'''

	def __init__(self, distributedTask):
		'''
		Constructor
		'''
	
		self.task = distributedTask
	
	
	
	
	
	def submit(self):
		
		(result, jt, error)=drmaa_allocate_job_template()

		if result != DRMAA_ERRNO_SUCCESS:
			print >> sys.stderr, "drmaa_allocate_job_template() failed: %s" % (error)
			sys.exit(-1)
	   
		(result, error)=drmaa_set_attribute(jt, DRMAA_WD, self.task.workingDirectory)
		if result != DRMAA_ERRNO_SUCCESS:
			print >> sys.stderr, "Error setting job template attribute: %s" % (error)
			sys.exit(-1)
		else:
			print ("	wordking directory: " + self.task.workingDirectory)
			
		   
		(result, error)=drmaa_set_attribute(jt, DRMAA_JOB_NAME, self.task.jobName)


		executable = self.task.executable
		
		if not (executable.startswith("/")):		
			print("	relative route for executable, considering that it is located at working directory")
			executable = "./" + executable

		(result, error)=drmaa_set_attribute(jt, DRMAA_REMOTE_COMMAND, executable)

		os.chmod(self.task.workingDirectory + "/" + self.task.executable,0777)
		
		(result, error)=drmaa_set_vector_attribute(jt, DRMAA_V_ARGV, self.task.getArguments())
	  
		if result != DRMAA_ERRNO_SUCCESS:
			print >> sys.stderr,"Error setting remote command arguments: %s" % (error)
			sys.exit(-1)
	 
	  
		if len(self.task.inputPath) > 0:
			print ("	input path: " + self.task.inputPath)
			(result, error)=drmaa_set_attribute(jt, DRMAA_INPUT_PATH, self.task.inputPath)
		
		if len(self.task.outputPath) > 0:
			print ("	outputPath path: " + self.task.outputPath)
			(result, error)=drmaa_set_attribute(jt, DRMAA_OUTPUT_PATH,self.task.outputPath)
		
		if len(self.task.errorPath) > 0:
			print ("	errorPath path: " + self.task.errorPath)
			(result, error)=drmaa_set_attribute(jt, DRMAA_ERROR_PATH,self.task.errorPath)
				
		
		if self.task.nativeSpecification != None:
			(result, error)=drmaa_set_attribute(jt, DRMAA_NATIVE_SPECIFICATION,self.task.nativeSpecification)
 
		(result, job_id, error)=drmaa_run_job(jt)
		
		if result != DRMAA_ERRNO_SUCCESS:
			print ("drmaa_run_job() failed: %s" % (error))
			sys.exit(-1)
		
		print ("Job successfully submited ID: %s" % (job_id))		
		
		