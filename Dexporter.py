#!/usr/bin/env python3
import configparser
import os
import sys
from time import sleep
import splunklib.client as client
from splunklib.binding import AuthenticationError
import progressbar


def run():
    dir_name = os.path.dirname(os.path.abspath(__file__))
    with open(os.path.join(dir_name, "config.conf"), "r") as f:
        config = configparser.RawConfigParser()
        config.read_file(f)
    try:
        hostname = config.get("options", "hostname")
        username = config.get("options", "username")
        password = config.get("options", "password")
        search_string = config.get("options", "search_string")
        earliest_time = config.get("options", "earliest_time")
        latest_time = config.get("options", "latest_time")
    except configparser.NoOptionError:
        sys.exit("Error in configuration file.")

    if '' in (hostname, username, password, search_string, earliest_time, latest_time):
        sys.exit("Error: missing config.conf value")
    try:
        service = client.connect(host=hostname, port=8089, username=username, password=password)
        print(service)
    except AuthenticationError:
        sys.exit("Error: incorrect credentials")
    print("Successfully connected to Splunk")
    jobs = service.jobs
    kwargs = {"exec_mode": "normal",
                             "earliest_time": earliest_time,
                             "latest_time": latest_time}
    print("Running search")
    job = jobs.create("search " + search_string, **kwargs)
    print("Search job created with SID %s" % job.sid)

    # Progress bar fanciness
    widgets = [progressbar.Percentage(), progressbar.Bar()]
    #bar = progressbar.ProgressBar(widgets=widgets, max_value=1000).start()
    bar = progressbar.ProgressBar(widgets=widgets).start()

    # Wait for job to complete
    while True:
        while not job.is_ready():
            pass
        if job["isDone"] == "1":
            bar.finish()
            print("\nJob completed")
            break
        else:
            progress_percent = round(float(job["doneProgress"])*100, 1)
            bar.update(int(progress_percent*10))
        sleep(2)


    event_count = int(job["eventCount"])
    print("\nDownloading and writing results to file")
    # Progress bar fanciness round 2
    i = 0

    widgets = [progressbar.Percentage(), progressbar.Bar()]
    #bar = progressbar.ProgressBar(widgets=widgets, max_value=(event_count-1)).start()
    bar = progressbar.ProgressBar(widgets=widgets).start()

    # Read results and write to file

    with open(os.path.join(dir_name, "output.csv"), "wb") as out_f:
        while i < event_count:
            try: 
                job_results = job.results(output_mode="csv", count=1000, offset=i)
            except AuthenticationError: 
                print("Session timed out. Reauthenticating")
                service = client.connect(host=hostname, port=8089, username=username, password=password)
                job_results = job.results(output_mode="csv", count=1000, offset=i)
            for result in job_results:
                out_f.write(result)
            #bar.update(i + 1)
            i += 1000
    bar.finish()
    print("\nDone!")


if __name__ == "__main__":
    run()
