##################################################
#
#   Author          : josue
#   Filename        : mylogger.sh
#   Description     : custom logger for my shell scripts
#   Creation Date   : 26-02-2015
#   Last Modified   : Thu Feb 26 00:50:23 2015
#
##################################################

function _log(){
    priority=$1
    message=$2
    output=$3

    if [ -z $output ]; then
        logger -s -p "local7.${priority}" "${message}" 2>&1
    else
        logger -s -p "local7.${priority}" "${message}" 2>> $output 
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

