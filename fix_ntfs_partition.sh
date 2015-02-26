##################################################
#
#   Author          : josue
#   Filename        : fix_ntfs_partition.sh
#   Description     : fixes ntfs partition
#   Creation Date   : 26-02-2015
#   Last Modified   : Thu Feb 26 09:34:25 2015
#
##################################################

function fix_ntfs_partition(){
    
    LOG_OUTPUT=$HOME_SCRIPTS/logs/fix_ntfs_partition.log

    if [ -z $1 ]; then
        echo -e 'At least a partition must be provided'
        _info 'At least a partition must be provided'
        return 1
    fi    

    if [ ! -f $1 ]; then
        echo -e "${1} is not a valid partition"
        exit_f
    fi

    sudo fsck_ufsd_NTFS -n $1
}
