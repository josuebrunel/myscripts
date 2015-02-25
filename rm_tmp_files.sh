#!/bin/bash

##################################################
#
#   Author          : yosuke
#   Filename        : rm_tmp_files.sh
#   Description     : Remove ~, .pyc recursively 
#   Creation Date   : 25-02-2015
#   Last Modified   : Wed 25 Feb 2015 09:25:59 AM CST
#
##################################################

function help(){
    echo -e  "help: \n \t john@doe$> rm_tmp_files /home/john/projects/ *.pyc"
    kill -INT $$
}

function rm_tmp_files(){
   
    if [ "$1" == "-h" ] || [ "$1" == "--help" ]; then
        help
    fi

    if [ $# -eq 2 ]; then
        dir=$1
        type=$2
    elif [ $# -eq 1 ]; then
        echo -e "No directory provided. The current directory will be used"
        dir='.'
        type=$1
    elif [ $# -gt 2 ];then
        echo -e "Don't be a fool. There's no such thing as a third argument"
    else
        echo -e "A type in required though"
        help
        kill -INT $$
    fi

    echo "find $dir -name $type | xargs ls -l"
    find $dir -name $type | xargs ls -l

}

rm_tmp_files $1 $2

