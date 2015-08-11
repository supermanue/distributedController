'''
Created on Aug 20, 2012

@author: Manuel Rodríguez Pascual, <manuel.rodriguez.pascual@gmail.com>

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

import GridTask, TaskInfo, InputFile, OutputFile, GridTask, Argument, TaskGroup

import sys

from sqlalchemy import *
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

from datetime import datetime, timedelta

if __name__ == '__main__':
	
   
	if len(sys.argv) != 3:
		print("usage: ExecutionStats firstTask lastTask")
		sys.exit(-1)
	
	
	
	#init stuff
	#boring
	engine = create_engine('mysql://root:monteraPass2013@localhost/DistributedController', echo=False)
	mySessionClass = sessionmaker(bind=engine)
	mySession = mySessionClass()
	metadata = MetaData()
	taskInfos = TaskInfo.dbDesign(metadata)
	inputFiles = InputFile.dbDesign(metadata)
	outputFiles = OutputFile.dbDesign(metadata)
	arguments = Argument.dbDesign(metadata)
	gridTasks = GridTask.dbDesign(metadata)
	taskGroups = TaskGroup.dbDesign(metadata) 
	metadata.create_all(engine)
	
	
	#load desired tasks
	
	minElement = int(sys.argv[1])
	maxElement = int(sys.argv[2])
	taskList = mySession.query(GridTask.GridTask).filter(GridTask.GridTask.taskGroupID>=minElement,GridTask.GridTask.taskGroupID<=maxElement, GridTask.GridTask.id < 50000)



	'''
	Creation date:
	-originalmente representaba la fecha de creación de la tarea.
	Esto no tiene mucho sentido, porque las puedes haber creado el mes pasado
	y empezar a ejecutarlas mañana.
	
	-pero hay que tener algo para diferencias las tareas normales y las réplicas
	de una manera molona en las gráficas
	
	-creation date ahora cuenta a partir del momento en que empieza a ejecutarse
	 la primera tarea. Si se ha creado antes es cero, y si no pues lo que indiques
	
	'''
	firstTaskSubmission = datetime.now()
	
	for task in taskList:
		if task.submissionDate != None:
			firstTaskSubmission = min(firstTaskSubmission, task.submissionDate)
		

	taskTimes = []
	
	print ("TASK_ID	Creation time	Submission time	Execution time	End time")

	for task in taskList:
		
		taskInit = max(task.creationDate, firstTaskSubmission)
		
		#si ha sido creada antes de enviar la primera lo consideramos cero
		creationTime = taskInit - firstTaskSubmission
		#=======================================================================
		# if creationTime > timedelta(0):
		#	print ("mas que cero")
		#=======================================================================
		
		try:
			submissionTime = task.submissionDate - taskInit
			
		except:
			submissionTime = timedelta(0)
			
		try:   
			executionTime = task.executionDate - task.submissionDate
		except:
			executionTime = timedelta(0)
			
		try:
			endTime = task.endDate - task.submissionDate
		except:
			endTime = timedelta(0)
		taskTimes.append([creationTime, submissionTime, executionTime, endTime])
	
		print (str(task.id) + "	" + str(creationTime.seconds) + "	" + str(submissionTime.seconds) + "	" + str(executionTime.seconds) + "	" + str(endTime.seconds))
