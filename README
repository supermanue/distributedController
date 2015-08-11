gridwayController
-----------------

Author: Manuel Rodriguez-Pascual <manuel.rodriguez.pascual@gmail.com>
Insititution: CIEMAT, Madrid, SPAIN


This is the documentation for gridwayController application.

It consists on a series of scripts and wrappers for a fast, robust and portable execution of tasks.

It is created for personal use and does not intend to serve for anything serios to anybody else.

I will update this documentation at some moment, but not now


#Installation#

Decir que se necesita python version noseque, drmaa, gridway, sqlalchemy y MySQL

El sqlalchemy esta configurado para mysql. si se utiliza otro, cambiarlo en las fuentes
(poner la linea y un enlace al tutorial de sqlalchemy)

poner donde se mete la clave y todo eso para la bbdd

#Usage#

el loader pa cargar los templates
el controller pa ejecutarlos


##Template format & creation##

Templates are XML files with a given format.

you can create them by hand or employ an (included) excutable to create them automatically.

### Template format ###

#### Index ####

The index is a text file containing one line for each template to execute. The idea is that an index contains information about all tasks composing a job.

index.txt
/sñjddjhljhldj
/ñkdjf ñkjf
/ñdkj dlkjd

#### Templates ####
A template contains all the information related to a task.

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


###Template creation###

There are some files (dirty hacks in fact) that create templates for different experiments. They are useful because can be adapted to new codes, speeding the template creation.


##loading templates##


##executing templates on the grid##

1.- Create templates

2.- Load template

3.- Execute template.










definir el formato de los templates: directorio, indice y templates
decir que no utiliza los templates de gridway porque estos se pueden usar en otros sitios
(SAGA, drmaa en cluster o lo que sea) haciendo que las aplicaciones sean más portables


subir la libreria java que crea los templates, ver de que manera



License
-------

este software está liberado bajo licencia GPL, bla bla bla

Citations
------
Users employing this software for scientific articles are encouraged to reference it.

The article that should be cited is:

Manuel Rodriguez Pascual, Antonio Juan Rubio-Montero, Rafael Mayo Garcia, "my article", not published yet
