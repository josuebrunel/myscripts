##################################################
#
#   Author          : josuebrunel
#   Filename        : pypi.sh
#   Description     :
#   Creation Date   : 03-05-2015
#   Last Modified   : Mon 04 May 2015 12:13:16 PM CEST
#
##################################################

function _register_(){
    server=$1
    _info "python setup.py register -r ${server}"
    python setup.py register -r $server
}

function _upload_(){
    server=$1
    _info "python setup.py sdist upload -r ${server}"
    python setup.py sdist upload -r $server
}

function _select_server_(){
    if [ -z $1 ]; then
        _debug "No server provided, using default server : pypitest"
        server=pypitest
    else
        if [ "$1" == "pypitest" ]; then
            _debug "${1} selected"
            server=$1
        else
            _debug "${1} selected"
            server=$1
        fi  
    fi
}

function pypi(){
    now=`date +'%d-%m-%Y'`
    #LOG_OUTPUT=$HOME_SCRIPTS/logs/pypi-$now.log

    action=$1

    case $action in
        "--register"|"-r" )
            _select_server_ $2
            _register_ $server
        ;;
        "--upload"|"-u" )
            _select_server_ $2
            _upload_ $server
        ;;
        *)
            echo -e "Help:  \n \t pypi --register|-r [server]\n \t pypi --publish|-p [server]"
        ;;
    esac 
}


