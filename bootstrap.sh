##################################################
#
#   Author          : josuebrunel
#   Filename        : bootstrap.sh
#   Description     : env installer
#   Creation Date   : 13-05-2015
#   Last Modified   : Thu 28 May 2015 07:40:15 AM CEST
#
##################################################
set -x
cd ~
git clone https://github.com/josuebrunel/myscripts.git ~/.scripts

# if .profile already exists
if [ -f ~/.profile ];then
    mv ~/.profile ~/.profile.bak
fi
ln -s ~/.scripts/profile ~/.profile

# if .gitconfig already exists
if [ -f ~/.profile ];then
    mv ~/.gitconfig ~/.gitconfig.bak
fi
ln -s ~/.scripts/gitconfig ~/.gitconfig 

source .profile

