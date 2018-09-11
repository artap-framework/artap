#!/bin/bash
file="$1"
class_file="${file%%.*}.class"
/opt/comsol-5.3/bin/comsol compile "${file}"
/opt/comsol-5.3/bin/comsol batch -inputfile "${class_file}"