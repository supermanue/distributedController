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
import GridTask, TaskInfo, InputFile, OutputFile, Argument, TaskGroup

import sys

from sqlalchemy import *
from sqlalchemy.orm import sessionmaker
import base

if __name__ == '__main__':

    if len(sys.argv) != 2:
        print("que puta mierda es esta")


    #connect to DB and create it if it does not exist

    engine = create_engine('mysql://'+base.dbUser+':'+base.dbPassword+'@localhost', echo=False)

try:
    engine.execute("CREATE DATABASE DistributedController") #create db
except: 
    print ("database already exists")

    engine.execute("USE DistributedController") # select new db

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


    #create task group
    taskGroup = TaskGroup.TaskGroup(sys.argv[1])
    mySession.add(taskGroup)
    mySession.commit()

    print("LOADING TASK GROUP: " + sys.argv[1])
    for xmlFile in open(sys.argv[1], 'r'):
        xmlFile = xmlFile.strip()
        auxTask = GridTask.GridTask()
        auxTask.fromXML(taskGroup.id,xmlFile)
        mySession.add(auxTask)
        print("    Loading task: " + xmlFile)

    print ("    updating DB")
    mySession.commit()


    print("TASKS LOADED")
