#!/bin/bash
iteration=0
while true
do
    ((iteration++))
    echo "<-- $iteration iteration done -->"
    bash /home/rkale2/crawler_script.sh
    sleep 2000
done
