##################################################
#
#   Author          : josuebrunel
#   Filename        : date.sh
#   Description     :
#   Creation Date   : 12-08-2015
#   Last Modified   : Wed 12 Aug 2015 12:02:44 PM CEST
#
##################################################

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

export -f get_date
export -f get_time
export -f get_datetime
