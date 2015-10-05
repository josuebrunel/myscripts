##################################################
#
#   Author          : josuebrunel
#   Filename        : bootstrap.sh
#   Description     : env installer
#   Creation Date   : 13-05-2015
#   Last Modified   : Mon 05 Oct 2015 11:43:28 AM CEST
#
##################################################
set -x
cd ~
git clone https://github.com/josuebrunel/myscripts.git ~/.scripts

function setup {
    filename=$1

    if [ -f ~/.$filename ]; then
        mv ~/.$filename ~/.$filename.bak
    fi

    ln -s ~/.scripts/$filename ~/.$filename 
}

for f in profile pypirc irbrc gitconfig sqliterc; do
    setup $f
done

source $HOME/.profile

