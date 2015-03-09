##################################################
#
#   Author          : yosuke
#   Filename        : exit_f.sh
#   Description     : simulate an exit() function
#   Creation Date   : 25-02-2015
#   Last Modified   : Wed 25 Feb 2015 09:48:43 AM CST
#
##################################################

function exit_f(){
    kill -INT $$
}
