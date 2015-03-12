##################################################
#
#   Author          : josue
#   Filename        : myfixers.sh
#   Description     : fixes OSX issues
#   Creation Date   : 26-02-2015
#   Last Modified   : Thu 12 Mar 2015 05:50:26 AM CDT
#
##################################################


LOG_OUTPUT=$HOME_SCRIPTS/logs/myfixers.log

function __fix_item_is_used_by_osx__(){
    if [ -z $1 ] || [ ! -d $1 ]; then
        echo -e "A directoy is required"
        _info "A directory or file is required"
        return 1
    fi
    
}

function __fix_ntfs_partition__(){
    

    if [ -z $1 ]; then
        echo -e 'At least a partition must be provided'
        _info 'At least a partition must be provided'
        return 1
    fi    

    if [ ! -f $1 ]; then
        echo -e "${1} is not a valid partition"
        _error "${1} is not a valid partition"
        return 1
    fi

    sudo fsck_ufsd_NTFS -y $1
}

function _help(){
    message=$1

    if [ ! -z $message ]; then
        echo -e "${message}"
    fi
    echo -e "Help \n \t --ntfs/-n /dev/diskname i.e disks3s1  \n \t --brokM/b dirname" 
    return 1
}

function myfixers(){
    
    if [ -z $1 ]; then
        _help
        return 1
    fi

    case in $1
        "--ntfs" | "-n")
            __fix_ntfs_partition__
        ;;
        "--brokM" | "-b")
            __fix_item_is_used_by_osx__
        ;;
        *) 
            _help

}
