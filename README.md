How to Use the Graphing Functionality:
In the settings.json file under "SAMPLES_TO_RUN" the parameter "PathToData" should contain the path to the CSV file that contains the Data to be plotted.
In this file the Headers should be "Date", "Time", "BenchmarkName", "GPU", "Mean", "Min", "Max", and "Data"
If the Data required is already in the CSV file, graphy.py can be run with either the data_over_time function, or with the hist_of_single_test function. Graphing only a subsection of the Data is a feature currently in development. If the data is already in a dictionary format the add_row_csv function in utilities.py can add the data to the specified CSV file. 

data_over_time: This function plots a graph with standard deviation bars in blue, the mean in black, and the max and min in red.

hist_of_single_test: This plots a histogram of the given test as well as a red line indicating the mean, and a green line indicating the maximum