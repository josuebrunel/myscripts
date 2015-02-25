##################################################
#
#   Author          : josue
#   Filename        : mylogger.sh
#   Description     : custom logger for my shell scripts
#   Creation Date   : 26-02-2015
#   Last Modified   : Thu Feb 26 00:56:49 2015
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
    _log "debug" $1 $LOG_OUTPUT
}

function _info(){
    _log "info" $1 $LOG_OUTPUT
}

function _warning(){
    _log "warning" $1 $LOG_OUTPUT
}

function _error(){
    _log "error" $1 $LOG_OUTPUT
}

