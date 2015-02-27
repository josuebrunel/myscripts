##################################################
#
#   Author          : josue
#   Filename        : mylogger.sh
#   Description     : custom logger for my shell scripts
#   Creation Date   : 26-02-2015
#   Last Modified   : Fri 27 Feb 2015 07:52:15 AM CST
#
##################################################

## If a LOG_OUTPUT variable is define,
## the logger will write to a file pointed to by the variable

function _log(){
    level=$1
    message=$2
    output=$3

    if [ -z $output ]; then
        logger -s -i -t "[`date +'%Y-%m-%d %H:%M:%S'` ${HOSTNAME} ${USER}][`echo ${level} | tr '[:lower:]' '[:upper:]'`]" -p "user.${level}" "${message}" 2>&1
    else
        logger -s -i -t "[`date +'%y-%m-%d %H:%M:%S'` ${HOSTNAME} ${USER}][`echo ${level} | tr '[:lower:]' '[:upper:]'`]" -p "user.${level}" "${message}" 2>> $output
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

export -f _log
export -f _process
export -f _info
export -f _debug
export -f _warning
export -f _error
export -f _notice
