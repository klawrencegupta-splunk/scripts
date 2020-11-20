# Import needed modules
import string
import datetime
import random
import time
import re


# Declare some needed variables
# time_range = overall time range to be searched
# time_crystals = discrete buckets of time  you want to chunk the search into (extra points for the Star Trek reference!)
time_earliest = 86400
time_latest = 43200
time_diff = time_earliest-time_latest
time_crystals = 900
num_jobs = time_diff/time_crystals
num_jobs = int(round(num_jobs))

print("Earliest in seconds")
print(time_earliest)
print("Latest in seconds")
print(time_latest)
print("Diff in seconds")
print(time_diff)
print("Time buckets")
print(time_crystals)
print("Final number of jobs")
print(num_jobs)

search_job = "index=_internal | stats count"
str(search_job)

for x in range(num_jobs):
    y = time_earliest-time_crystals
    z = time_earliest+time_crystals
    if y < time_earliest:
       y = y-(time_crystals*x)
       z = z-(time_crystals*x)
       print("job number " + str(x) + " Runs search:  latest=-" + str(y) + "s " + "earliest=-" + str(z) + "s   " + str(search_job))