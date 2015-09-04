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
import GridTask, TaskInfo, InputFile, OutputFile, Argument, TaskGroup, Host

import sys

from sqlalchemy import *
from sqlalchemy.orm import sessionmaker
import base



if __name__ == '__main__':

    print("Cleaning database")


    #connect to DB and create it if it does not exist

    engine = create_engine('mysql://'+base.dbUser+':'+base.dbPassword+'@localhost', echo=False)

    engine.execute("USE DistributedController") # select new db

    mySessionClass = sessionmaker(bind=engine)
    mySession = mySessionClass()

    #Remove tasks
    print ("    deleting old tasks")
    for gridTask in mySession.query(GridTask.GridTask).filter((GridTask.GridTask.status!="VENTILATED")):
        gridTask.status ="VENTILATED"
        mySession.add(gridTask)

    print ("    deleting old groups of tasks")
    for taskGroup in  mySession.query(TaskGroup.TaskGroup).filter((TaskGroup.TaskGroup.finished==False)):
        TaskGroup.finished=True
        mySession.add(taskGroup)

    print ("    Reseting host info")
    for host in  mySession.query(Host.Host):
        host.failedTasks = 0
        host.problematicTasks=0
        host.problematicTasksInARow=0
        mySession.add(host)


    print ("    Saving everything")
    mySession.commit()


    print("Evrything is clean now")
