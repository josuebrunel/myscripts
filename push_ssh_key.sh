##################################################
#
#   Author          : yosuke
#   Filename        : push_ssh_key.sh
#   Description     : Copy a ssh key to a remote host
#   Creation Date   : 25-02-2015
#   Last Modified   : Thu 26 Feb 2015 10:08:59 AM CST
#
##################################################


function push_ssh_key(){
    LOG_OUTPUT=$HOME_SCRIPTS/logs/push_ssh_key.log
    _debug "START push_ssh_key"
    pub_key="$HOME/.ssh/id_rsa.pub"
    if [ ! -f $pub_key ]; then
        echo -e "I think you should generate a pub_key first. \n \t -> ssh-keygen # if you have no private key \n \t -> ssh-keygen -y -f ~/.ssh/id_rsa > ~/.ssh/id_rsa.pub"
        _error "No pub key found for user $USER"
        return 1
    fi

    if [ ! -z $1 ]; then
        if  ! cat $HOME/.ssh/id_rsa.pub | ssh $1 'cat >> $HOME/.ssh/authorized_keys' ; then
            _error "${1} information aren't valid"
        fi
    else
        echo "You must provided a remote host i.e john@doe"
        _info "You must provided a remote host i.e john@doe"
        return 1
    fi
    _debug "END push_ssh_key"
    return 0
}
