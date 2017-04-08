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

for f in profile pypirc irbrc gitconfig gitignore sqliterc; do
    setup $f
done

# set python project manager binary
ln -s ~/.scripts/bin/py_project_manager.py ~/.local/bin/py-project-manager

source $HOME/.profile
