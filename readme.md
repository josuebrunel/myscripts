## MyScripts

Bunch of scripts i use on a daily basis.
* shell ( some modules for my environement and my shell scripts )
* python ( most feature for the python shell )

## Installation

```shell
john@doe:$ cd
john@doe:$ git clone git@github.com:josuebrunel/myscripts.git
john@doe:$ mv myscripts .scripts
john@doe:$ ln -s .scripts/.profile .profile # .bashrc if you want
john@doe:$ source .profile
john@doe:$ reload # which loads the session with the new scripts
```

***NB***

Don't hesitate to change the *reload* alias to meet your needs if necessary. If *.bashrc* is the script you want bash
to loads when it is launched interactively you can do something like this :

```shell
alias reload='source .bashrc'
```

## Documentation

#### The Custom Logger
This is the module used in other script to simulate a logger
If the variable ***LOG_OUTPUT*** is not defined, logs are 
redirected to *STDOUT*.

* **_info**
```shell
john@doe:$ _info "This is an info message"
Feb 26 17:28:44 LokingMac.local josue[811] <Info>: hello josh
```

* **_notice**
```shell
john@doe:$ _notice "This is an notice message"
Feb 26 17:28:44 LokingMac.local josue[811] <Notice>: hello josh
```

* **_debug**
```shell
john@doe:$ _debug "This is a debug message"
Feb 26 17:28:44 LokingMac.local josue[811] <Debug>: hello josh
```

* **_warning**
```shell
john@doe:$ _warning "This is a warning message"
Feb 26 17:28:44 LokingMac.local josue[811] <Warning>: hello josh
```

* **_error**
```shell
john@doe:$ _error "This is an error message"
Feb 26 17:28:44 LokingMac.local josue[811] <Error>: hello josh
```

#### push_ssh_key

This command copy a ssh public key to a remote host

```shell
john@doe:$ push_ssh_key huey@newtown
```


