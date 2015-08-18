gridwayController
-----------------
This is the documentation for gridwayController application.

It consists on a series of scripts and wrappers for a fast, robust and portable execution of tasks.

It is created for personal use and does not intend to serve for anything serious to anybody else. Same applies to this README.

The basic idea is that you can create a template describing your job to be executed on a remote system, and then employ some of the existing scripts to execute it on a given infrastructure. Currently it supports Grid and Cluster.

#Installation

This program requires python 2.7, SQLAlchemy, MySQL, DRMAA and GridWay (just for the Grid)


## Configuration

GridController has some hardcoded parameters. They are all in the __init__ method. The execption is database user and password, which is on base.py

##MySQL
It has to be installed

user/password is hardcoded in base.py . Password cannot be empty.

If mysql is passwordless, you have to set one. It is done with

```
set password = password ('desired password')
```

##SQLAlchemy

Download latest code from https://pypi.python.org/pypi/SQLAlchemy

Install. If a local install (ie not root permissions is desired),

```
mkdir $HOME/libs
cd (SQLAlchemy dir)
python setup.py install --root $HOME/libs

export PYTHONPATH=$PYTHONPATH:$HOME/libs/:
#to set it forever on login, add this same to .bashrc
```

SQLAlchemy is hard-coded configured to employ MySQL. If a diferent one is desired, change it on the source code. of GridController, TaskLoader and ExecutionAnalyer. (I know, it should be simpler...)


#Usage

##Templates

Templates are XML files with a given format.

you can create them by hand or employ an (included) excutable to create them automatically.

### Template format

#### Index

The index is a text file containing one line for each template to execute. The idea is that an index contains information about all tasks composing a job.

```
/home/u5682/templates/test1/corsika_1
/home/u5682/templates/test1/corsika_2
/home/u5682/templates/test1/corsika_3
/home/u5682/templates/test1/corsika_4
/home/u5682/templates/test1/corsika_5
```

#### Templates
A template contains all the information related to a task.

```
<gridTask>
	<jobName>desired job name, as will appar on GridWay</jobName>
	<executable>/bin/sh</executable>
	<arguments>
		<argument>argument to the executable</argument>
    (as many as desired)
	</arguments>
	<workingDirectory>" + directory where input files are stored and output files will be, too + "</workingDirectory>
	<inputFiles>
		<inputFile>file name, relative to working directory</inputFile>
    (as many as desired)
	</inputFiles>
	<outputFiles>
		<outputFile>output file name</outputFile>
    (as many as desired)
	</outputFiles>
</gridTask>
```

###Template creation


####Manual creation
There are some files (dirty hacks in fact) that create templates for different experiments. They are useful because can be adapted to new codes, speeding the template creation.

These files are located in /templateCreation


####App integration
File gridController/GridTask.py can be employed to manage templates in python. It is quite self-explanatory.

Java intrface and code is stored in javaTemplateManager


##loading templates in a database

There is an script for this.

```
python TaskLoader.py <indexFile>
```

##Executing a code on the grid
- Load templates on the database
- Refresh grid certificates in the remote sites (this should not be necessary) with
```
python RefreshCertificates.py
```

- Execute on the Grid with
```
python  GridController.py
```
- When finished, results will be automatically analyzed with ExecutionAnaLyzer.py and displayed on the screen.


##Executing a code in a cluster

As clusters are supposed to be robust, no databases are employed. Templates are just read from an index file and executed.
For PBS, you have to use

```
python pbsMultipleTasks.py <fileWithTaskGroups>
```
Here there is some control not to break the system if too many tasks are submitted at the same time.


If system supports DRMAA, then the script is

```
python MultipleDRAAJobSubmission.py <fileWithTaskGroups>

```
this one has no control of any kind, just submits everything.

Anyway the files in /clusterController are quite experimental, probably don't work, and should be cleaned at some point.



#Authoring & License

Code is distributed with a  GNU GENERAL PUBLIC LICENSE Version 2.

You should have received a copy of the GNU General Public License
along with gridwayController.  If not, see <http://www.gnu.org/licenses/>.


Author: Manuel Rodriguez-Pascual <manuel.rodriguez.pascual@gmail.com>

Insititution: CIEMAT, Madrid, SPAIN


Manuel Rodriguez Pascual, Antonio Juan Rubio-Montero, Rafael Mayo Garcia, "my article", not published yet








#OLD


definir el formato de los templates: directorio, indice y templates
decir que no utiliza los templates de gridway porque estos se pueden usar en otros sitios
(SAGA, drmaa en cluster o lo que sea) haciendo que las aplicaciones sean mas portables


subir la libreria java que crea los templates, ver de que manera
