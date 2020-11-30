# Import needed modules
import string
import datetime
import random
import time
import subprocess
import re


# Declare some needed variables
# time_range = overall time range to be searched
# time_crystals = discrete buckets of time  you want to chunk the search into (extra points for the Star Trek reference!)
time_earliest = 601
time_latest = 1
time_diff = time_earliest-time_latest
time_crystals = 30
num_jobs = time_diff/time_crystals
num_jobs = int(round(num_jobs))
#job_limiter = 3

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

search_job = "index=_internal | table _raw _time | head 1000"
str(search_job)

def run_search(job):
    cmd = "/opt/splunk/bin/./splunk search "+ '"' + job + '"' + " -detach true -preview false -auth scripter:password -output rawdata"
#    cmd = "curl -k -u scripter:password https://18.233.97.196:8089/servicesNS/admin/search/search/jobs/export -d" + " search="+'"'+"search " + search_job + '"'
    print(cmd)
    pio = subprocess.Popen(cmd,bufsize=512,shell=True, stderr=subprocess.PIPE, stdout=subprocess.PIPE)

if __name__ == "__main__":
    for x in range(num_jobs):
        y = time_earliest-time_crystals
        z = time_earliest+time_crystals
        if y < time_earliest:
              y = y-(time_crystals*x)
              z = z-(time_crystals*x)
              job = ("latest=-" + str(y) + "s " + "earliest=-" + str(z) + "s  " + str(search_job))
              run_search(job)
              print("job number " + str(x) + " Runs search: " + str(job))
