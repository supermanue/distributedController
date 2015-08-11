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


class OutputFile(Base):
    '''
    classdocs
    '''

    __tablename__ = 'outputFiles'
    id = Column(Integer, primary_key=True)
    text = Column(String)
    taskID = Column(Integer, ForeignKey('gridTasks.id'))
#    gridTask = relationship("GridTask", backref=backref('outputFiles', order_by=id))
    
    
    def __init__(self, text):
        self.text = text

    def __repr__(self):
        return "<OutputFile('%i', '%s')>" % (self.id, self.text)
    
def dbDesign(metadata):
    return Table('outputFiles', metadata, 
        Column('id', Integer, primary_key=True),
        Column('taskID', Integer),
        Column('text', String(256)))