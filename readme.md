# MyScripts


## Installation

```shell
john@doe:$ sudo apt install ansible
john@doe:$ git clone https://github.com/josuebrunel/myscripts.git .scripts/
john@doe:$ cd .scripts/ 
john@doe:$ ansible-playbook -vv ansible/home_playbook.yml

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

### Date
Just a couple of date shorcuts

* ___get_date [format]___
```shell
$ get_date
2015-08-12
$ get_data %D
08/12/15
```
* ___get_time [format]___
```shell
$ get_time
14:03:10
```
* ___get_datetime [format]___
```
$ get_datetime
2015-08-12 14:04:14
```
* ___date_add___
```shell
$ date_add '10 years'
Tue Aug 12 14:04:52 CEST 2025
```
* ___date_minus___
```shell
$ date_minus '3 weeks'
Wed Jul 22 14:05:48 CEST 2015
```

```shell
USAGE:
        function '<number> <[minutes,hours,days,weeks,months,years]>'
Examples:
        date_add '10 weeks'
        date_minus '10 days'
```
