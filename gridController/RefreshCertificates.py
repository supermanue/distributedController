'''
Created on Jan 11, 2013

@author: u5682
'''

import Host, InputFile, OutputFile, TaskInfo, Argument, GridTask, TaskGroup

from sqlalchemy import *
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

import subprocess as sub
from datetime import datetime, timedelta



def runProcess(command):	
	# Start subprocess
	print ("Executing command: " + command)
	p = sub.Popen(command + ' 2>&1', shell = True, stdout=sub.PIPE)
	# Wait for it to finish
	p.wait()
	# Get output
	res = p.communicate()[0]

	# If error, raise exception
	if p.returncode:
		raise 'Error in "{0}". Exit code: {1}. Output: {2}'

	# Else, return output
	return res

def initializeDB(metadata, engine):

	taskInfos = TaskInfo.dbDesign(metadata)	  
	inputFiles = InputFile.dbDesign(metadata)	   
	outputFiles = OutputFile.dbDesign(metadata)	  
	arguments = Argument.dbDesign(metadata)	
	gridTasks = GridTask.dbDesign(metadata)	 
	hosts = Host.dbDesign(metadata)	
	taskGroups = TaskGroup.dbDesign(metadata)
		
	metadata.create_all(engine)
	
def processGWHosts():
	runProcess("gwhost -f  > "+ gwhostLocation)
	fileToRead = open(gwhostLocation, 'r')
	
	hosts=[]
	for line in fileToRead.readlines():
		if line.count("HOSTNAME") >0:
			hostname = line.split("=")[1].strip()
			hosts.append(hostname)
			continue
	return hosts
	
	
if __name__ == '__main__':
	
	gwhostLocation = "/tmp/gwHosts"
	engine = create_engine('mysql://root:monteraPass2013@localhost/DistributedController', echo=False)
	mySessionClass = sessionmaker(bind=engine)
	mySession = mySessionClass()
	metadata = MetaData()
	
	initializeDB(metadata, engine)



	print ("OBTAINING AVAILABLE HOSTS")
	

	gwHosts = processGWHosts()

	employedHosts = mySession.query(Host.Host)
	print ("UPDATING CERTIFICATE IN REMOTE HOSTS")
	
	hostList=[]
	for gwHost in gwHosts:

		
		hasBeenUsed = False
		for host in employedHosts:
			if gwHost.find(host.hostname)>=0:
				hasBeenUsed= True
				break
		
		if not hasBeenUsed:
			continue

		
		lastTask = mySession.query(GridTask.GridTask).filter(GridTask.GridTask.hostID==host.id).order_by('-id').first()
		
		if lastTask == None:
			continue
	
	#	timeSinceLastSubmission = datetime.now()-lastTask.submissionDate
	#	timeLimit = timedelta(days=7)
		
	#	if timeSinceLastSubmission > timeLimit:
	#		continue
		
		print ("-----")
		print ("Host: " + gwHost)
		print ("	host found in past executions")
			
		print ("	last submission: " + str(lastTask.id) + ": " + str(lastTask.creationDate))
		command = "glite-ce-proxy-renew -e " + gwHost + " GridWay"
		print ("	" + command)
		
		
		try:
			result = runProcess(command)
			print (result)
			print ("	parece que ruló")
			hostList.append(gwHost)
		except:
			print ("parece que falló")

	print ("")
	print("RENEWED CERTIFICATES")
	for host in hostList:
		print (host)
