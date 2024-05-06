# Periodicity-detection
A code to slice a given data into n laps based on the autocorrelation and local maximas of speed and acceleration data. The function saves the data into n csv files.
## Required libraries:
numpy, pandas, scipy, csv (plotly for the test.ipynb).
If you don't have these install them with pip or conda before running the code.

## Setup and running the code:
1. Put the csv file you want to slice up and the code file in the same folder

2. Change the path and n variables at the end of the file as needed according to the comments

3. Run the python file and you will have a smaller csv for each lap.

Note that the code only works for a certain type of csv file generated bx MaxxECU engine management, with the speific column names used in the code

## Test run and details

You can find a test and it's results in the test.ipynb file. In this file I also described in more detail the idea behind the method I am using and why it is useful and working. 

To see this simply download the test.ipynb file. Open it and check the results. Note that if you want to rerun certain cells you will need an example data. Thw one I am using in my test is bigger than 25 MB so I cannot upload it here but if you want to try out the test for yourself reach out to me in email and I will happily provide you the data I was using. papp.gyorgy.szabolcs@gmail.com
