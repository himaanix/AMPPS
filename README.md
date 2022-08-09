In order to use these scripts, you must first have some basic requirements.
1. Have O3DE installed - instructions for this can be found at ()
2. Have the projects that you desire to test cloned
3. O3DE, the target projects, and this repository should all be cloned at the same level
4. You must have python installed on your machine
5. You must have matplotlib installed if you intend to use the graphing functionality


Once you have completed the steps above, you may configure the settings.json file.
For each sample in "samples_to_run" there are 11 variables that are needed. 
"url": this is the url for the git repository of the target project
"project": this is the local name for the folder of the target project
"game_executable": this is the name of the executable of the project without the .exe extension
"subfolder": if the main files of the project are in subfolder, include this here
"branch": this is the branch of the project that you have cloned and are testing
"cmd_param": when the game executable is run, specify what command line parameters you would like to run it with
"width": this is the width you would like the Viewport resized to
"height": this is the height you would like the Viewport resized to
"path_to_data": This is the path to the local file where you will store the data that is collected
"data_name": This is the name of the CSV data file where the collected data is stored
"output_location": This is the output location of the generated data in the project. It is important that the generated Data follows the same format as in the wiki.
More information on each of these parameters can be found in the wiki


How to Use The Functionalities Together:
Simply type into the command line "runner.py"
This will configure, build, generate and collect data, and save in the "path_to_data" location images of your graphs.


How to Use the Graphing Functionality Alone:
If the file in "data_name" is not empty, ensure that the column names and order are: "Date", "Time", "BenchmarkName", "GPU", "Mean", "Min", "Max", and "Data"
Once the file has been populated with the data that you want graphed, you can run (). This will save a plot of the Max, Min, Mean and Standard Deviation of the data for each row in the file. 

If the Data required is already in the CSV file, graphy.py can be run with either the DataOverTime function, or with the HistOfSingleTest function. Graphing only a subsection of the Data is a feature currently in development. If the data is already in a dictionary format the AddRowCsv function in utilities.py can add the data to the specified CSV file. 

DataOverTime: This function plots a graph with standard deviation bars in blue, the mean in black, and the max and min in red.

HistOfSingleTest: This plots a histogram of the given test as well as a red line indicating the mean, and a green line indicating the maximum