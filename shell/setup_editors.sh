##################################################
#
#   Author          : yosuke
#   Filename        : setup_vim.sh
#   Description     : setup vim config
#   Creation Date   : 19-03-2015
#   Last Modified   : Fri 20 Mar 2015 08:11:44 AM CDT
#
##################################################

function setup_editor(){

    today=$(date +"%d-%m-%Y")
    #LOG_OUTPUT=$HOME_SCRIPTS/logs/setup_vim-$today.log

    if [ -z $1 ]; then
        echo -e "An editor name is required i.e vim or emacs"
        _info "Editor name not provided"
        return 1
    fi
    echo -e $1
    if [ $1 != "emacs" ] && [ $1 != "vim" ]; then
        echo -e "Only emacs and vim are accepted as editor name"
        _error "Invalid editor name : ${1}"
        return 1
    fi
    _debug "Valid editor name : $1" 
    REPOSITORY=https://github.com/josuebrunel/my$1.git
    editor="$1"

    if [ $editor == "emacs"]; then
        dir='.emacs.d/'
        file='.emacs'
    else
        dir='.vim/'
        file='.vimrc'
    fi

    _debug "Editor ${editor} will be set up in ${dir}"

    _debug "===START==="

    cd $HOME # go to home directory

    _debug "Cloning ${REPOSITORY} into ${dir} "
    #git clone $REPOSITORY $dir

    _debug "Installing vim"
    #ln -s "${dir}/{$vim}" $file
    cd -
    _debug "===END==="
}
