##################################################
#
#   Author          : josue
#   Filename        : mylogger.sh
#   Description     : custom logger for my shell scripts
#   Creation Date   : 26-02-2015
#   Last Modified   : Sat Mar 21 20:54:25 2015
#
##################################################

## If a LOG_OUTPUT variable is defined,
## the logger will write to a file pointed to by the variable

function __log__(){
    level=$1
    message=$2
    output=$3

    if [ -z $output ]; then
        if [ `uname -s` != "Darwin" ]; then
            logger -s -i -t "[`date +'%Y-%m-%d %H:%M:%S'` ${HOSTNAME} ${USER}][`echo ${level} | tr '[:lower:]' '[:upper:]'`]" -p "user.${level}" "${message}" 2>&1
        else
            logger -s -p "user.${level}" "${message}" 2>&1
        fi
     else
         if [ `uname -s` != "Darwin" ]; then
            logger -s -i -t "[`date +'%Y-%m-%d %H:%M:%S'` ${HOSTNAME} ${USER}][`echo ${level} | tr '[:lower:]' '[:upper:]'`]" -p "user.${level}" "${message}" 2>> $output
        else
            logger -s -p "user.${level}" "${message}" 2>> $output
        fi
    fi
}

function __process__(){
    level=$1
    message=$2
    
    #Creating LOG folder when it doesn't exist
    if [ ! -d $LOG_OUTPUT ]; then
        mkdir -p $HOME_SCRIPTS/logs
    fi

    if [ ! "${message}" == "" ]; then
        __log__ "${level}" "${message}" $LOG_OUTPUT
        #unset LOG_OUTPUT # Unsetting variable
    else
        echo -e "A message must be provided i.e : _${level} 'your message'"
    fi
}

function _info(){
    __process__ "info" "$1"
}

function _debug(){
    __process__ "debug" "$1"
}

function _warning(){
    __process__ "warning" "$1"
}

function _error(){
    __process__ "error" "$1"
}

function _notice(){
    __process__ "notice" "$1"
}

export -f __log__
export -f __process__
export -f _info
export -f _debug
export -f _warning
export -f _error
export -f _notice
