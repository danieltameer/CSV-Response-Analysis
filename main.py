# Import required libraries and functions
import os
from Functions_Library import plot, response_sorting, read_txt

# Get current working directory
workdir = os.getcwd()

# Get settings file name
file = workdir + "\\Settings.txt"

# Read settings file and get username and CSV file name
settings = read_txt(file)

# Print message stating username and CSV file name
print(f"Username: {settings['username']}")
print(f"CSV file: {settings['filename']}")
print(f"Analyzing...")

# Sort the responses chronologically and determine the number
# of failures at each hourly timestamp within the CSV file
dates, responses = response_sorting(workdir, settings["username"], settings["filename"])

# Print the timestamp and num. of failures at each timestamp
print("\nTimeStamp                Num. of Failures")
print("-----------------------------------------")
for i in range(len(dates)):
    print(dates[i] + "         " + str(responses[i]))

# Plot the number of failure responses over each hourly timestamp
plot(dates, responses)