package es.ciemat.gridExecution; //MAYBE THIS IS WRONG

import java.io.IOException;
import java.util.LinkedList;


/**
 * Encapsulates all the information related to the execution of tasks on the Grid
 *
 * @author Manuel Rodríguez Pascual
 *
 * @since 0.1
 */

public interface GridTask {

	/**
	 *  name of the executable file that will be executed on the remote site
	 *
	 *
	 * @return the name of the executbale
	 */
	public abstract String getExecutable();


	/**
	 * sets the name of the executable file that will be executed on the remote site
	 *
	 *
	 * @param executable name of the execuable
	 */
	public abstract void setExecutable(String executable);

	/**
	 * arguments of the executable.
	 *
	 * They will be concatenated on the remote site, forming a long string
	 *
	 *
	 * @return the arguments of the executable
	 */
	public abstract String[] getArguments();


	/**
	 * sets the arguments of the executable
	 *
	 * @param arguments the arguments of the execuable
	 */
	public abstract void setArguments(String[] arguments);


	/**
	 *  output directory on the remote site
	 *
	 * @return the output directory on the remote site
	 */
	public abstract String getOutputPath();

	/**
	 * sets the output directory on the remote site
	 *
	 * @param outputPath output directory on the remote site
	 */
	public abstract void setOutputPath(String outputPath);

	/**
	 * output file, where stdout will be redirected.
	 *
	 * Default value is stdout.GW_JOB_ID
	 *
	 *
	 * @return output file name
	 */
	public abstract String getOutputFile();

	/**
	 * sets the output file, where stdout will be redirected
	 *
	 *
	 * @param outputFile file name
	 */
	public abstract void setOutputFile(String outputFile);

	/**
	 *  the error path on the remote site
	 *
	 * @return error path on the remote site
	 */
	public abstract String getErrorPath();

	/**
	 * sets the error path on the remote site
	 *
	 * @param errorPath path on the remote site
	 */
	public abstract void setErrorPath(String errorPath);

	/**
	 *  the input path on the remote site
	 *
	 * @return input path on the remote site
	 */
	public abstract String getInputPath();

	/**
	 * sets the input path on the remote site
	 *
	 * @param inputPath path on the remote site
	 */

	public abstract void setInputPath(String inputPath);


	/**
	 * input sandbox on the remote site.
	 *
	 * Currently, this is not used on DRMAA-based templates
	 *
	 * @return input sandbox on the remote site
	 */
	public abstract String getInputSandbox();

	/**
	 * sets input sandbox on the remote site.
	 *
	 * Currently, this is not used on DRMAA-based templates
	 *
	 * @param inputSandbox input sandbox name
	 */
	public abstract void setInputSandbox(String inputSandbox);

	/**
	 * output sandbox on the remote site.
	 *
	 * Currently, this is not used on DRMAA-based templates
	 *
	 * @return output sandbox on the remote site
	 */
	public abstract String getOutputSandbox();


	/**
	 * sets output sandbox on the remote site.
	 *
	 * Currently, this is not used on DRMAA-based templates
	 *
	 * @param outputSandbox input sandbox name
	 */

	public abstract void setOutputSandbox(String outputSandbox);

	/**
	 * Working directory on local site.
	 *
	 * This is the origin of relative routes for input/output files
	 *
	 *
	 * @return working directory path
	 */
	public abstract String getWorkingDirectory();

	/**
	 * sets the Working directory on local site.
	 *
	 * This is the origin of relative routes for input/output files
	 *
	 *
	 * @param workingDirectory working directory path
	 */
	public abstract void setWorkingDirectory(String workingDirectory);

	/**
	 * requirement list for remote hosts
	 *
	 *
	 * @return the requirement list
	 */
	public abstract String getRequirements();

	/**
	 * sets the requirement list for remote hosts
	 *
	 * @param requirements requirement list
	 */

	public abstract void setRequirements(String requirements);

	/**
	 *
	 * input files for the Grid task
	 *
	 * @return input file names
	 */
	public abstract String[] getInputFiles();


	/**
	 * sets the input files for the Grid task
	 *
	 * @param inputFiles input file names
	 */
	public abstract void setInputFiles(String[] inputFiles);


	/**
	 *
	 * output files for the Grid task, that will be fetched from the remote site
	 *
	 * @return output file names
	 */

	public abstract String[] getOutputFiles();

	/**
	 * sets the output files for the Grid task, that will be fetched from the remote site
	 *
	 * @param outputFiles output file names
	 */
	public abstract void setOutputFiles(String[] outputFiles);


	/**
	 *
	 * Name of the task to execute
	 *
	 * @return task name
	 */
	public abstract String getTaskName();


	/**
	 *
	 *sets the name of the task to execute on the remote site
	 *
	 * @param taskName name of the task
	 */
	public abstract void setTaskName(String taskName);


	/**
	 *
	 * native specification.
	 *
	 * no tengo la menor idea de qué es esto, pero ha de existir por alguna razón
	 *
	 *
	 * @return native specification
	 */
	public abstract String getNativeSpecification();

	/**
	 * sets the native specification
	 *
	 *
	 *
	 * @param nativeSpecification native specification
	 */
	public abstract void setNativeSpecification(String nativeSpecification);

	/**
	 *
	 * exports the information related to a task into an XML string
	 *
	 *
	 *
	 * @return a string containing the task information
	 */
	public abstract String toXML();

	/**
	 *
	 * updates all the task information from an XML file
	 *
	 * @param fileName filename
	 */
	public abstract void fromXML(String fileName);

	/**
	 *
	 * export the information related to a task to an XML file
	 * @param fullName name of the file
	 * @return whether the export was successful or not
	 * @throws IOException if could not store the task on the desired file
	 */
	public abstract boolean exportGridTask(String fullName) throws IOException;




	/**
	 *
	 * load a group of tasks from a file. That file contains the names
	 * of other files, each containing a taks. This is, a method is a simple way
	 * of calling "fromXML" multiple times
	 *
	 * @param tasksFile filename
	 * @return linkedList of GridTasks
	 * @throws IOException
	 */
	public abstract LinkedList<GridTask> loadGridTasks(String tasksFile) throws IOException;


	/**
	 *
	 * Store a group of tasks into files.
	 * There is an index file, stores in $PATH/all_grid_task, that contains a
	 * line for each task. That line represents a file_name, in the form of $PATH/file_name
	 * that contains all the related information.
	 *
	 * this method is like calling exportGridTask one time per task and then saving all the file_names
	 * in a format that  loadGridTasks can understand
	 *
	 * @param gridTaskList list of tasks that will be stored
	 * @param path path where all the tasks will be stored
	 * @return whether the export was successful or not
	 * @throws IOException
	 */
	public abstract boolean exportGridTasks(LinkedList<GridTask> gridTaskList, String path) throws IOException;

}
