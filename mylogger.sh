##################################################
#
#   Author          : josue
#   Filename        : mylogger.sh
#   Description     : custom logger for my shell scripts
#   Creation Date   : 26-02-2015
#   Last Modified   : Thu Feb 26 01:04:55 2015
#
##################################################

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

function _debug(){
    if [ ! -z $1 ]; then
        _log "debug" $1 $LOG_OUTPUT
    else
        echo -e "A message must be provided i.e _debug 'my message'"
    fi
}

function _info(){
    if [ ! -z $1 ]; then
        _log "info" $1 $LOG_OUTPUT
    else
        echo -e "A message must be provided i.e _info 'my message'"
    fi
}

function _warning(){
    if [ ! -z $1 ]; then
        _log "warning" $1 $LOG_OUTPUT
    else
        echo -e "A message must be provided i.e :  _warning 'my message'"
    fi
}

function _error(){
    if [ ! -z $1 ]; then
        _log "error" $1 $LOG_OUTPUT
    else
        echo -e "A message must be provided i.e : _error 'my message'"
    fi
}

