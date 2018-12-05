#!/usr/bin/python

import datetime
import subprocess

now = datetime.datetime.now()
tds = str(now)


def hostname():
    hostname_cmd = "hostname"
    host = subprocess.Popen(hostname_cmd,bufsize=512,shell=True, stderr=subprocess.PIPE, stdout=subprocess.PIPE)
    return_code = host.wait()
    for line in host.stdout:
        h = line.rstrip()
        hostname = str(h)
        hostname = hostname[:16]
    return hostname

def pio(vol):
    cmd = "iostat -mN | grep "+ vol
    pio = subprocess.Popen(cmd,bufsize=512,shell=True, stderr=subprocess.PIPE, stdout=subprocess.PIPE)
    for line in pio.stdout:
         r = line.rstrip()
         r = str(r)
         r = r.split('\n')
         for line in r:
             line = line.split()
             r1 = tds + " hostname=" + str(hostname()) + " volume=" + line[0] + " mbread=" + line[4] + " mbrwrite=" + line[5]
             r2 = tds + " hostname=" + str(hostname()) + " volume=" + line[0] + " tps=" + line[1] + " mbrs=" + line[2] + " mbws=" + line[3]
             print(r1)
	     print(r2)


hostname()

find_vols_cmd = "ls -lth /sys/block/ | grep io | awk '{print $9}'"
find_vols = subprocess.Popen(find_vols_cmd,bufsize=512,shell=True, stderr=subprocess.PIPE, stdout=subprocess.PIPE)
return_code = find_vols.wait()
for line in find_vols.stdout:
    h = line.rstrip()
    vols = str(h)
    pio(vols)
