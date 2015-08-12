##################################################
#
#   Author          : josuebrunel
#   Filename        : date.sh
#   Description     :
#   Creation Date   : 12-08-2015
#   Last Modified   : Wed 12 Aug 2015 01:56:18 PM CEST
#
##################################################

function operation_help(){
    echo -e "USAGE:"
    echo -e "\tfunction '<number> <[minutes,hours,days,weeks,months,years]>'"
    echo -e "Examples:"
    echo -e "\tdate_add '10 weeks'"
    echo -e "\tdate_minus '10 days'"
}

function get_date(){
    today=`date +"%Y-%m-%d"`
    echo $today
}

function get_time(){
    current_time=`date +"%H:%M:%S"`
    echo $current_time
}

function get_datetime(){
    datetime=`date +"%Y-%m-%d %H:%M:%S"`
    echo $datetime
}

function date_plus(){
    if [ ! -z "$1" ]; then
        today=`date -d "+${1}"`
    else
        operation_help
    fi
    echo $today
}

function date_minus(){
    if [ ! -z "$1" ]; then
        today=`date -d "-${1}"`
    else
        operation_help
    fi
    echo $today
}

export -f get_date
export -f get_time
export -f get_datetime
export -f date_plus
export -f date_minus
