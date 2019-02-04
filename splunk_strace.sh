#!/bin/bash

#strace shell script - strace.sh
# $1 is the directory for the logs
# $2 is the timeout for the run of the strace

for x in $(ps aux | grep splunkd | awk '{print $2}')
do timeout $2 strace -fo $1'/strace'_$x.summary.txt -c -p $x
done

for x in $(ps aux | grep splunkd | awk '{print $2}')
do timeout $2 strace -fo $1'/strace'_$x.full.txt -p $x
done

tar -cf $1/strace_outputs.tar $1/*strace*.txt; rm -f $1/*strace*.txt
