#Colored Terminal
export CLICOLOR=1
export LSCOLORS=GxFxCxDxBxegedabagaced

export TERM="xterm-color"
PS1='\[\e[0;33m\]\u\[\e[0m\]@\[\e[0;32m\]\h\[\e[0m\]:\[\e[0;34m\]\w\[\e[0m\]\$'

# SUDO AUTOCOMPLETE
complete -cf sudo

#MY PYTHON ENVIRONMENT
export PYTHONSTARTUP=$HOME/.pythonenv.py

#VARIABLES
export HOME_SCRIPTS=$HOME/.scripts/

## COMMON LS
alias ll='ls -lht'
alias la='ls -lhAt'
alias lt='ls -lht'
alias ld='du -sh ./*/'

## FILE COMPRESSION
alias ltar='tar tzvf'
alias ctar='tar czvf'
alias xtar='tar xzvf'

alias reload='source $HOME/.profile'
alias goto_workspace='cd $HOME/workspace'

# GZIP & XZ COMPRESSION LEVEL
export GZIP=-9
export XZ_OPT=-9

#LOCALES
export LC_ALL=en_US.UTF-8
export LANG=en_US.UTF-8

## LOADS SCRIPTS
source $HOME/.scripts/exit_f.sh
source $HOME/.scripts/push_ssh_key.sh
source $HOME/.scripts/rm_tmp_files.sh
source $HOME/.scripts/archive.sh
source $HOME/.scripts/mylogger.sh
source $HOME/.scripts/fix_ntfs_partition.sh

## OSX SPECIAL
if [ `uname -s` == "Darwin" ]; then
    #MY ALIASES
    alias umount_toshiba='sudo umount /VOLUMES/TOSHIBA/'
    alias goto_toshiba='cd /Volumes/TOSHIBA/'
    alias goto_macext='cd /Volumes/MacintoshEX/'
    alias disklist='diskutil list'

    alias emax='/Applications/Emacs.app/Contents/MacOS/Emacs -nw'
    alias show_hidden_files='defaults write com.apple.finder AppleShowAllFiles YES; killall Finder /System/Library/CoreServices/Finder.app'
    alias hide_hidden_files='defaults write com.apple.finder AppleShowAllFiles NO; killall Finder /System/Library/CoreServices/Finder.app'

    #VIRTUAL ENVS
    source /usr/local/bin/virtualenvwrapper.sh

    #MYSQL CONFIG
    export PATH=$PATH:/usr/local/mysql/bin
    export DYLD_LIBRARY_PATH=/usr/local/mysql/lib
    
    ##
    # Your previous /Users/josue/.profile file was backed up as /Users/josue/.profile.macports-saved_2014-11-08_at_12:21:31
    ##

    # MacPorts Installer addition on 2014-11-08_at_12:21:31: adding an appropriate PATH variable for use with MacPorts.
    export PATH="/opt/local/bin:/opt/local/sbin:$PATH"
    # Finished adapting your PATH environment variable for use with MacPorts.

    export PATH="$PATH:$HOME/.rvm/bin" # Add RVM to PATH for scripting

    [[ -s "$HOME/.rvm/scripts/rvm" ]] && source "$HOME/.rvm/scripts/rvm" # Load RVM into a shell session *as a function*   
fi


