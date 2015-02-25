##################################################
#
#   Author          : yosuke
#   Filename        : push_ssh_key.sh
#   Description     : Copy a ssh key to a remote host
#   Creation Date   : 25-02-2015
#   Last Modified   : Wed 25 Feb 2015 07:16:52 AM CST
#
##################################################

function push_ssh_key(){
    if [ ! -z $1 ]; then
        cat .ssh/id_rsa.pub | ssh $1 'cat >> .ssh/authorized_keys'
    else
        echo "You must provided a remote host i.e john@doe"
    fi
}
