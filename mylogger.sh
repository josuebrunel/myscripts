##################################################
#
#   Author          : josue
#   Filename        : mylogger.sh
#   Description     : custom logger for my shell scripts
#   Creation Date   : 26-02-2015
#   Last Modified   : Thu 26 Feb 2015 09:53:52 AM CST
#
##################################################

## If a LOG_OUTPUT variable is define,
## the logger will write to a file pointed to by the variable

function _log(){
    level=$1
    message=$2
    output=$3

    if [ -z $output ]; then
        logger -s -p "local7.${level}" "${message}" 2>&1
    else
        logger -s -p "local7.${level}" "${message}" 2>> $output 
    fi
}

function _process(){
    level=$1
    message=$2

    if [ ! "${message}" == "" ]; then
        _log "${level}" "${message}" $LOG_OUTPUT
    else
        echo -e "A message must be provided i.e : _${level} 'your message'"
    fi
}

function _info(){
    _process "info" "$1"
}

function _debug(){
    _process "debug" "$1"
}

function _warning(){
    _process "warning" "$1"
}

function _error(){
    _process "error" "$1"
}

function _notice(){
    _process "notice" "$1"
}
