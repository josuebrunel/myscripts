##################################################
#
#   Author          : yosuke
#   Filename        : push_ssh_key.sh
#   Description     : Copy a ssh key to a remote host
#   Creation Date   : 25-02-2015
#   Last Modified   : Wed 25 Feb 2015 10:11:51 AM CST
#
##################################################

function push_ssh_key(){
    pub_key="$HOME/.ssh/id_rsa.pub"
    if [ ! -f $pub_key ]; then
        echo -e "I think you should generate a pub_key first. \n \t -> ssh-keygen # if you have no private key \n \t -> ssh-keygen -y -f ~/.ssh/id_rsa > ~/.ssh/id_rsa.pub"
        exit_f
    fi

    if [ ! -z $1 ]; then
        cat $HOME/.ssh/id_rsa.pub | ssh $1 'cat >> $HOME/.ssh/authorized_keys'
        return 0
    else
        echo "You must provided a remote host i.e john@doe"
        exit_f
    fi
}
