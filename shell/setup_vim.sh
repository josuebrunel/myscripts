##################################################
#
#   Author          : yosuke
#   Filename        : setup_vim.sh
#   Description     : setup vim config
#   Creation Date   : 19-03-2015
#   Last Modified   : Thu 19 Mar 2015 04:48:11 PM CDT
#
##################################################

function setup_vim(){
    today=$(now +'%d-%m-%Y')
    LOG_OUTPUT=$HOME_SCRIPTS/logs/setup_vim-$today.log
    REPOSITORY=https://github.com/josuebrunel/myvim.git

    _debug "===START==="

    cd ~ # go to home directory

    _debug "Cloning ${REPOSITORY} into .vim/ "
    git clone $REPOSITORY .vim

    _debug "Installing vim"
    ln -s .vim/.vimrc .vimrc

    _debug "===END==="
}
