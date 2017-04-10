#!/bin/bash

function harakiri(){
    if [ -z $1 ]; then
        echo -e "A process name is required"
        return 1
    fi

    process_name=$1

    if pgrep $process_name; xargs kill -9; then
        _info "$process_name properly terminated"
    else
        _error "Something went wrong"
        return 1
    fi
}
