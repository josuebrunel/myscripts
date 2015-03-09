#!/bin/bash

#Script to __backup__ or __restore__ my workspace


function __backup__(){
	name=$1
	archive_name=$2
    if [ ! -z $3 ]; then
    	path="$3/${archive_name}"
    else
        path="${archive_name}"
    fi
	
	if tar czvfh  $path --exclude='*.log' --exclude='*log/*' $name ; then
		_info -e "$name is archived as $path"
		return 0
	else
		_error -e "Something went wrong"
		return 1
	fi
}

function __restore__(){
	archive_name=$1
	location=$2
	
	if  tar xzvf $archive_name -C $location ; then
		_info "$archive_name restored to $location"
		return 0
	else
		_error -e "Something went wrong"
		return 1
	fi
}

function archive(){

    LOG_OUTPUT=$HOME_SCRIPTS/logs/archives.log

    if [ $# -lt 1 ]; then
        echo -e "Help:  \n \t archive --backup|-b input [destination path] \n \t archive --restore|-r {archive} [destination path]"
        return 1
    fi

    GZIP=-9
    now=$(date +"%d-%m-%y_%H-%M")
    action=$1
    path=""

    case $action in
        "--backup" | "-b" )
            if [ -z $2 ]; then
                echo -e "An input file is required"
                return 1
            fi

            input=$2 
            archive_name="${input}-${now}.tar.gz"

            if [ ! -z $3 ]; then
                if [ ! -d $3 ]; then
                    echo -e "$3 is an invalid path"
                    return 1
                fi
                path=$3
            fi
            
            echo -e "Backing up ${input} ..."
            __backup__ $input $archive_name $path
            ;;
        "--restore" | "-r" )
            if [ -z $2 ]; then
                echo -e "An archive file must be provided"
                return 1
            else 
                archive_name=$2

                if [ ! -f $archive_name ]; then
                    echo -e "Can't find $archive_name"
                    return 1
                fi
            fi

            if [ ! -z $3 ]; then
                path=$3
            fi

            echo -e "Restoring workspace ..."
            __restore__ $archive_name $path 
            ;;
        *)
            echo -e "Action not recognized. Only --backup or --restore are allowed"
    esac
}
