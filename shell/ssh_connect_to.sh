##################################################
#
#   Author          : josuebrunel
#   Filename        : ssh_connect_to.sh
#   Description     :
#   Creation Date   : 11-04-2015
#   Last Modified   : Tue Jul 21 20:30:49 2015
#
##################################################


function ssh_connect_to(){
    host=$1
    unset r_host
    cfg_file="$HOME_SCRIPTS/cfg/ssh.txt"
    if [ ! -f $cfg_file ]; then
        _warning "File ${cfg_file} doesn't exist yet"
        return 1
    fi

    while read -r line || [[ -n $line ]]; do
       
        if [[ $host == `echo $line | cut -f 1 -d ' '` ]]; then
            r_host=`echo $line | cut -f 2 -d ' '`
            _info "Macth found"
            break
        fi       
    done < "$HOME_SCRIPTS/cfg/ssh.txt"
    
    if [ -z $r_host ]; then
        _info "No macth found for ${host}"
        return 0
    fi
    _info "Connecting to ${r_host}"
    bash -c "ssh ${r_host}"
}

function ssh_list_hosts(){
    ssh_file=$HOME_SCRIPTS/cfg/ssh.txt
    if [ ! -f  $ssh_file ]; then
        _info "No ${ssh_file} file found"
    else
        cat $ssh_file
    fi
}

export -f ssh_connect_to
export -f ssh_list_hosts
