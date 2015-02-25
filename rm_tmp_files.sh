##################################################
#
#   Author          : yosuke
#   Filename        : rm_tmp_files.sh
#   Description     : Remove ~, .pyc recursively 
#   Creation Date   : 25-02-2015
#   Last Modified   : Wed 25 Feb 2015 07:51:50 AM CST
#
##################################################

function rm_tmp_files(){
    dir=$1
    type=$2

    if [ "$1" == "-h" ] || [ "$1" == "--help" ]; then
        echo -e  "help: \n \t john@doe$> rm_tmp_files /home/john/projects/ *.pyc"
        kill -INT $$
    fi

    if [ -Z $dir ]; then
        echo -e "No directory provided. The current directory will be used"
        dir='.'
    fi

    if [ -Z $type ]; then
        echo -e "No type provided. ~ will be used"
        type='*~'
    fi

    find $dir -name $type | ls -l

}

rm_tmp_files $1 $2
