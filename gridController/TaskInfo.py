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

from sqlalchemy import *
from sqlalchemy.orm import relationship, backref
from base import Base

class TaskInfo(Base):
    '''
    classdocs
    '''
    __tablename__ = 'taskInfos'
    
    id = Column(Integer, primary_key=True)
    
    executable = Column(String)

    outputPath = Column(String)
    outputFile = Column(String)

    errorPath = Column(String)
    inputPath = Column(String)

    inputSandbox = Column(String)
    outputSandbox = Column(String)

    workingDirectory = Column(String)

    requirements = Column(String)

    jobName = Column(String)

    nativeSpecification = Column(String)
    taskID = Column(Integer, ForeignKey('gridTasks.id'))

 #   gridTask = relationship("GridTask", backref=backref('taskInfos', order_by=id))


    def __init__(self, executable, outputPath, outputFile,
                 errorPath, inputPath,
                 inputSandbox, outputSandbox,
                 workingDirectory, requirements,
                 jobName, nativeSpecification):
        self.executable = executable
        self.outputPath = outputPath
        self.outputFile = outputFile
        self.errorPath = errorPath
        self.inputPath = inputPath
        self.inputSandbox = inputSandbox
        self.outputSandbox = outputSandbox
        self.workingDirectory = workingDirectory
        self.requirements = requirements
        self.jobName = jobName
        self.nativeSpecification = nativeSpecification
        
    def __repr__(self):
        #return "<TaskInfo('%i', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s')>" %(self.id, self.executable, self.outputPath, self.outputFile, self.errorPath, self.inputPath, self.inputSandbox, self.outputSandbox, self.workingDirectory, self.requirements, self.jobName, self.nativeSpecification)
		return "<TaskInfo('%i', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s')>" %(self.id, self.executable, self.outputPath, self.outputFile, self.errorPath, self.inputPath, self.inputSandbox, self.outputSandbox, self.workingDirectory, self.requirements, self.jobName, self.nativeSpecification)



def dbDesign(metadata):
    return Table('taskInfos', metadata,
        Column('id', Integer, primary_key=True),
        Column('taskID', Integer),
        Column('executable', String(256)),
        Column('outputPath', String(256)),
        Column('outputFile', String(256)),
        Column('errorPath', String(256)),
        Column('inputPath', String(256)),
        Column('inputSandbox', String(256)),
        Column('outputSandbox', String(256)),
        Column('workingDirectory', String(256)),
        Column('requirements', String(256)),
        Column('jobName', String(256)),
        Column('nativeSpecification', String(256))
        )