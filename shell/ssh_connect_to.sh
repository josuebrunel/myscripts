##################################################
#
#   Author          : josuebrunel
#   Filename        : ssh_connect_to.sh
#   Description     :
#   Creation Date   : 11-04-2015
#   Last Modified   : Sat Apr 11 05:49:15 2015
#
##################################################


function ssh-connect-to(){
    host=$1

    while read -r line || [[ -n $line ]]; do
        r_hostname=`echo $line | cut -f 1 -d ' '`
        r_host=`echo $line | cut -f 2 -d ' '`
        if [[ $host == $r_hostname ]]; then
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

export -f ssh-connect-to
