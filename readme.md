### Scripts

Couples of scripts loaded when logging in.

* push_ssh_key
* rm_tmp_files
* archive
* mylogger


#### LOGS

All logs can be found in **$HOME_SCRIPTS/logs/**

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


