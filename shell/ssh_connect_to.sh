##################################################
#
#   Author          : josuebrunel
#   Filename        : ssh_connect_to.sh
#   Description     :
#   Creation Date   : 11-04-2015
#   Last Modified   : Sat Apr 11 16:11:05 2015
#
##################################################


function ssh_connect_to(){
    host=$1
    unset r_host
    while read -r line || [[ -n $line ]]; do
       
        if [[ $host == `echo $line | cut -f 1 -d ' '` ]]; then
            r_host=`echo $line | cut -f 2 -d ' '`
            _info "Macth found"
            break
        fi       
    done < "$HOME_SCRIPTS/cfg/ssh.txt"
    
    if [ -z $r_host ]; then
        _info "No macth found"
        return 0
    fi
    _info "Connecting to ${r_host}"
    bash -c "ssh ${r_host}"
}

export -f ssh_connect_to
