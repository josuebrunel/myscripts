## MyScripts

Bunch of scripts i use on a daily basis.
* shell ( some modules for my environement and my shell scripts )
* python ( most feature for the python shell )

## Installation

```shell
john@doe:$ cd
john@doe:$ git clone https://github.com/josuebrunel/myscripts.git .scripts/
john@doe:$ ln -s .scripts/profile .profile # .bashrc if you want
john@doe:$ source .profile
john@doe:$ reload # which loads the session with the new scripts
```
Or you can use the **bootstrap**

```shell
$ wget https://github.com/josuebrunel/myscripts/blob/master/bootstrap.sh
$ chmod +x bootstrap.sh
$ ./bootstrap.sh
```

***NB***

Don't hesitate to change the *reload* alias to meet your needs if necessary. If *.bashrc* is the script you want bash
to load you can do something like this :

```shell
alias reload='source .bashrc'
```

## Documentation

#### The Custom Shell Logger
This is the module used in other script to simulate a logger.
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

#### Push ssh key to remote host

This command copies a ssh public key to a remote host

```shell
john@doe:$ push_ssh_key huey@newtown
```

#### Ssh Connect To Remote host by name

In *$HOME\_SCRIPTS/cfg/ssh.txt* , assign a names to your remote hosts as follow:

```text
jenkins jenkins@192.168.1.3
debian  josue@192.168.1.2
raspberry pi@192.168.1.7
```
then to connect to _debian_ just run:

```shell
$ ssh_connect_to debian
```

#### Archiving

This function help you backup/restore a file 


```shell
john@doe:$ archive
Help:  
         archive --backup|-b input [destination path] 
         archive --restore|-r {archive} [destination path]
john@doe:$ archive -b myfoler/ 
john@doe:$ archive -r myfoler.tar.gz
```

#### Pypi Register/Publish
This function helps publishing a package on the Python Package Index

A ***$HOME/.pypirc*** is required. i.e

```cfg
[distutils] # this tells distutils what package indexes you can push to
index-servers =
    pypi
    pypitest

[pypi]
repository: https://pypi.python.org/pypi
username: josuebrunel

[pypitest]
repository: https://testpypi.python.org/pypi
username: josuebrunel

```

Run the commands below in your project folder

```shell
john@doe:$ pypi
Help:
        pypi --register|-r [server] #Register the package
        pypi --upload|-u [server] #Upload the package 
        pypi --all|-a [server] # Register then Upload the package
```

### OSX Fixers

* --ntfs/n : Fixes issues related to NTFS Corrupted disk. Equivalent to _check and repair_ on windows
* --brokM/b : Fixes issues related to file being _used by OSX_ while they're not. This happens for files on a NTFS Device

```shell
john@doe:$ fixers -h
Help
    --ntfs/-n /dev/diskname i.e disks3s1
    --brokM/b dirname
```



