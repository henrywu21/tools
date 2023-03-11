#!/bin/bash

#ps -e|grep $1 | awk '{print $1}' | xargs kill
ps -e|grep [c]hromedriver | awk '{print $1}' | xargs kill
ps -e|grep [g]eckodriver | awk '{print $1}' | xargs kill
