#!/bin/bash
usage() {
    echo "Usage: $0 <output_dir> <sid>"
    exit -1
}

SAMPLES=600
SAMPLE_PERIOD=1
i=1

# store arguments in a special array
args=("$@")
OUTPUT_DIR=$1
search=$2
if [ -z "$OUTPUT_DIR" ]
then
    usage
fi

if [ -z "$search" ]; then
    usage
fi

#echo "search --id=$search"
while [ $i -lt $SAMPLES ]; do
    for j in `ps -ef | grep "[s]earch --id=$search" | awk '{print $2}'`;do
        if [ $j -gt 0 ]; then
            echo "search --id=$search"
            echo "pstack search --id=$search $j"
            pstack $j > $OUTPUT_DIR/pstack_splunkd-$j-$i-`date +%s`.out
        fi
    done
    let "i+=1"
    sleep $SAMPLE_PERIOD
done
