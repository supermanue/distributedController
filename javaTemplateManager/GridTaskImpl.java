package es.ciemat.gridExecution;

import java.io.BufferedReader;
import java.io.BufferedWriter;
import java.io.File;
import java.io.FileReader;
import java.io.FileWriter;
import java.io.IOException;
import java.util.LinkedList;

import javax.xml.parsers.DocumentBuilder;
import javax.xml.parsers.DocumentBuilderFactory;

import org.w3c.dom.Document;
import org.w3c.dom.Element;
import org.w3c.dom.NodeList;
import org.w3c.dom.Node;


public class GridTaskImpl implements GridTask {


	private String executable;
	private String[] arguments;

	private String outputPath;
	private String outputFile;

	private String errorPath;
	private String inputPath;

	private String inputSandbox;
	private String outputSandbox;

	private String workingDirectory;

	private String requirements;

	private String[] inputFiles;
	private String[] outputFiles;

	private String jobName;
	
	private String nativeSpecification;


	public GridTaskImpl() {
		super();
		this.executable = "";
		this.arguments = new String[]{};
		this.outputPath = "";
		this.outputFile = "";
		this.errorPath = "";
		this.inputPath = "";
		this.inputSandbox = "";
		this.outputSandbox = "";
		this.workingDirectory = "";
		this.requirements = "";
		this.inputFiles = new String[]{};
		this.outputFiles = new String[]{};
		this.jobName = "";
		this.nativeSpecification = "";

	}

	public GridTaskImpl(String executable, String[] arguments, String outputPath,
			String outputFile, String errorPath, String errorFile,
			String inputSandbox, String outputSandbox, String workingDirectory,
			String requirements, String[] inputFiles, String[] outputFiles,
			String jobName) {
		super();
		this.executable = executable;
		this.arguments = arguments;
		this.outputPath = outputPath;
		this.outputFile = outputFile;
		this.errorPath = errorPath;
		this.inputPath = errorFile;
		this.inputSandbox = inputSandbox;
		this.outputSandbox = outputSandbox;
		this.workingDirectory = workingDirectory;
		this.requirements = requirements;
		this.inputFiles = inputFiles;
		this.outputFiles = outputFiles;
		this.jobName = jobName;
	}

	/* (non-Javadoc)
	 * @see gridExecution.GridTask#getExecutable()
	 */
	@Override
	public String getExecutable() {
		return executable;
	}

	/* (non-Javadoc)
	 * @see gridExecution.GridTask#setExecutable(java.lang.String)
	 */
	@Override
	public void setExecutable(String executable) {
		this.executable = executable;
	}

	/* (non-Javadoc)
	 * @see gridExecution.GridTask#getArguments()
	 */
	@Override
	public String[] getArguments() {
		return arguments;
	}

	/* (non-Javadoc)
	 * @see gridExecution.GridTask#setArguments(java.lang.String[])
	 */
	@Override
	public void setArguments(String[] arguments) {
		this.arguments = arguments;
	}

	/* (non-Javadoc)
	 * @see gridExecution.GridTask#getOutputPath()
	 */
	@Override
	public String getOutputPath() {
		return outputPath;
	}

	/* (non-Javadoc)
	 * @see gridExecution.GridTask#setOutputPath(java.lang.String)
	 */
	@Override
	public void setOutputPath(String outputPath) {
		this.outputPath = outputPath;
	}

	/* (non-Javadoc)
	 * @see gridExecution.GridTask#getOutputFile()
	 */
	@Override
	public String getOutputFile() {
		return outputFile;
	}

	/* (non-Javadoc)
	 * @see gridExecution.GridTask#setOutputFile(java.lang.String)
	 */
	@Override
	public void setOutputFile(String outputFile) {
		this.outputFile = outputFile;
	}

	/* (non-Javadoc)
	 * @see gridExecution.GridTask#getErrorPath()
	 */
	@Override
	public String getErrorPath() {
		return errorPath;
	}

	/* (non-Javadoc)
	 * @see gridExecution.GridTask#setErrorPath(java.lang.String)
	 */
	@Override
	public void setErrorPath(String errorPath) {
		this.errorPath = errorPath;
	}

	/* (non-Javadoc)
	 * @see gridExecution.GridTask#getInputPath()
	 */
	@Override
	public String getInputPath() {
		return inputPath;
	}

	/* (non-Javadoc)
	 * @see gridExecution.GridTask#setInputPath(java.lang.String)
	 */
	@Override
	public void setInputPath(String inputPath) {
		this.inputPath = inputPath;
	}

	/* (non-Javadoc)
	 * @see gridExecution.GridTask#getInputSandbox()
	 */
	@Override
	public String getInputSandbox() {
		return inputSandbox;
	}

	/* (non-Javadoc)
	 * @see gridExecution.GridTask#setInputSandbox(java.lang.String)
	 */
	@Override
	public void setInputSandbox(String inputSandbox) {
		this.inputSandbox = inputSandbox;
	}

	/* (non-Javadoc)
	 * @see gridExecution.GridTask#getOutputSandbox()
	 */
	@Override
	public String getOutputSandbox() {
		return outputSandbox;
	}

	/* (non-Javadoc)
	 * @see gridExecution.GridTask#setOutputSandbox(java.lang.String)
	 */
	@Override
	public void setOutputSandbox(String outputSandbox) {
		this.outputSandbox = outputSandbox;
	}

	/* (non-Javadoc)
	 * @see gridExecution.GridTask#getWorkingDirectory()
	 */
	@Override
	public String getWorkingDirectory() {
		return workingDirectory;
	}

	/* (non-Javadoc)
	 * @see gridExecution.GridTask#setWorkingDirectory(java.lang.String)
	 */
	@Override
	public void setWorkingDirectory(String workingDirectory) {
		this.workingDirectory = workingDirectory;
	}

	/* (non-Javadoc)
	 * @see gridExecution.GridTask#getRequirements()
	 */
	@Override
	public String getRequirements() {
		return requirements;
	}

	/* (non-Javadoc)
	 * @see gridExecution.GridTask#setRequirements(java.lang.String)
	 */
	@Override
	public void setRequirements(String requirements) {
		this.requirements = requirements;
	}

	/* (non-Javadoc)
	 * @see gridExecution.GridTask#getInputFiles()
	 */
	@Override
	public String[] getInputFiles() {
		return inputFiles;
	}

	/* (non-Javadoc)
	 * @see gridExecution.GridTask#setInputFiles(java.lang.String[])
	 */
	@Override
	public void setInputFiles(String[] inputFiles) {
		this.inputFiles = inputFiles;
	}

	/* (non-Javadoc)
	 * @see gridExecution.GridTask#getOutputFiles()
	 */
	@Override
	public String[] getOutputFiles() {
		return outputFiles;
	}

	/* (non-Javadoc)
	 * @see gridExecution.GridTask#setOutputFiles(java.lang.String[])
	 */
	@Override
	public void setOutputFiles(String[] outputFiles) {
		this.outputFiles = outputFiles;
	}

	/* (non-Javadoc)
	 * @see gridExecution.GridTask#getJobName()
	 */
	@Override
	public String getTaskName() {
		return jobName;
	}

	/* (non-Javadoc)
	 * @see gridExecution.GridTask#setJobName(java.lang.String)
	 */
	@Override
	public void setTaskName(String jobName) {
		this.jobName = jobName;
	}

	public void setNativeSpecification(String nativeSpecification) {
		this.nativeSpecification = nativeSpecification;
	}

	public String getNativeSpecification() {
		return nativeSpecification;
	}
	
	
	//creates an XML String with information about this task on it
	/* (non-Javadoc)
	 * @see gridExecution.GridTask#toXML()
	 */
	@Override
	public String toXML(){
		String solution = "";

		solution+="<gridTask>\n";
		solution+="	<executable>" + this.getExecutable() + "</executable>\n";

		solution+="	<arguments>\n";
		for (String argument: this.getArguments())
			solution+="		<argument>" + argument+ "</argument>" + "\n";	
		solution+="	</arguments>\n";		

		solution+="	<outputPath>" + this.getOutputPath() + "</outputPath>\n";
		solution+="	<outputFile>" + this.getOutputFile() + "</outputFile>\n";
		solution+="	<errorPath>" + this.getErrorPath() + "</errorPath>\n";
		solution+="	<errorFile>" + this.getInputPath() + "</errorFile>\n";
		solution+="	<inputSandbox>" + this.getInputSandbox() + "</inputSandbox>\n";
		solution+="	<outputSandbox>" + this.getOutputSandbox() + "</outputSandbox>\n";
		solution+="	<workingDirectory>" + this.getWorkingDirectory() + "</workingDirectory>\n";
		solution+="	<requirements>" + this.getRequirements() + "</requirements>\n";

		solution+="	<inputFiles>\n";
		for (String inputFile: this.getInputFiles())
			solution+="		<inputFile>" + inputFile+ "</inputFile>" + "\n";
		solution+="	</inputFiles>\n";		

		solution+="	<outputFiles>\n";
		for (String outputFile: this.getOutputFiles())
			solution+="		<outputFile>" + outputFile+ "</outputFile>" + "\n";
		solution+="	</outputFiles>\n";	

		solution+="	<jobName>" + this.getTaskName() + "</jobName>\n";
		solution+="	<nativeSpecification>" + this.getNativeSpecification() + "</nativeSpecification>\n";

		solution+="</gridTask>\n";

		return solution;	
	}


	//updates information from an XML file
	/* (non-Javadoc)
	 * @see gridExecution.GridTask#fromXML(java.lang.String)
	 */
	@Override
	public void fromXML(String fileName){

		File myFile = new File(fileName);

		//File myFile = new File("/Users/Macbook/Documents/workspace/Montera/bin/resource_info.tmp");
		DocumentBuilderFactory docBuilderFactory = DocumentBuilderFactory.newInstance();
		Document doc = null;
		try {
			DocumentBuilder docBuilder = docBuilderFactory.newDocumentBuilder();
			doc =  docBuilder.parse(myFile);
		} catch (Exception e) {
			System.out.println("GridTask, ha petado al parsear el fichero de entrada: " + fileName);
			e.printStackTrace();

			//e.printStackTrace();
		} 
		// normalize text representation
		doc.getDocumentElement ().normalize ();
		NodeList nl = doc.getElementsByTagName("gridTask");


		Node fstNode = nl.item(0);

		if (fstNode.getNodeType() == Node.ELEMENT_NODE) {

			Element element = (Element) fstNode;

			this.obtainGridTask(element);

		} //Si es un nodo
	}

	/*
	 * 
	 * 
	 * creates a new file with name fullName (includes full path)
	 * and stores all the information regarding this task
	 */

	/* (non-Javadoc)
	 * @see gridExecution.GridTask#exportGridTask(java.lang.String)
	 */
	@Override
	public boolean exportGridTask (String fullName) throws IOException{
		File file = new File(fullName);

		//if there exist a previous version, delete it
		if (file.exists()) {
			System.out.println("conflict when storing information from Grid task " + this.getTaskName() + "on file: " + fullName);
			System.out.println("output file already exists, I am rewriting it");
			file.delete();

		}



		BufferedWriter bw = 
			new BufferedWriter(new FileWriter(file));


		bw.write(this.toXML());
		bw.close();
		return true;
	}



	
	/**
	 * reads an XML representing a GridTask and updates the value of this object
	 * @param element the head node of the XML
	 * @return whether the operation was successful
	 */
	private boolean obtainGridTask(Element element){

		this.setExecutable(this.obtainText(element, "executable"));
		this.setOutputPath(this.obtainText(element, "outputPath"));
		this.setOutputFile(this.obtainText(element, "outputFile"));
		this.setErrorPath(this.obtainText(element, "errorPath"));
		//myGridTask.setErrorFile(this.obtainText(element, "errorFile"));
		this.setInputSandbox(this.obtainText(element, "inputSandbox"));
		this.setOutputSandbox(this.obtainText(element, "outputSandbox"));
		this.setWorkingDirectory(this.obtainText(element, "workingDirectory"));
		this.setRequirements(this.obtainText(element, "requirements"));
		this.setTaskName(this.obtainText(element, "jobName"));
		this.setNativeSpecification(this.obtainText(element, "nativeSpecification"));

		
		this.setArguments(this.obtainTextArray(element, "arguments", "argument"));
		this.setInputFiles(this.obtainTextArray(element, "inputFiles", "inputFile"));
		this.setOutputFiles(this.obtainTextArray(element, "outputFiles", "outputFile"));
				
		/*
	fstNmElmntLst = fstElmnt.getElementsByTagName("arguments");
	fstNmElmnt = (Element) fstNmElmntLst.item(0);
	fstNm = fstNmElmnt.getChildNodes();
	String[] arguments = new String [fstNm.getLength()];	
	for (int cont = 0; cont < fstNm.getLength(); cont++){
		Node auxNode = null;
		if (((Node) fstNm.item(cont)).getNodeType() == Node.ELEMENT_NODE)
			auxNode = ((Node) fstNm.item(cont)).getFirstChild();

		//if (auxNode != null)
			arguments[cont] = String.valueOf(auxNode.getNodeValue());
	}
	this.setArguments(arguments);
		 */

		/*
	fstNmElmntLst = fstElmnt.getElementsByTagName("inputFiles");
	fstNmElmnt = (Element) fstNmElmntLst.item(0);
	fstNm = fstNmElmnt.getChildNodes();
	String[] inputFiles = new String [fstNm.getLength()];	
	for (int cont = 0; cont < fstNm.getLength(); cont++)
		inputFiles[cont] = String.valueOf(((Node) fstNm.item(cont)).getNodeValue());
	this.setInputFiles(inputFiles);

	fstNmElmntLst = fstElmnt.getElementsByTagName("outputFiles");
	fstNmElmnt = (Element) fstNmElmntLst.item(0);
	fstNm = fstNmElmnt.getChildNodes();
	String[] outputFiles = new String [fstNm.getLength()];	
	for (int cont = 0; cont < fstNm.getLength(); cont++)
		outputFiles[cont] = String.valueOf(((Node) fstNm.item(0)).getNodeValue());
	this.setOutputFiles(outputFiles);


		 */



		return true;
	} //Si es un nodo

	
	/**
	 * XML-related method
	 * Finds a node with the tag name and returns its value.
	 * It is employed to retrieve the value of an string stored on a XML
	 * 
	 * 
	 * @param element head node
	 * @param tagName tag we are looing for
	 * @return value of the node
	 */
	
	private String obtainText(Element element, String tagName) {
		String text = "";
		NodeList nl = element.getElementsByTagName(tagName);
		if (nl != null && nl.getLength() > 0) {
			Element el = (Element) nl.item(0);
			Node textNode = el.getFirstChild();
			if (textNode != null)
				text = textNode.getNodeValue();
		}
		return text;
	}
	
	
	/**
	 * XML-related method
	 * Finds all the node with the first name, finds all its sons with the second tag name and returns their values.
	 * It is employed to retrieve the value of an string array stored on a XML
	 * 
	 * 
	 * @param element head node
	 * @param fatherTagName tag name of the father
	 * @param sonTagName tag name of the sons
	 * @return the desired string array
	 */
	private String[] obtainTextArray(Element element, String fatherTagName,
			String sonTagName) {
		
		NodeList auxNl = element.getElementsByTagName(fatherTagName);
		
		Element headNode = (Element) auxNl.item(0);
		NodeList newNodeList = headNode.getElementsByTagName(sonTagName);
		
		String text[] = new String[newNodeList.getLength()]; //VERIFICAR SI ESTA LONGITUD ES CORRECTA

		if (newNodeList != null && newNodeList.getLength() > 0) {
	        for (int i = 0; i < newNodeList.getLength(); i++) {
	            // a. Obtener el elemento
	            Element elemento = (Element) newNodeList.item(i);
	            text[i]="";
	            if (elemento!=null)
	            	if (elemento.getFirstChild()!=null)
	            		text[i] = elemento.getFirstChild().getNodeValue();
	            
	        }
	    }
		return text;


	}

	


	public LinkedList<GridTask> loadGridTasks(String tasksFile) throws IOException {
		// TODO Auto-generated method stub
		System.out.println("Loading multiple tasks");

		LinkedList<GridTask> myList = new LinkedList<GridTask>();

		FileReader fr = null;

		fr = new FileReader(tasksFile);

		BufferedReader bf = new BufferedReader(fr);
		String taskFileName;

		// read the file
		while ((taskFileName = bf.readLine()) != null) {
			GridTask myGridTask = new GridTaskImpl();
			myGridTask.fromXML(taskFileName);

			System.out.println("Task loaded.");
			System.out.println("Task info:");
			System.out.println(myGridTask.toXML());

			myList.add(myGridTask);
		}
		
		System.out.println("Grid tasks loaded from file");

		return myList;
		
		
		
		
	}

	@Override
	public boolean exportGridTasks(LinkedList<GridTask> gridTaskList,
			String path) throws IOException {
		//comprobar si existe
		File storePath = new File(path);
		
		if (storePath.exists()) {
			if (storePath.isDirectory()){
				System.out.println("Path is correct and corresponds to an existing directory");	
			}
			else{
				System.out.println("Selected path does not correspond to a directory");
				System.out.println("Problem when processing Grid results");
				
			}
			
		}
		else //si no existe, crearlo
		{
			System.out.println("Selected path does not correspond to an existing directory");
			System.out.println("I will create a new one");
			storePath.mkdirs();

		
		}
		
		
		File file = new File(path + "/all_grid_tasks");
		BufferedWriter bw;	
		int cont = 0;
		try {
			bw = new BufferedWriter(new FileWriter(file));
			for (GridTask gridTask: gridTaskList){
				String fileName = path + "/grid_task_" + cont;
				gridTask.exportGridTask(fileName);
				bw.write(fileName + "\n");
				cont++;
			}
			bw.close();

		} catch (Exception e) {
			// TODO Auto-generated catch block
			System.out.println("Could not store GridTasks information");
			e.printStackTrace();
			return false;
		}

		System.out.println("Task list stored in : " + path+"/all_grid_tasks");
		return true;
			
	}


}
