##################################################
#
#   Author          : josuebrunel
#   Filename        : bootstrap.sh
#   Description     : env installer
#   Creation Date   : 13-05-2015
#   Last Modified   : Wed 13 May 2015 02:05:39 PM CEST
#
##################################################
set -x
cd ~
git clone https://github.com/josuebrunel/myscripts.git .scripts
if [ -f ~/.profile ];then
    mv ~/.profile ~/.profile.bak
fi
ln -s .scripts/profile .profile
source .profile

