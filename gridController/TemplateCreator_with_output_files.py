'''
Created on Feb 12, 2015

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

import os

if __name__ == '__main__':
	
	#params
	executable="/bin/sh"
	argument1="corsika.sh"
	argument2="corsika-73500-lago-single"
	inputFilePath="/soft/users/home/u5682/nfs/todo_corsika/new_experiment/"
	inputFilePrefix="DAT"
	outputTemplatePath="/soft/users/home/u5682/nfs/todo_corsika/new_experiment/templates"
	
	
	#create output folder if it does not exist
	if not os.path.exists(outputTemplatePath):
		os.makedirs(outputTemplatePath)
	
	counter=0
	indexName = outputTemplatePath + "/" + "all_grid_tasks"
	index = open(indexName, 'w')
	#create templates	
	for inputFile in os.listdir(inputFilePath):
		if inputFile.startswith(inputFilePrefix):
			counter+=1
			templateName = outputTemplatePath + "/" + "grid_task_" + str(counter)
			f = open(templateName, 'w')
			f.write("<gridTask>\n")
			f.write("	<jobName>grid_task_"+ str(counter) +"</jobName>\n")
			f.write("	<executable>/bin/sh</executable>\n")
			f.write("	<arguments>\n")
			f.write("		<argument>"+argument1+"</argument>\n")
			f.write("		<argument>"+argument2+"</argument>\n")
			f.write("		<argument>"+ str(counter) +"</argument>\n")
			f.write("		<argument>" + inputFile+ "</argument>\n")
			f.write("	</arguments>\n")
			f.write("	<workingDirectory>" + inputFilePath + "</workingDirectory>\n")
			f.write("	<inputFiles>\n")
			f.write("		<inputFile>corsika.sh</inputFile>\n")
			f.write("		<inputFile>" + inputFile + "</inputFile>\n")
			f.write("	</inputFiles>\n")
			f.write("	<outputFiles>\n")
			f.write("		<outputFile>results"+str(counter) + ".tar.gz</outputFile>\n")
			f.write("	</outputFiles>\n")
			f.write("</gridTask>\n")
			f.close()
			
			index.write(templateName + "\n")
	index.close()
	print ("Templates have been created. Index located at " + indexName)
	
	
