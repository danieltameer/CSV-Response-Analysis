# Import required libraries and functions
import pandas as pd
from datetime import datetime, timedelta
import matplotlib.pyplot as plt
from ast import literal_eval

def response_sorting(workdir, user, file):

    # Read CSV file
    authentications = pd.read_csv(f"{workdir}\\{file}")

    # Find the Timestamp column in the CSV
    for i in range(len(authentications.columns)):
        if (authentications.columns[i] == 'Timestamp'):
            timestamp_col_num = i
            break

    # Get the timestamp for each row in the CSV file, convert each timestamp to a string format, and save each string to a list
    timestamps = authentications.iloc[:, timestamp_col_num].astype(str).tolist()

    # Iterate through the list of strings, extract the first 13 characters
    short_timestamps = []
    for i in range(len(timestamps)):
        timestamp = timestamps[i]
        short_timestamp = timestamp[0:13]
        short_timestamps.append(short_timestamp)

    # Remove duplicate items in the list
    short_timestamps = list(set(short_timestamps))

    # Convert the list of date strings to a list of datetime objects
    short_timestamps = [datetime.strptime(date, '%Y-%m-%d %H') for date in short_timestamps]

    # Sort the list of datetime objects
    short_timestamps.sort()

    # Convert the sorted list of datetime objects back to a list of strings
    sorted_short_timestamps = [date.strftime('%Y-%m-%d %H') for date in short_timestamps]

    # Find the Username column in the CSV
    for i in range(len(authentications.columns)):
        if (authentications.columns[i] == 'Username'):
            username_col_num = i
            break

    # Find the Response column in the CSV
    for j in range(len(authentications.columns)):
        if (authentications.columns[j] == 'Response'):
            response_col_num = j
            break

    # Start an empty list to count the number of times each 'Failure' string appears in the CSV
    num_failure_list = []

    # Start an empty list to count the number of times each 'Success' string appears in the CSV
    num_success_list = []

    # Loop through each index in the sorted_short_timestamps list
    for k in range(len(sorted_short_timestamps)):
        ts = sorted_short_timestamps[k]

        fail_counter = 0
        success_counter = 0
        for l in range(len(timestamps)):
            if (ts in timestamps[l]):

                # Check if the username for this timestamp is the correct username to check failures against
                if (authentications.iloc[l, username_col_num] == user):
                    
                    # Check if the response was a failure
                    if (authentications.iloc[l, response_col_num] == "Failure"):
                        fail_counter = fail_counter + 1 # Increment the failure counter by 1
                    
                    # Check if the response was a success
                    elif (authentications.iloc[l, response_col_num] == "Success"):
                        success_counter = success_counter + 1 # Increment the success counter by 1
                    
                    # Check if the response cell is empty or blank
                    else:
                        pass

        num_failure_list.append(fail_counter)
        num_success_list.append(success_counter)

    # Define the format of your date strings
    date_format = "%Y-%m-%d %H"

    # Convert the list of date strings to datetime objects
    dates = [datetime.strptime(date, date_format) for date in sorted_short_timestamps]

    # Determine the range of dates
    start_date = min(dates)
    end_date = max(dates)

    # Create a list of all dates within the range (assuming hourly increments)
    all_dates = []
    current_date = start_date

    i = 0 # Need a counter to iterate through num_failure_list
    response_failures = []

    while current_date <= end_date:
        all_dates.append(current_date)

        # check if current_date is in the original dates list
        # if yes, append the index 'i' from num_failure_list list to num_failure_list_new list
        # if no, append 0 to num_failure_list_new list
        if current_date in dates:

            response_failures.append(num_failure_list[i])
            i += 1 # increment the counter by 1
        else:
            response_failures.append(0)

        current_date += timedelta(hours = 1)  # Adjust the increment if needed (e.g., days, minutes)

    # Loop through and check for successes now
    current_date = start_date

    i = 0 # Need a counter to iterate through num_success_list
    response_successes = []

    while current_date <= end_date:
        if current_date in dates:

            response_successes.append(num_success_list[i])
            i += 1 # increment the counter by 1
        else:
            response_successes.append(0)

        current_date += timedelta(hours = 1)  # Adjust the increment if needed (e.g., days, minutes)

    # Convert the generated datetime objects back to strings
    all_date_strings = [date.strftime(date_format) for date in all_dates]

    # Combine the original dates and the generated dates, and remove duplicates
    combined_dates = sorted(set(all_date_strings + sorted_short_timestamps))

    # Iterate through the list and append characters ":00" for the hours
    for i in range(len(combined_dates)):
        combined_dates[i] += ":00"

    return combined_dates, response_failures, response_successes

def plot(x_values, y1_values, y2_values):

    # Set the size of the plot with a white background
    plt.figure(figsize=(20,10))

    # Plot the failure data with markers
    plt.plot(x_values, y1_values, '--', color='red', label='Failures')

    # Plot the success data with markers
    plt.plot(x_values, y2_values, ':', color='green', label='Successes')  

    # Add labels and title
    plt.xlabel("Timestamp", color = "black")
    plt.ylabel("Number of Responses", color = "black")
    plt.title("Responses vs. Time", color = "black")

    # Function add a legend
    plt.legend(["Failures", "Successes"], loc="upper right")

    # Rotate x-axis labels to be vertical
    plt.xticks(rotation = 45, fontsize = 8)  

    # Set the color of the ticks on the x and y axes
    plt.tick_params(axis='x')
    plt.tick_params(axis='y')

    # Optional: Add grid lines
    plt.grid(True)
    
    # Display the plot
    plt.show()

    return

def read_txt(filename):
    settings = {}
    with open(filename,'r') as file:
        for line in file:
            # if line[0] == '#' or line[0] == '\n':
            #     pass
            # else:
            line = line[:-1] #assuming each read variable has '/n' after it
            ind = line.find('=')
            settings[line[0:ind-1]] = literal_eval(line[(ind+2):])
        file.close()
    return settings