from datetime import datetime


# Define the start time as a string
start_time_utc_str = "13:59"

# Calculate the difference between the start time and the current time
time_difference = datetime.strptime(start_time_utc_str, "%H:%M") - datetime.strptime(datetime.now().strftime("%H:%M"), "%H:%M")

# Format the time difference as a string in "%H:%M" format
time_difference_str = "{:02d}:{:02d}".format(time_difference.seconds // 3600, (time_difference.seconds % 3600) // 60)

print("Difference in time:", time_difference_str)
