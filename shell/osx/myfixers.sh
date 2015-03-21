##################################################
#
#   Author          : josue
#   Filename        : myfixers.sh
#   Description     : fixes OSX issues
#   Creation Date   : 26-02-2015
#   Last Modified   : Sat Mar 21 15:36:09 2015
#
##################################################



function __fix_item_is_used_by_osx__(){
    _debug "${0}"
    if [ -z $1 ] || [ ! -d $1 ]; then
        echo -e "A directoy is required"
        _info "A directory or file is required"
        return 1
    fi
    dir=$1
    for file in `find $dir -type f`; do
        if [ -f $file ]; then
            if SetFile -c "" -t "" "${file}" ; then
                _info "$file is fixed"
            else    
                _error "Can't process file : ${file}"
            fi
        fi
    done
}

function __is_mounted__(){
    _debug "Is disk $1 mounted ?"
    if diskutil info $1 | grep 'Mount Point' ; then
        _debug "Yes"
        return 0
    fi
    _debug "Nope"
    return 1
}

function __fix_ntfs_partition__(){
    if [ -z $1 ]; then
        echo -e 'A volume or disk is required'
        _info 'A volume or disk is required'
        return 1
    fi   

    if  __is_mounted__ $1 ; then
        _debug "Unmounting $1"
        sudo diskutil unmount $1
    fi

    _debug "Fixing $1"
    sudo fsck_ufsd_NTFS -y $1
    _debug "Done fixing $1"
}

function _help(){
    _debug "{0}"
    message=$1

    if [ ! -z $message ]; then
        echo -e "${message}"
    fi
    echo -e "Help \n \t --ntfs/-n /dev/diskname i.e disks3s1  \n \t --brokM/-b dirname" 
    return 1
}

function fixers(){
    
    LOG_OUTPUT=$HOME_SCRIPTS/logs/myfixers-$(date +'%Y-%m-%d').log

    _info "START"
    if [ -z $1 ]; then
        _help
        return 1
    fi

    case $1 in
        "--help" | "-h")
            _help
        ;;
        "--ntfs" | "-n")
            __fix_ntfs_partition__ $2
        ;;
        "--brokM" | "-b")
            __fix_item_is_used_by_osx__ $2
        ;;
        *) 
            _help
    esac
    _info "END"
    echo -e "LOGS  ===>>  ${LOG_OUTPUT}"
}
