# Periodcity-detection
A code to slice a given data into n laps based on the autocorrelation and local maximas of speed and acceleration data. The function saves the data into n csv files.
## Required libraries:
numpy, pandas, scipy, csv (plotly for the test.ipynb).
If you don't have these install them with pip or conda before running the code.

## Setup and running the code:
1. Put the csv file you want to slice up and the code file in the same folder

2. Change the path and n variables at the end of the file as needed according to the comments

3. Run the python file and you will have a smaller csv for each lap.

## Test run and details

You can find a test and it's results in the test.ipynb file. In this file I also described in more detail the idea behind the method I am using and why it is useful and working. 

To see this simply download the test.ipynb file, open it and check the results, rerun certain cells if you want to.
