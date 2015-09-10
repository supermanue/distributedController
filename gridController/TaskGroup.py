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
from sqlalchemy import *

from sqlalchemy.orm import relationship, backref

from base import Base
from datetime import datetime

class TaskGroup(Base):
    '''
    classdocs
    '''

    __tablename__ = 'taskGroups'
    id = Column(Integer, primary_key=True)
    indexFile = Column(String)
    creationDate = Column(DateTime)
    replicas = Column(Integer)
    finished = Column(Boolean)
    postProcessScript = Column(String)

    #gridTask = relationship("GridTask", backref=backref('arguments', order_by=id))

    def __init__(self, indexFile, postProcessScript=null):
        self.indexFile = indexFile
        self.creationDate = datetime.now()
        self.replicas = 0
        self.finished = False
        self.gridTasks=[]
        self.postProcessScript = postProcessScript

    def __repr__(self):
        return "<TaskGroup('%i', '%s')>" % (self.id, self.indexFile)




    def updateStatus(self):
        self.finished = True
        for gridTask in self.gridTasks:
            if gridTask.status != "VENTILATED":
                self.finished = False
                return
        print("TaskGroup " + str(self.id) + " status: finished")


def dbDesign(metadata):
    return Table('taskGroups', metadata,
    Column('id', Integer, primary_key=True),
    Column("creationDate", DateTime),
    Column('indexFile', String(256)),
    Column('replicas', Integer),
    Column('finished', Boolean),
    Column('postProcessScript', String(256)),
           )
