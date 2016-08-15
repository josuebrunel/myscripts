#Colored Terminal
export CLICOLOR=1
export LSCOLORS=GxFxCxDxBxegedabagaced

export TERM="xterm-color"
PS1='\[\e[0;33m\]\u\[\e[0m\]%\[\e[0;32m\]\h\[\e[0m\]:\[\e[0;34m\]\w\[\e[0m\]\$'

# SUDO AUTOCOMPLETE
complete -cf sudo

#VARIABLES
export HOME_SCRIPTS=$HOME/.scripts

## COMMON LS
alias ll='ls -lht'
alias la='ls -lhAt'
alias lt='ls -lht'
alias ld='du -sh ./*/'
alias list-ca='awk -v cmd="openssl x509 -noout -subject" "/BEGIN/{close(cmd)};{print | cmd}" < /etc/ssl/certs/ca-certificates.crt'

## FILE COMPRESSION
alias ltar='tar tzvf'
alias ctar='tar czvf'
alias xtar='tar xzvf'

alias reload='source $HOME/.profile'
alias goto_workspace='cd $HOME/workspace'
alias goto_scripts='cd $HOME_SCRIPTS'
alias www-data_as_new_owner='sudo chown www-data:www-data'

alias json_pretty='python -m json.tool'

# JSON
alias json_pretty='python -m json.tool'

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

## LOADS SCRIPTS
source $HOME_SCRIPTS/shell/exit_f.sh
source $HOME_SCRIPTS/shell/ssh_push_key.sh
source $HOME_SCRIPTS/shell/archive.sh
source $HOME_SCRIPTS/shell/mylogger.sh
source $HOME_SCRIPTS/shell/setup_editors.sh
source $HOME_SCRIPTS/shell/ssh_connect_to.sh
source $HOME_SCRIPTS/shell/pypi.sh
source $HOME_SCRIPTS/shell/git-completion.bash
source $HOME_SCRIPTS/shell/date.sh

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

## ANDROID
alias android_push='adb push -p'
alias android_pull='adb pull'
export ANDROID_SD=/storage/extSdCard/
export ANDROID_SD_VIDEOS=/storage/extSdCard/Videos/
export ANDROID_SD_MUSIC=/storage/extSdCard/Music/
export ANDROID_SD_SERMONS=/storage/extSdCard/Sermons/
export ANDROID_SD_DOC=/storage/extSdCard/Documentations/

## YOUTUBE-DL
alias youtube-dl-audio='youtube-dl --extract-audio --audio-format mp3'
alias youtube-dl-video='youtube-dl -f 22'

## SOUNDCLOUD DL
alias soundcloud-dl='scdl -l'

## Debian Special
if [ `uname -s` == "Linux" ]; then
    export TOSHIBA_MOVIES=/media/$USERNAME/TOSHIBA/Movies/
    export TOSHIBA_SERIES=/media/$USERNAME/TOSHIBA/Series/
    export LOKING_SERIES=/media/$USERNAME/LOKING/Series/
    export LOKING_ANIMES=/media/$USERNAME/LOKING/Animes/
    alias update-system='sudo apt update; sudo apt upgrade; sudo apt autoremove; sudo apt dist-upgrade'
fi

# Thinkpad fix wifi
alias fix-wifi='nmcli device disconnect wlp3s0  ; nmcli device connect wlp3s0'

## OSX SPECIAL
if [ `uname -s` == "Darwin" ]; then
    #Fix terminal in Vi mode
    set -o emacs

    ## Vim location
    alias vim='/usr/bin/vim'

    #MY ALIASES
    alias umount_toshiba='sudo umount /VOLUMES/TOSHIBA/'
    alias goto_toshiba='cd /Volumes/TOSHIBA/'
    alias goto_macext='cd /Volumes/MacintoshEX/'
    alias disklist='diskutil list'

    alias update-system='port selfupdate; sudo port upgrade outdated'
    alias emax='/Applications/Emacs.app/Contents/MacOS/Emacs -nw'
    alias show_hidden_files='defaults write com.apple.finder AppleShowAllFiles YES; killall Finder /System/Library/CoreServices/Finder.app'
    alias hide_hidden_files='defaults write com.apple.finder AppleShowAllFiles NO; killall Finder /System/Library/CoreServices/Finder.app'

    #VIRTUAL ENVS
    source /usr/local/bin/virtualenvwrapper.sh

    #MYSQL CONFIG
    export PATH=$PATH:/usr/local/mysql/bin
    export DYLD_LIBRARY_PATH=/usr/local/mysql/lib

    #LOAD SCRIPTS
    source $HOME_SCRIPTS/shell/osx/myfixers.sh

    ##
    # Your previous /Users/josue/.profile file was backed up as /Users/josue/.profile.macports-saved_2014-11-08_at_12:21:31
    ##

    # MacPorts Installer addition on 2014-11-08_at_12:21:31: adding an appropriate PATH variable for use with MacPorts.
    export PATH="/opt/local/bin:/opt/local/sbin:$PATH"
    # Finished adapting your PATH environment variable for use with MacPorts.

    export PATH="$PATH:$HOME/.rvm/bin" # Add RVM to PATH for scripting

    [[ -s "$HOME/.rvm/scripts/rvm" ]] && source "$HOME/.rvm/scripts/rvm" # Load RVM into a shell session *as a function*
fi

fortune 2> /dev/null
