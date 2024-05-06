# importing the required libraries
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from scipy.signal import find_peaks
import csv

# required functions for the code

def autocorr(x: np.ndarray) -> np.ndarray:

    """ Calculates the autocorrelation of the input array."""

    n = x.size # size of the array
    norm = (x - np.mean(x)) # normalizing the array by subtracting the mean
    result = np.correlate(norm, norm, mode='full') # finding the correlation of the array with itself
    lengths = np.concatenate((np.arange(n, round(n*0.1), -1), np.ones(round(n*0.1), dtype=int)*round(n*0.1))) # setting the last 10% of the array to a constant value so the autocorrelation is converging to 0
    acorr = result[n-1: 2*n] / (x.var() * lengths) # calculating the autocorrelation 
    return acorr

def find_local_maximas(array: np.ndarray, nmaximas: int, radius=None) -> np.ndarray:

    """ Finds given number of local maximas in the input array using a sliding window approach with a default radius of n / nmaximas, where n is the length of the array."""
    
    n = len(array) # Length of the array
    if radius is None:
        radius = n // nmaximas  # Default radius
    
    # Ensure radius is at least 1
    radius = max(radius, 1)
    
    # Initialize variables
    interval_start = radius
    interval_end = 2 * radius
    maximas = []

    while len(maximas) < nmaximas: # Loop until we have the required number of maximas
        interval = array[interval_start:interval_end] # Get the interval
        max_index = np.argmax(interval) + interval_start # Find the index of the max value in the interval
        maximas.append(max_index) # Append the index to the maximas list 
        interval_start += radius # Update the interval start
        interval_end += radius # Update the interval end

        # Check if we've reached the end of the array
        if interval_end >= n:
            break

    # Ensure exactly 10 maximas
    if len(maximas) < nmaximas:
        # Calculate differences between consecutive maximas
        maximas_with_1 = np.concatenate(([1], maximas, [n])) # Add 1 and n to the list of maximas
        differences = np.diff(maximas_with_1) # Find the differences between consecutive maximas
        max_difference_index = np.argmax(differences) # Find the index of the largest difference
        start_gap = maximas_with_1[max_difference_index] # Find the start of the largest gap
        end_gap = maximas_with_1[max_difference_index + 1] # Find the end of the largest gap
        # Find local maxima in the middle of the largest gap
        max_index = find_local_maximas(array[start_gap:end_gap], radius=radius // 2, nmaximas=1)[0] #

        maximas.append(max_index) # Append the index to the maximas list

    # Sort maximas
    maximas.sort()

    # Ensure exactly given number of maximas
    maximas = maximas[:nmaximas]

    return maximas

def slice_csv(big_csv_path: str, indices_array: np.ndarray) -> None:

    """Slices a big CSV file into smaller CSV files based on the indices in the indices_array."""

    # Open the big CSV file for reading
    with open(big_csv_path, 'r', newline='') as big_csv_file:
        # Create a CSV reader
        csv_reader = csv.reader(big_csv_file)
        
        # Read the header from the big CSV file
        header = next(csv_reader)
        
        # Create a dictionary of output CSV writers for each lap
        lap_writers = {}
        for i, index in enumerate(indices_array, start=1): # Enumerate the indices array
            lap_filename = f"lap_{i}.csv" # Create the filename for the lap CSV file
            lap_file = open(lap_filename, 'w', newline='') # Open the lap CSV file for writing
            lap_writer = csv.writer(lap_file) # Create a CSV writer for the lap CSV file
            lap_writers[index] = (lap_file, lap_writer) # Add the lap CSV writer to the dictionary
            # Write the header to each output CSV file
            lap_writer.writerow(header)
        
        # Read rows from the big CSV file and write them to the appropriate lap CSV file
        for row_number, row in enumerate(csv_reader, start=1): # Enumerate the rows in the big CSV file
            for index, (lap_file, lap_writer) in lap_writers.items(): # Enumerate the lap CSV writers
                if row_number <= index: # Check if the row number is less than or equal to the index
                    lap_writer.writerow(row) # Write the row to the lap CSV file
                    break # Break the loop
    
    # Close all lap CSV files
    for lap_file, _ in lap_writers.values(): # Enumerate the lap CSV files
        lap_file.close() # Close the lap CSV file


############### THE MAIN FUNCTION ###############


def lap_slicer(df: pd.DataFrame, nlaps: int) -> None:
    """
    Function to slice the data into n laps based on the autocorrelation and local maximas of speed and acceleration data. The function saves the data into n csv files.
    """

    speed = df['Undriven wheels avg spd [254]']
    ay = df['User CAN14 (Acceleration Y) [760]']

    # get the indices of the local maximas of the autocorrelation of the speed and acceleration data

    data =  np.array([speed, ay]).T # Combine the speed, rpm and acceleration data into a single array

    # Calculate the autocorrelation of the data
    autocorr_results = []
    for i in range(data.shape[1]): # Loop through the columns of the data
        autocorr_results.append(autocorr(data[:, i])) # Calculate the autocorrelation of the column and appends it to the results

    peaks = [find_local_maximas(result, nlaps) for result in autocorr_results] # Find the local maximas of the autocorrelation results

    # Calculate the average across dimensions
    average_maxima = np.mean(peaks, axis=0) # Calculate the average of the peaks

    # Slice the data based on the average maximas
    slice_csv('endu.csv', average_maxima) # Slice the data into laps based on the average maximas

# if the file is run as a script the following code will be executed

if __name__ == '__main__':
    n = 10 # replace this with the number of laps in the data
    path = 'endu.csv' # replace this with the path to the data file
    df = pd.read_csv(path) # read the data file
    lap_slicer(df, n)
    print('Data sliced into laps successfully!') # print a success message

