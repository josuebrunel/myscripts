##################################################
#
#   Author          : yosuke
#   Filename        : function_loader.sh
#   Description     : load function and register them in /usr/local/bin
#   Creation Date   : 26-02-2015
#   Last Modified   : Thu 26 Feb 2015 07:16:07 AM CST
#
##################################################

LOG_OUTPUT=$HOME_SCRIPTS/logs/function_loader.log
LOCAL_BIN=/usr/local/bin/

function function_loader(){
    func=$1

    if [ -z $func ]; then
        _error "No function provided"
        echo -e "A function name must be provided"
        return 1
    fi

    if [ ! -e $LOCAL_BIN/$func ]; then
        ln -s "${HOME_SCRIPTS}/${func}.sh" "${LOCAL_BIN}/${func}"
    fi  
}
