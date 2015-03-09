#!/bin/bash

#Script to backup or restore my workspace


function backup(){
	name=$1
	archive_name=$2
	path=$3
	
	if tar czvfh  $path/$archive_name --exclude='*.log' --exclude='*log/*' $name ; then
		echo -e "$name is archived as $path/$archive_name  "
		return 0
	else
		echo -e "Something went wrong"
		return 1
	fi
}

function restore(){
	archive_name=$1
	location=$2
	
	if  tar xzvf $archive_name -C $location ; then
		echo -e "$archive_name restored to $location"
		return 0
	else
		echo -e "Something went wrong"
		return 1
	fi
}

function archive(){

    LOG_OUTPUT=$HOME_SCRIPTS/logs/archives.log

    if [ $# -lt 1 ]; then
        echo -e "Help:  \n \t $0 --backup input [destination path] \n \t $0 --restore {archive} [destination path]"
        return 1
    fi

    export GZIP=-9
    export now=$(date +"%d-%m-%y_%H-%M")
    export archive_name="workspace-$now.tar.gz"
    export action=$1
    export path="./"

    case $action in
        "--backup" )
            if [ -z $2 ]; then
                echo -e "An input file is required"
                return 1
            fi

            input=$2 

            if [ ! -z $3 ]; then
                if [ ! -d $3 ]; then
                    echo -e "$3 is an invalid path"
                    return 1
                fi
                path=$3
            fi
            
            echo -e "Backing up workspace ..."
            backup $input $archive_name $path
            ;;
        "--restore" )
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
            restore $archive_name $path 
            ;;
    esac
}
