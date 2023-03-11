#!/bin/bash

while true
do
    echo $@
    $@
    if [[ $? != 0 ]]; then exit; fi
    echo "Press [CTRL+C] to stop.."
    sleep 10;
done
