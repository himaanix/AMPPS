<h2> AMPPS </h2>  

AMPPS stands for Automated Multi-Project Performance Collection System.  
This repository allows for collecting the performance data for multiple projects easily and efficiently.  

<h2>In order to use these scripts, you must first have some basic requirements:</h2>  

1. Have O3DE installed - instructions for this can be found at https://github.com/o3de/o3de  
2. Have the projects that you desire to test cloned  
3. O3DE, the target projects, and this repository should all be cloned at the same level  
4. You must have python installed on your machine  
5. You must have matplotlib installed if you intend to use the graphing functionality  


<h2>Once you have completed the steps above, you may configure the settings.json file:</h2>  

Unless stated otherwise all paths need to be relative to the AMPPS directory
* "path_to_o3de": Specify the path to O3DE in your file system here. 
For each project in "samples_to_run" there are 13 variables that are needed.  
* "url": this is the url for the git repository of the target project  
* "project": this is the path to the folder of the target project  
* "game_executable": this is the name of the executable of the project without the .exe extension  
* "subfolder": if the main files of the project are in subfolder, include the name of the subfolder here  
* "branch": this is the branch of the project that you have cloned and are testing  
* "cmd_param": when the game executable is run, specify what command line parameters you would like to run it with  
* "width": this is the width you would like the Viewport resized to  
* "height": this is the height you would like the Viewport resized to  
* "frame_time": this is the amount of frames that you would like data collected for  
* "idle_time": this is the amount of frames you would like the level to idle for before beginning data collection  
* "path_to_data": This is path to the local CSV file where you will store the data that is collected as well as where any graphs generated will be saved
* "data_name": This is the name of the CSV file where the collected data is stored  
* "output_location": This is the output location of the generated data in the project. It is important that the generated Data follows the same format as in the wiki. This should be relative to the subfolder. This path should be ***relative to the user folder*** in your project.  

More information on each of these parameters can be found in the wiki  
  
    

<h2>How to Use:</h2>  

***Run*** `runner.py` ***with the desired command line parameters.***  
* Without any command line parameters runner.py will update the repositories of the project, incrementally build the project and asset processor, run the asset processor, collect and copy data to the specified file, and save a histogram of the latest data, as well as a graph over time of both frametimes and frames per second.  
* In order to run a clean build of the project or a clean build of assets, use `--clean_build` and/or `--clean_assets`  
* If you only want to use a subset of the functionalities, use the parameters for the functions you would like to use. By specifying one or more of these functions, the rest will not execute unless also specified. 
* If you are collecting data, ensure that the data file is not open
* You may also specify an alternate settings.json file with `--path_to_settings` followed by the path to the alternate file.
* For more information on command line parameter options run `runner.py --help`  

  
    
  

<h3>Requirements for the Graphing Functionality:</h3>  

* If the file in "data_name" is not empty, ensure that the column names and order are: "Timestamp", "BenchmarkName", "GPU", "Mean", "Min", "Max", "Standard Deviation", and "Data"
* Once the file has been populated with the data that you want graphed, you can run a graphing function.

<h4>Using the Graphing Functionality for Other Uses:</h4>
If the DataOverTime function is being used to graph something other than FPS, ensure that the fps parameter is always set to false.  

`DataOverTime`: This function plots a graph with standard deviation bars in blue, the mean in black, and the max and min in red.  
`HistOfSingleTest`: This function plots a histogram of the given test as well as a green line indicating the mean, and a red line indicating the maximum  
`HistOfLatest`: This function plots a histogram of the last row in the specified data file


levels/AutomatedTesting/Levels/Performance/10KEntityCpuPerfTest/10KEntityCpuPerfTest.spawnable