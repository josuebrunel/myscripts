#!/bin/bash

#Script that process each line of a file as you want

function process_file_lines(){
    if [ -z $1 ]; then
        echo -e "Filename required";
        return 1
    fi

    if [ -z $2 ]; then
        echo -e "Command required";
        return 1
    fi

    fname=$1;
    cmds=$2;

    cat $1 | while read line; do $2 $line; done
}
