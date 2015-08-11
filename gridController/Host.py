'''
Created on Aug 22, 2012

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

from sqlalchemy import *
from datetime import timedelta, datetime

from base import Base

class Host(Base):
	'''
	classdocs
	'''

	__tablename__ = 'hosts'
	id = Column(Integer, primary_key=True)
	hostname = Column(String)
	successfulTasks = Column(Integer)
	failedTasks = Column(Integer)
	problematicTasks = Column(Integer)
	problematicTasksInARow = Column(Integer)
	lastProblematicTask = Column(DateTime)
	
	bannedTime = 7200
	
	def __init__(self, hostname):
		self.hostname = hostname
		self.successfulTasks = 0
		self.failedTasks = 0
		self.problematicTasks = 0
		self.problematicTasksInARow = 0
		
	def __repr__(self):
		return "<Host('%i', '%s', '%i', '%i', '%i')>" % (self.id, self.hostname, self.successfulTasks, self.failedTasks, self.problematicTasks)



	def registerSuccesfulExecution(self):
		self.successfulTasks +=1
		self.problematicTasksInARow = 0
		
	def registerFailedExecution(self, date):
		self.failedTasks += 1
		
	def registerProblematicExecution(self,date):
		self.problematicTasksInARow +=1
		self.lastProblematicTask = date


#------------------------------------------------------------------------------ 
	#------------------------------------------------------- def isBanned(self):
		#--------------------------------------- if self.problematicTasks < 100:
			#------------------------------------------------------ return False
		#---------------------------------- if self.lastProblematicTask == None:
			#------------------------------------------------------ return False
		# if (2.0 * self.successfulTasks / (self.problematicTasks + self.failedTasks)) > 1:
			#------------------------------------------------------ return False
		#------- timeLimit = datetime.now() - timedelta(seconds=self.bannedTime)
		#------------------------------ if self.lastProblematicTask > timeLimit:
			#------------------------------------------------------- return True
		#---------------------------------------------------------- return False
 


#baneo: incremental, 10 minutos por cada tarea fallida
#con un máximo de un día
	def isBanned(self):
		
		if len(self.hostname.strip())< 2:
			return False
		
		if self.problematicTasksInARow < 10:
			return False
		
		banTime = 10 * 60 * (self.problematicTasksInARow - 10)
		maxBanTime = 24 * 60 * 60
		banTime = min (banTime, maxBanTime)
		
		timeSinceLastFail = datetime.now() - self.lastProblematicTask
		
		if timeSinceLastFail < timedelta(banTime):
			return True
		
		return False
			

	

def dbDesign(metadata):
	return Table('hosts', metadata, 
		Column('id', Integer, primary_key=True),
		Column('hostname', String(256)),
		Column('successfulTasks', Integer),
		Column('failedTasks', Integer),
		Column('problematicTasks', Integer),
   		Column('problematicTasksInARow', Integer),
		Column('lastProblematicTask', DateTime)
)
	



def readHost(gwpsFile, gwID):

	result = "" 

	foundTask = False
	fileToRead = open(gwpsFile, 'r')
	for line in fileToRead.readlines():
		if line.count("JOB_ID") > 0:
			if line.count(gwID) > 0:
				foundTask = True
		if foundTask and line.count("HOST") >0:
			resultWithQueue = line.split("=")[1].strip()
			result = resultWithQueue.split("/")[0]
			resultHost=result.split(".")[0]
			
			result = result[(len(resultHost)+1):]
			break
	return result