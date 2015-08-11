'''
Created on Feb 22, 2013

@author: u5682
'''

import subprocess as sub

class ShellExecution(object):
	'''
	classdocs
	'''


	def __init__(self):

		return None
		
def execute(commandToExecute):
	# Start subprocess
	print ("command to execute: " + commandToExecute)
	p = sub.Popen(commandToExecute + ' 2>&1', shell = True, stdout=sub.PIPE)
	# Wait for it to finish
	p.wait()
	# Get output
	res = p.communicate()[0]

	# If error, raise exception
	if p.returncode:
		raise 'Error in "{0}". Exit code: {1}. Output: {2}'

	# Else, return output
	return res

	