#Colored Terminal
export CLICOLOR=1
export LSCOLORS=GxFxCxDxBxegedabagaced

export TERM="xterm-color"
PS1='\[\e[0;33m\]\u\[\e[0m\]%\[\e[0;32m\]\h\[\e[0m\]:\[\e[0;34m\]\w\[\e[0m\]\$'

# SUDO AUTOCOMPLETE
complete -cf sudo

#VARIABLES
export HOME_SCRIPTS=$HOME/.scripts


# GZIP & XZ COMPRESSION LEVEL
export GZIP=-9
export XZ_OPT=-9

#LOCALES
export LC_ALL=en_US.UTF-8
export LANG=en_US.UTF-8

#MY PYTHON ENVIRONMENT
export PYTHONSTARTUP=$HOME_SCRIPTS/python/__init__.py

#GOPATH
export GOPATH=$HOME/workspace/go
export PATH=$PATH:/usr/local/go/bin

# LOCAL BINARY PATH
export PATH=$PATH:$HOME/.local/bin

## LOADS SCRIPTS
# source $HOME_SCRIPTS/osx
source $HOME_SCRIPTS/aliases
source $HOME_SCRIPTS/shell/exit_f.sh
source $HOME_SCRIPTS/shell/ssh_push_key.sh
source $HOME_SCRIPTS/shell/archive.sh
source $HOME_SCRIPTS/shell/mylogger.sh
source $HOME_SCRIPTS/shell/setup_editors.sh
source $HOME_SCRIPTS/shell/ssh_connect_to.sh
source $HOME_SCRIPTS/shell/pypi.sh
source $HOME_SCRIPTS/shell/git-completion.bash
source $HOME_SCRIPTS/shell/date.sh
source $HOME_SCRIPTS/shell/harakiri.sh
source $HOME_SCRIPTS/shell/process_line_as.sh

## HISTORY SETTINGS
if [ `uname -s` == "Linux" ]; then
    export HISTCONTROL=ignoredups:erasedups  # no duplicate entries
    export HISTSIZE=-1                   # big big history
    export HISTFILESIZE=-1               # big big history
    export HISTTIMEFORMAT="%d/%m/%y %T " # hist timestamp
    shopt -s histappend                      # append to history, don't overwrite it
    #Save and reload the history after each command finishes
    export PROMPT_COMMAND="history -a; history -c; history -r; $PROMPT_COMMAND"
fi

export ANDROID_SD=/storage/extSdCard/
export ANDROID_SD_VIDEOS=/storage/extSdCard/Videos/
export ANDROID_SD_MUSIC=/storage/extSdCard/Music/
export ANDROID_SD_SERMONS=/storage/extSdCard/Sermons/
export ANDROID_SD_DOC=/storage/extSdCard/Documentations/


## Debian Special
if [ `uname -s` == "Linux" ]; then
    export TOSHIBA_MOVIES=/media/$USERNAME/TOSHIBA/Movies/
    export TOSHIBA_SERIES=/media/$USERNAME/TOSHIBA/Series/
    export LOKING_SERIES=/media/$USERNAME/LOKING/Series/
    export LOKING_ANIMES=/media/$USERNAME/LOKING/Animes/
fi

## OSX SPECIAL
if [ `uname -s` == "Darwin" ]; then
    source osx
fi

fortune 2> /dev/null
