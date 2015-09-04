##################################################
#
#   Author          : josuebrunel
#   Filename        : bootstrap.sh
#   Description     : env installer
#   Creation Date   : 13-05-2015
#   Last Modified   : Fri 04 Sep 2015 11:15:16 AM CEST
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

for f in profile pypirc irbrc gitconfig; do
    setup $f
done

source .profile

