#!/bin/sh


#executes the desired command after a qsub
#aceptable params:

#working_directory
#executable
#arguments

set -x
echo "executable: " $executable
echo "arguments: " $arguments

./$executable $arguments

