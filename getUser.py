import os

print('test2: ' + os.getlogin())
print()
print('test1: ' + os.path.expanduser('~'))
print()
print('test3: ' + os.environ.get( 'USERNAME' ))



# TO CALCULATE TIME

from datetime import datetime

# start time
start_time = "2:13:57"
end_time = "11:46:38"

# convert time string to datetime
t1 = datetime.strptime(start_time, "%H:%M:%S")
print('Start time:', t1.time())

t2 = datetime.strptime(end_time, "%H:%M:%S")
print('End time:', t2.time())

# get difference
delta = t2 - t1

# time difference in seconds
print(f"Time difference is {delta.total_seconds()} seconds")

# time difference in milliseconds
ms = delta.total_seconds() * 1000
print(f"Time difference is {ms} milliseconds")


'''
Subtract the end time from the start time
To get the difference between two-time, subtract time1 from time2. A result is a timedelta object. The timedelta represents a duration which is the difference between two-time to the microsecond resolution.

Get time difference in seconds
To get a time difference in seconds, use the timedelta.total_seconds() methods.

Get time difference in milliseconds
Multiply the total seconds by 1000 to get the time difference in milliseconds.

Get time difference in minutes
Divide the seconds by 60 to get the difference in minutes.

Get time difference in hours
Divide the seconds by 3600 to get the final result in hours.
'''