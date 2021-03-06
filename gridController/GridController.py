'''
Created on Aug 22, 2012

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

from DRMAA import *
import sys, os, time
from datetime import datetime, timedelta
from time import sleep
import math
import subprocess as sub

import Host, InputFile, OutputFile, TaskInfo, Argument, GridTask, TaskGroup

from sqlalchemy import *
from sqlalchemy.orm import sessionmaker
from sqlalchemy import desc
import base
import threading

class GridWayController(object):
	'''
	classdocs
	'''

	def __init__(self, sequentialExecution = False):
		'''
		Constructor
		'''
		self.gridTasks = []
		self.hostList = []
		self.gwpsFileLocation = "/tmp/gwpsOutput"
		self.timeBetweenIterations = 60 #seconds
		self.maxQueueTime = 7200

		self.replicaFraction = 10 #percentage of tasks to replicate (this is 5%, for example)
		self.maxAllowedTasksToSubmit = 100

		self.bannedHostLimit = 5 #if more than 5 hosts are included, DRMAA tends to crash

		self.sequentialExecution = sequentialExecution

	def initGridSession(self):
		#=======================================================================
		# print("-->DRMAA CALL: init <---")
		#=======================================================================
		(result, error)=drmaa_init(None)
		if result == DRMAA_ERRNO_ALREADY_ACTIVE_SESSION:
			print "drmaa_init(): sesion was already intialized"
		elif result != DRMAA_ERRNO_SUCCESS :
			print "drmaa_init() failed: "+error
			return -1
		else:
			print "drmaa_init() success"
			return 0

	def exitGridSession(self):
		#=======================================================================
		# print("-->DRMAA CALL: exit <---")
		#=======================================================================

		(result, error)=drmaa_exit()
		if result == DRMAA_ERRNO_NO_ACTIVE_SESSION:
			print "drmaa_exit(): there was no active session "

		elif result != DRMAA_ERRNO_SUCCESS:
			print "drmaa_exit() failed: "+error
			sys.exit(-1)
		else:
			print "drmaa_exit() success"



	def obtainTaskHost(self, dbSession, gwTaskID):
		hostname = Host.readHost(self.gwpsFileLocation, gwTaskID)

		auxHost = dbSession.query(Host.Host).filter(Host.Host.hostname == hostname).first()

		if (auxHost == None):
			print("new host employed! " + hostname)
			auxHost = Host.Host(hostname)
			dbSession.add(auxHost)
			dbSession.commit()

		return auxHost



	def obtainGridWayStateDRMAA(self, myGridTask):
		(result, remote_ps, error)=drmaa_job_ps(myGridTask.gwID)

		if result != DRMAA_ERRNO_SUCCESS:
			print "obtainGridWayState() failed: "+error
			return DRMAA_PS_UNDETERMINED
		else:
			return remote_ps


	def obtainGridWayState(self, myGridTask):
		gwID = myGridTask.gwID

		foundTask = False
		job_state = "ERROR"
		em_state = "----"
		fileToRead = open(self.gwpsFileLocation, 'r')
		for line in fileToRead.readlines():
			if line.count("JOB_ID") > 0:
				if line.count(gwID) > 0:
					foundTask = True
					continue

			if foundTask and line.count("JOB_STATE") >0:
				job_state = line.split("=")[1].strip()
				continue

			if foundTask and line.count("EM_STATE") >0:
				em_state = line.split("=")[1].strip()
				break;

		fileToRead.close()
		if not foundTask:
			return DRMAA_PS_UNDETERMINED

		#ahora paso del status en modo "texto" al oficial de GW
		if job_state =="pend":
			return DRMAA_PS_UNDETERMINED

		elif job_state =="prew" or job_state=="wrap":

			if em_state == "actv" or em_state=="fail" or em_state=="done":
				return DRMAA_PS_RUNNING
			else:
				return DRMAA_PS_QUEUED_ACTIVE

		elif job_state =="epil":
			return DRMAA_PS_RUNNING

		elif job_state =="fail":
			return DRMAA_PS_FAILED

		elif job_state =="done":
			return DRMAA_PS_DONE

		else:
			return DRMAA_PS_UNDETERMINED




	def borraTarea(self, myGridTask):
		gwID = myGridTask.gwID

		#=======================================================================
		# print("-->DRMAA CALL: wait <---")
		#=======================================================================

		(result, job_id_out, stat, rusage, error)=drmaa_wait(gwID, DRMAA_TIMEOUT_NO_WAIT)
		#=======================================================================
		#print ("desactivado el borrado de tarea para facilitar el debug")
		#result=DRMAA_ERRNO_SUCCESS #hay que borrar esta linea y descomentar la anterior
		#=======================================================================

		#=======================================================================
		print ("	borraTarea: Deleting task " + gwID)
		#=======================================================================

		if result != DRMAA_ERRNO_SUCCESS:
			#print ("ERROR WHEN OBTAINING GW STATUS FROM TASK " + str(myGridTask.id) +" with GridWay ID " + gwID + ". Doing it the hard way")
			#sys.exit(-1)


			#myGridTask.status="DELETING"

			#===================================================================
			print("         borraTarea: could not delete task " + str(myGridTask.id) + " with gwID " + gwID)
			#===================================================================


			#===================================================================
			# (result, error)=drmaa_control(gwID, DRMAA_CONTROL_TERMINATE)
			# if result != DRMAA_ERRNO_SUCCESS:
			#	print("ERROR, when deleting task " + str(myGridTask.id) + " with gwID " + gwID + ". Maybe not present on system")
			# else:
			#	print("task deleted")
			#===================================================================
			#===================================================================
			# token = drmaa_control(gwID, DRMAA_CONTROL_TERMINATE)
			#===================================================================

			#===================================================================
			# print("Trying to hard-delete task "+ str(myGridTask.id) + " with gwID " + gwID + " from site: " + myGridTask.host.hostname)
			# self.runProcessUnnatended("nohup gwkill " + gwID + " &")
			#===================================================================
			return False
		else:
			#===================================================================
			print("        borraTarea: DELETED task " + str(myGridTask.id) + " with gwID " + gwID)
			#===================================================================

			return True

	def createJobTemplate(self, myGridTask, bannedHosts):

		(result, jt, error)=drmaa_allocate_job_template()

		if result != DRMAA_ERRNO_SUCCESS:
			print >> sys.stderr, "drmaa_allocate_job_template() failed: %s" % (error)
			sys.exit(-1)

		workingDirectory = myGridTask.taskInfo.workingDirectory

		(result, error)=drmaa_set_attribute(jt, DRMAA_WD, workingDirectory)
		if result != DRMAA_ERRNO_SUCCESS:
			print >> sys.stderr, "Error setting job template attribute: %s" % (error)
			sys.exit(-1)


		(result, error)=drmaa_set_attribute(jt, DRMAA_JOB_NAME, myGridTask.taskInfo.jobName)

		(result, error)=drmaa_set_attribute(jt, DRMAA_REMOTE_COMMAND, myGridTask.taskInfo.executable)

		(result, error)=drmaa_set_vector_attribute(jt, DRMAA_V_ARGV, myGridTask.getArguments())

		if result != DRMAA_ERRNO_SUCCESS:
			print >> sys.stderr,"Error setting remote command arguments: %s" % (error)
			sys.exit(-1)


 		(result, error)=drmaa_set_attribute(jt, DRMAA_OUTPUT_PATH, myGridTask.taskInfo.outputPath)
 		(result, error)=drmaa_set_attribute(jt, DRMAA_ERROR_PATH,myGridTask.taskInfo.errorPath)
 		(result, error)=drmaa_set_attribute(jt, DRMAA_INPUT_PATH,myGridTask.taskInfo.inputPath)

 		(result, error)=drmaa_set_vector_attribute(jt, DRMAA_V_GW_INPUT_FILES, myGridTask.getInputFiles())
 		(result, error)=drmaa_set_vector_attribute(jt, DRMAA_V_GW_OUTPUT_FILES, myGridTask.getOutputFiles())


		######3REQUIREMENTS FOR BANNED HOSTS

		defTaskRequirements = myGridTask.taskInfo.requirements
		for bannedHost in bannedHosts:
			if defTaskRequirements == "":
				defTaskRequirements += "!(HOSTNAME=\"*" + bannedHost.hostname + "\")"
			else:
				defTaskRequirements += "& !(HOSTNAME=\"*" + bannedHost.hostname + "\")"
		#=======================================================================
		# if myGridTask.taskInfo.requirements != "":
		#	defTaskRequirements += "& (" +  myGridTask.taskInfo.requirements + ")"
		#
		#=======================================================================
		if defTaskRequirements != None:
			#===================================================================
			# print("Requirements: " + defTaskRequirements)
			#===================================================================
			(result, error)=drmaa_set_attribute(jt, DRMAA_GW_REQUIREMENTS,defTaskRequirements)



		if myGridTask.taskInfo.nativeSpecification != None:
			(result, error)=drmaa_set_attribute(jt, DRMAA_NATIVE_SPECIFICATION,myGridTask.taskInfo.nativeSpecification)

		(result, error)=drmaa_set_attribute(jt, DRMAA_GW_SUSPENSION_TIMEOUT ,str(7200))

		return jt



	def submitTaskToTheGrid(self, myGridTask, bannedHosts):

		if not myGridTask.inputFilesExist():
			print ("Task ID: " + str(myGridTask.id))
			print ("	problematic execution: input files do not exist")
			print ("	Submission will be cancelled and task erased")
			myGridTask.status="VENTILATED"
			return

		jt=self.createJobTemplate(myGridTask, bannedHosts)

		#=======================================================================
		# print("-->DRMAA CALL: run job <---")
		#=======================================================================

		(result, job_id, error)=drmaa_run_job(jt)

		if result != DRMAA_ERRNO_SUCCESS:
			print ("drmaa_run_job() failed: %s" % (error))
			return
			sys.exit(-1)

		print("task ID: " + str(myGridTask.id))
		print("	Successfully submited task")
		print("	group: " + str(myGridTask.taskGroupID))
		print("	gridway ID: %s" % (job_id))

		myGridTask.gwID = job_id
		myGridTask.status = "SUBMITTED"
		myGridTask.hostID = -1
		myGridTask.submissionDate = datetime.now()
		myGridTask.retryNumber +=1


		stdoutFile=os.environ['GW_LOCATION'] +  "/var/" + myGridTask.gwID + "/stdout.wrapper.0"
		f = open(stdoutFile, "w")
		f.write("EXIT_STATUS=0")
		f.close()
		os.chmod(stdoutFile, 0777)


	def initializeDB(self, metadata, engine):

		taskInfos = TaskInfo.dbDesign(metadata)
		inputFiles = InputFile.dbDesign(metadata)
		outputFiles = OutputFile.dbDesign(metadata)
		arguments = Argument.dbDesign(metadata)
		gridTasks = GridTask.dbDesign(metadata)
		hosts = Host.dbDesign(metadata)
		taskGroups = TaskGroup.dbDesign(metadata)

		metadata.create_all(engine)


	def runProcess(self,command):
		# Start subprocess
		print ("Executing command: " + command)
		p = sub.Popen(command + ' 2>&1', shell = True, stdout=sub.PIPE)
		# Wait for it to finish
		p.wait()
		# Get output
		res = p.communicate()[0]

		# If error, raise exception
		if p.returncode:
			raise ('Error in when executing' + command)

		# Else, return output
		return res

	def runProcessUnnatended(self,command):
		# Start subprocess
		print ("Executing command: " + command)
		p = sub.Popen(command + ' 2>&1', shell = True, stdout=sub.PIPE)
		# Wait for it to finish



	#if all tasks have been executed and processed, the execution is over
	def endExecution(self, dbSession):
		test = 80000
		allTasks = dbSession.query(func.count(GridTask.GridTask)).filter(GridTask.GridTask.status !="DELETING",GridTask.GridTask.status !="FAILED").scalar()
		clearedTasks = dbSession.query(func.count(GridTask.GridTask)).filter(GridTask.GridTask.status =="VENTILATED").scalar()

		if clearedTasks == allTasks:
			return True
		else:
			return False


	#this method checks whether it is neccesary to replicate a task.
	#if true, it creates the replica.

	 #esto sirve para evitar que en algun host problematico haya tareas que figuren como ejecutandose pero sea un error.
	#esto pasa en un numero pequeno de casos pero difuclta enormemente el trabajo. La solucion es replicar la tarea
	#y que se ejecute en otro sieito
	#tambien sirve por si alguna tarea ha caido en un host muy lento y esta haciendo de cuello de botella

	#la solucion es replicar el 10% de las tarea de cada grupo que mas estan tardando en acabar

	#como mandar una duplicada:
	#para hacer eso basta con ponerlas como WAITING. Esto hace que le den un nuevo ID, se envie y tal.
	#como la otra sigue dentro de gridway, si acaba su ejecucion correctamente tendremos los archivos de salida deseados,
	#con lo que en el paso anterior (punto 1) se detectara y marcara como acabada.

	#PROBLEMA: esto deja una de las dos tareas por el grid sin cancela, creando un pequeno overhead. Es un problema pero es la solucion facil hehehe
	def replicaControl(self, dbSession):

		#get all task groups in execution

		#=======================================================================
		# for elems in dbSession.query(TaskGroup.TaskGroup, func.count(GridTask.GridTask)).filter(GridTask.GridTask.taskGroupID ==TaskGroup.TaskGroup.id, GridTask.GridTask.status!="WAITING",  GridTask.GridTask.status!="SUBMITTED"):
		#	group = elems[0]
		#	number = elems[1]
		#	print ("Group " + str (group.id) + ", pending tasks" + str(number))
		#=======================================================================

		#=======================================================================
		# for group, pendingTasks in dbSession.query(TaskGroup.TaskGroup,func.count(GridTask.GridTask.id)).\
		#			join(GridTask.GridTask, GridTask.GridTask.taskGroupID ==TaskGroup.TaskGroup.id).\
		#			filter(TaskGroup.TaskGroup.finished==False, TaskGroup.TaskGroup.replicas ==0,
		#			or_((GridTask.GridTask.status=="WAITING"),  (GridTask.GridTask.status=="SUBMITTED"))).\
		#			group_by(GridTask.GridTask.taskGroupID):
		#=======================================================================


		for group in dbSession.query(TaskGroup.TaskGroup).\
				filter(TaskGroup.TaskGroup.finished==False, TaskGroup.TaskGroup.replicas ==0):

			pendingTasks = dbSession.query(func.count(GridTask.GridTask.id)).\
							filter(GridTask.GridTask.taskGroupID == group.id, or_(GridTask.GridTask.status=="WAITING",GridTask.GridTask.status=="SUBMITTED")).scalar()


			#===================================================================
			# print ("Group " + str (group.id) + ", pending tasks " + str(pendingTasks))
			#===================================================================

		#=======================================================================
		#
		# for pendingTasks in dbSession.query(func.count(GridTask.GridTask.id)).\
		#					filter(GridTask.GridTask.taskGroupID == group.id, GridTask.GridTask.status=="WAITING"):
		#	print "a pending task"
		#=======================================================================


		#=======================================================================
		# for group in dbSession.query(TaskGroup.TaskGroup):
		#	if group.finished == True:
		#		continue
		#	if group.replicas > 0:
		#		continue
		#
		#=======================================================================
			if pendingTasks > 0:
				continue
			groupSize = dbSession.query(func.count(GridTask.GridTask)).filter(GridTask.GridTask.taskGroupID ==group.id).scalar()

			#TODO: esto es una chapuza. Esta situacion no se tendri que dar nunca, es un parche por si se inicializo mal la db o algo
			if groupSize ==0:
				continue
			#===================================================================
			# print ("deep analysis of group " + str(group.id))
			#===================================================================

			activeTasksInGroup = dbSession.query(GridTask.GridTask).filter((GridTask.GridTask.taskGroupID ==group.id), or_((GridTask.GridTask.status=="RUNNING"), (GridTask.GridTask.status=="QUEUED")))
			activeTasksInGroupSize = activeTasksInGroup.count()

			#===================================================================
			# print ("recplica fraction: " + str(math.ceil(activeTasksInGroupSize * 100 )/groupSize))
			#===================================================================

			if (math.ceil(activeTasksInGroupSize * 100 )/groupSize) < self.replicaFraction :
				#now we need to replicate the tasks
				#to do that, as it is been said, we only need to set its status to
				print ("REPLICA CONTROL: replication in group " + str(group.id))
				print("Active tasks, fraction = " + str(activeTasksInGroupSize) + "," + str(math.ceil(activeTasksInGroupSize * 100 )/groupSize))

				for gridTask in activeTasksInGroup:

					gridTaskReplica = GridTask.GridTask()
					gridTaskReplica.fromXML(group.id, gridTask.templateLocation)

					gridTaskReplica.taskInfo.requirements=("!(hostname=\"*" + gridTask.host.hostname + "\")")

					group.gridTasks.append(gridTaskReplica)
					self.gridTasks.append(gridTaskReplica)

					dbSession.add(gridTaskReplica)
					dbSession.commit()
					print ("Replicating task: " + str(gridTask.id) + " with gw_id = " + gridTask.gwID + "with requirements: " + gridTaskReplica.taskInfo.requirements)
				group.replicas +=1
				dbSession.add(group)
				dbSession.commit()


#return true if the execution was successful, false otherwise
	def updateTerminationStatus(self, gridTask, gwStatus):

		if gridTask.outputFilesExist():
			gridTask.endDate = datetime.now()
			print("SUCCESFUL EXECUTION of task " + str (gridTask.id) + " with gwID "  + gridTask.gwID)
			gridTask.host.registerSuccesfulExecution()

			if self.borraTarea(gridTask):
					gridTask.status ="VENTILATED"
			else:
					gridTask.status = "DELETING"


			return True
		else:
			gridTask.status = "WAITING"

			if gwStatus == DRMAA_PS_DONE:
				gridTask.showErrorMessage("Problematic execution, output files not found")
				if gridTask.host != None:
					gridTask.outputFilesExist(showMissingFiles = True)
					gridTask.host.registerProblematicExecution(datetime.now())

			elif gwStatus == DRMAA_PS_UNDETERMINED:
				gridTask.showErrorMessage("Problematic execution, task disapeared ")
				if gridTask.host != None:
					gridTask.outputFilesExist(showMissingFiles = True)
					gridTask.host.registerProblematicExecution(datetime.now())

			else:
				gridTask.showErrorMessage("Failed execution")
				if gridTask.host != None:
					gridTask.host.registerFailedExecution(datetime.now())

			if (self.borraTarea(gridTask)):
				print ("	Successfully removed from GridWay")
			else:
				print ("	Could not remove task from Grdidway, may appear as zombie")

			return False


	#the best number of tasks being executed is the maximun number of tasks that can be scheduled between 2 calls of ControlExecution
	#this is obtained by the the number of tasks submitted on each dispatch chunk, multiplied by the number of dispatch chunks between
	#two calls of controlExecution

	def bestNumberOfTaskInQueue(self):
		gwHome = os.environ['GW_LOCATION']
		schedFile = open(gwHome + "/etc/sched.conf", 'r')
		for line in schedFile.readlines():
			if line.startswith("DISPATCH_CHUNK"):
				dispatchChunk = int(line.split("=")[1])
				break
		schedFile.close()

		gwdFile = open(gwHome + "/etc/gwd.conf", 'r')

		for line in gwdFile.readlines():
			if line.startswith("SCHEDULING_INTERVAL") > 0:
				schedulingInterval = int(line.split("=")[1])
				break
		gwdFile.close()

		bestNumber = int((1.0 * self.timeBetweenIterations / schedulingInterval) * dispatchChunk)
		return bestNumber


	def purgeTasks(self, dbSession):
		print("")
		print("PURGE DB BEFORE EXECUTION")
		print ("(this may take a while...)")
		for myGridTask in  dbSession.query(GridTask.GridTask).filter((GridTask.GridTask.status!="VENTILATED")):
			if not myGridTask.inputFilesExist():
				print ("Task ID: " + str(myGridTask.id))
				print ("	problematic execution: input files do not exist")
				print ("	Submission will be cancelled and task erased")
				myGridTask.status="VENTILATED"
				dbSession.add(myGridTask)

			elif myGridTask.outputFilesExist():
				print ("Task ID: " + str(myGridTask.id))
				print ("	already finished")
				myGridTask.status="VENTILATED"
				dbSession.add(myGridTask)

		for myGridTask in  dbSession.query(GridTask.GridTask).filter((GridTask.GridTask.status!="VENTILATED"),(GridTask.GridTask.status!="WAITING")):
			print ("Task ID: " + str(myGridTask.id))
			print ("	restarted")
			myGridTask.status="WAITING"
			dbSession.add(myGridTask)

		for myHost in dbSession.query(Host.Host):
			myHost.failedTasks = 0
	        myHost.problematicTasks=0
	        myHost.problematicTasksInARow=0
	        mySession.add(myHost)

		dbSession.commit()

	def controlExecution(self, dbSession):

		#open conection with GW
		while (controller.initGridSession() != 0):
			time.sleep(10)

		#VER QUE TAL VAN LAS QUE ESTAN CORRIENDO

		print ("CONTROL OF TASK EXECUTION")

		print ()
		print ("HOST INFO UPDATE")

		#=======================================================================
		# print("-->DRMAA CALL:gwps <---")
		#=======================================================================

		#print ("desactivado el gwps")
		self.runProcess("gwps -f  > "+ self.gwpsFileLocation)



		print("")
		print("CONTROL OF RUNNNING TASKS")
		print ("studying running tasks")
		for task in dbSession.query(GridTask.GridTask).filter(GridTask.GridTask.status =="RUNNING"):
			host = task.host

			#ver su status actual
			gwTaskStatus = self.obtainGridWayState(task)


			if gwTaskStatus == DRMAA_PS_DONE or gwTaskStatus == DRMAA_PS_FAILED or gwTaskStatus == DRMAA_PS_UNDETERMINED: #acabado
				#===============================================================
				# print("STATUS: RUNNING. GW_STATUS: DONE")
				#===============================================================
				self.updateTerminationStatus(task, gwTaskStatus)
				dbSession.add(task)
				dbSession.add(host)
			dbSession.commit()


		print ("studying queued tasks")
		for task in dbSession.query(GridTask.GridTask).filter(GridTask.GridTask.status =="QUEUED"):
			gwTaskStatus = self.obtainGridWayState(task)
			host = self.obtainTaskHost(dbSession, task.gwID)
			if host != None:
				task.hostID = host.id
				task.host = host

			#por algun motivo ha pasado de enviado a acabado sin pasar por running
			if gwTaskStatus == DRMAA_PS_DONE:
				#===============================================================
				# print("STATUS: QUEUED. GW_STATUS: DRMAA_PS_DONE")
				#===============================================================
				self.updateTerminationStatus(task, gwTaskStatus)


			elif gwTaskStatus== DRMAA_PS_RUNNING:
				task.status="RUNNING"
				task.executionStartDate = datetime.now()

			elif gwTaskStatus == DRMAA_PS_QUEUED_ACTIVE:
				timeLimit = datetime.now()- timedelta(seconds=self.maxQueueTime)
				if task.submissionDate < timeLimit:
					task.showErrorMessage("Too long queue time")
					self.updateTerminationStatus(task, gwTaskStatus)

			#si ha petado o se ha perdido la reenvio
			elif gwTaskStatus == DRMAA_PS_UNDETERMINED or gwTaskStatus == DRMAA_PS_FAILED or gwTaskStatus == None:
				task.showErrorMessage("Unknown problem in QUEUE stage")
				self.updateTerminationStatus(task, gwTaskStatus)

			dbSession.add(task)
			dbSession.add(host)
		dbSession.commit()

		print ("studying submitted tasks")
		for task in dbSession.query(GridTask.GridTask).filter(GridTask.GridTask.status =="SUBMITTED"):
			gwTaskStatus = self.obtainGridWayState(task)
			host = self.obtainTaskHost(dbSession, task.gwID)
			if host != None:
				task.hostID = host.id
				task.host = host

			#por algun motivo ha pasado de enviado a acabado sin pasar por running
			if gwTaskStatus == DRMAA_PS_DONE:
				#===============================================================
				# print("STATUS: SUBMITTED. GW_STATUS: DRMAA_PS_DONE")
				#===============================================================
				self.updateTerminationStatus(task, gwTaskStatus)

			elif gwTaskStatus== DRMAA_PS_RUNNING:
				task.status="RUNNING"
				task.executionStartDate = datetime.now()


			elif gwTaskStatus == DRMAA_PS_QUEUED_ACTIVE:
				task.status="QUEUED"

			elif gwTaskStatus == DRMAA_PS_UNDETERMINED:
				timeLimit = datetime.now()- timedelta(seconds=self.maxQueueTime)
				if task.submissionDate < timeLimit:
					task.showErrorMessage("Queued for two hours")
					self.updateTerminationStatus(task, gwTaskStatus)


			#si ha petado o se ha perdido la reenvio
			elif gwTaskStatus == DRMAA_PS_FAILED or gwTaskStatus == None:
				task.showErrorMessage("Unknown problem in SUBMITTED stage")
				self.updateTerminationStatus(task, gwTaskStatus)

			dbSession.add(task)
			dbSession.add(host)

		dbSession.commit()


		print("")
		print("UPDATING LIST OF BANNED HOSTS")
		bannedHosts = []
		for host in dbSession.query(Host.Host).order_by(desc(Host.Host.lastProblematicTask)):
			if host.isBanned():
				bannedHosts.append(host)
			if len(bannedHosts) > self.bannedHostLimit:
				break


		for host in bannedHosts:
			print ("	" + host.hostname)



		#enviar al Grid las tareas que todavia no han sido enviadas
		#esto se hace despues del paso anterior (y no antes, que seria lo intuitivo) para evitar que la enviemos e
		#inmediatamente despues estemos obteniendo su estado de ejecucion


		#####
		#
		#Update group status and removal of finished groups
		print ("UPDATING GROUP INFO")

		#=======================================================================
		# for group, notFinishedTasks in dbSession.query(TaskGroup.TaskGroup, func.count(GridTask.GridTask) ).\
		#								join(GridTask.GridTask, GridTask.GridTask.taskGroupID == TaskGroup.TaskGroup.id).\
		#								filter(TaskGroup.TaskGroup.finished == False,\
		#									 GridTask.GridTask.status != "VENTILATED",GridTask.GridTask.status != "DELETING").\
		#								group_by(GridTask.GridTask.taskGroupID):
		#=======================================================================

		for group in dbSession.query(TaskGroup.TaskGroup).filter(TaskGroup.TaskGroup.finished == False):

			notFinishedTasks = dbSession.query(func.count(GridTask.GridTask)).\
			 						filter(GridTask.GridTask.taskGroupID==group.id,\
										GridTask.GridTask.status != "VENTILATED",GridTask.GridTask.status != "DELETING").scalar()


			if notFinishedTasks == 0:
				group.finished = True
				print("TaskGroup " + str(group.id) + " status: finished")
				dbSession.add(group)

				print ("Executing post-process script of group " + str(group.id) + ". This will run in background")
				self.runProcess(group.postProcessScript)
		dbSession.commit()






		print("")
		print("TASK SUBMISSION & RE-SUBMISSION")

		tasksToSubmit = []
		if (self.sequentialExecution):
			firstPendingGroup = dbSession.query(TaskGroup.TaskGroup).filter(TaskGroup.TaskGroup.finished == False).first()
			pendingTaksInGroup = dbSession.query(func.count(GridTask.GridTask)).filter(firstPendingGroup.id == GridTask.GridTask.taskGroupID, GridTask.GridTask.status!="WAITING").scalar()

			if pendingTaksInGroup > 0:
				print ("	New group submission is not  needed")
				for task in dbSession.query(GridTask.GridTask).filter(firstPendingGroup.id == GridTask.GridTask.taskGroupID, GridTask.GridTask.status == "WAITING"):
					tasksToSubmit.append(task)
			else:
				print("	new task group to be submitted: " + str(firstPendingGroup.id))
				for task in dbSession.query(GridTask.GridTask).filter(firstPendingGroup.id == GridTask.GridTask.taskGroupID):
					tasksToSubmit.append(task)
		else:

			numberOfSubmittedTasks = dbSession.query(func.count(GridTask.GridTask)).filter(GridTask.GridTask.status =="SUBMITTED").scalar()
			numberOfWaitingTasks = dbSession.query(func.count(GridTask.GridTask)).filter(GridTask.GridTask.status =="WAITING").scalar()
			maxSubmittedTasks = self.bestNumberOfTaskInQueue()

			#number of tasks to submit regarding system
			numberOfTasksToSubmit = min(maxSubmittedTasks - numberOfSubmittedTasks, numberOfWaitingTasks)

			print ("numberOfSubmittedTasks numberOfWaitingTasks maxSubmittedTasks numberOfTasksToSubmit" + str(numberOfSubmittedTasks) + " " +str(numberOfWaitingTasks) + " " + str(maxSubmittedTasks) + " " + str(numberOfTasksToSubmit))

			#number of tasks to submit considering user preferences
			numberOfTasksToSubmit = min(numberOfTasksToSubmit, self.maxAllowedTasksToSubmit)

			print("	Number of tasks to submit: " + str(numberOfTasksToSubmit))

			#aqui despues de hostID ponia ", GridTask.GridTask.id"
			for task in dbSession.query(GridTask.GridTask).filter(GridTask.GridTask.status =="WAITING").limit(numberOfTasksToSubmit):
				tasksToSubmit.append(task)


		for task in tasksToSubmit:
				task.executionStartDate=None
				controller.submitTaskToTheGrid(task, bannedHosts)
				dbSession.add(task)
		dbSession.commit()




		######
		######
		# replica control

		print("")
		print("REPLICA CONTROL")
		self.replicaControl(dbSession)




	#aqui consideramos finished cualquier tarea que  tiene sus archivos de salida
	#esto tiene una utilidad doble: por un lado controla las rtareas replicadas, y por otro
	#aquellas en las que ha habido error y no se han actualizado a pesar de haber acabado (culpa de GW)
	#lo de waiting no se si es un freno o es bueno, hay que pensarlo. por un lado evita algun pequeno problema pero por otro
	#anade un overhead enorme

		print("")
		print("CONTROL OF OLD, FINISHED AND LOST TASKS")


		for task in dbSession.query(GridTask.GridTask).filter(GridTask.GridTask.status !="VENTILATED", GridTask.GridTask.status !="DELETING", GridTask.GridTask.status !="WAITING"):
			if task.outputFilesExist():
				print("SUCCESFUL EXECUTION of task " + str (task.id) + " with gwID "  + task.gwID)
				host = task.host
				#esto es menos elegante que un chandal de cuero
				if host == None:
					host = self.obtainTaskHost(dbSession, task.gwID)
				if host != None:
					host.registerSuccesfulExecution()
					dbSession.add(host)
				else:
					print ("	Could not find host")
				task.status = "VENTILATED"
				task.endDate = datetime.now()

				if not (self.borraTarea(task)):
					task.status ="DELETING"
				dbSession.add(task)

			dbSession.commit()


		print ("")
		for task in dbSession.query(GridTask.GridTask).filter(GridTask.GridTask.status =="DELETING"):
			#self.updateTerminationStatus(task)


			gwTaskStatus = self.obtainGridWayState(task)

			if gwTaskStatus == DRMAA_PS_DONE or gwTaskStatus == DRMAA_PS_FAILED:
				if (self.borraTarea(task)):
					print ("	Old task " + task.gwID + " removed from GridWay")
					task.status = "VENTILATED"
					task.endDate = datetime.now()
					dbSession.add(task)
			elif gwTaskStatus == DRMAA_PS_UNDETERMINED:
					print ("Old task " + task.gwID + " could not be found, considered to be removed from GridWay")
					task.endDate = datetime.now()
					task.status = "VENTILATED"
					dbSession.add(task)

		dbSession.commit()


		##########
		#
		#Before finishing, show info
		print("")
		print("TASK STATUS")
		numberOfRunningTasks = dbSession.query(func.count(GridTask.GridTask)).filter(GridTask.GridTask.status =="RUNNING").scalar()
		print("Tasks Running: " + str(numberOfRunningTasks))

		maxQueuedTasks = dbSession.query(func.count(GridTask.GridTask)).filter(GridTask.GridTask.status =="QUEUED").scalar()
		print("Tasks Queued: " + str(maxQueuedTasks))

		numberOfSubmittedTasks = dbSession.query(func.count(GridTask.GridTask)).filter(GridTask.GridTask.status =="SUBMITTED").scalar()
		print("Tasks Submitted: " + str(numberOfSubmittedTasks))

		numberOfWaitingTasks = dbSession.query(func.count(GridTask.GridTask)).filter(GridTask.GridTask.status =="WAITING").scalar()
		print("Tasks Waiting: " + str(numberOfWaitingTasks))

		controller.exitGridSession()

if __name__ == '__main__':

		print ("Analyzing input parameters")
		sequentialExecution = False
		purge = False
		for param in sys.argv:
			if param == "-purge":
				print ("Purge DB")
				purge = True
			elif param == "-sequential":
				print ("SEquential execution")
				sequentialExecution = True


		controller = GridWayController(sequentialExecution)

		engine = create_engine('mysql://'+base.dbUser+':'+base.dbPassword+'@localhost/DistributedController', echo=False)
		mySessionClass = sessionmaker(bind=engine)
		mySession = mySessionClass()
		metadata = MetaData()

		controller.initializeDB(metadata, engine)

		if purge:
			controller.purgeTasks(mySession)

		while True:
			iterationStart = datetime.now()
			print (iterationStart)

			controller.controlExecution(mySession)
			if controller.endExecution(mySession):
				break
			print("...")
			print("")

			executionTime = datetime.now() - iterationStart
			sleepingTime = timedelta(seconds=controller.timeBetweenIterations) - executionTime
			if sleepingTime  > timedelta(seconds=0):
				print ("sleeping time: " + str(sleepingTime))
				sleep(float(sleepingTime.seconds))
			else:
				print ("no sleeping time, loop took more than " + str(controller.timeBetweenIterations)+ " seconds")
		#=======================================================================
		# controller.controlExecution(mySession)
		#=======================================================================


		print("APPLICATION FINISHED, EXITING")
