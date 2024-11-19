# Import required libraries and functions
import os
from Functions_Library import plot, response_sorting, read_txt

# Get current OS working directory
workdir = os.getcwd()

# Get settings file name
file = workdir + "\\Settings.txt"

# Read settings text file to get username and CSV file name
settings = read_txt(file)

# Print message stating username and CSV file name
print(f"Username: {settings['username']}")
print(f"CSV File: {settings['filename']}")
print(f"Analyzing...")

# Sort the responses chronologically and determine the number of failure and success responses at each hourly timestamp in the CSV file
dates, response_failures, response_successes = response_sorting(workdir, settings['username'], settings['filename'])

# Print the timestamp and num. of failures and successes at each timestamp
print("\nTimeStamp                Num. of Failures           Num. of Successes")
print("---------------------------------------------------------------------")
for i in range(len(dates)):
    print(dates[i] + "         " + str(response_failures[i]) + "                          " + str(response_successes[i]))
print('')

# Plot the number of failure and success responses over each hourly timestamp
plot(dates, response_failures, response_successes)