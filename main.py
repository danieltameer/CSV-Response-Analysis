# Import required functions
from Functions_Library import open_gui, response_sorting, plot

# Get the username and CSV file path through the GUI
username, file_path = open_gui()

# Print message stating username and CSV file name
print(f"Username: {username}")
print(f"CSV File: {file_path}")
print(f"Analyzing...")

# Sort the responses chronologically and determine the number of failure and success responses at each hourly timestamp in the CSV file
dates, response_failures, response_successes = response_sorting(file_path, username)

# Print the timestamp and num. of failures and successes at each timestamp
print("\nTimeStamp                Num. of Failures           Num. of Successes")
print("---------------------------------------------------------------------")
for i in range(len(dates)):
    print(dates[i] + "         " + str(response_failures[i]) + "                          " + str(response_successes[i]))
print('')

# Plot the number of failure and success responses over each hourly timestamp
plot(dates, response_failures, response_successes)