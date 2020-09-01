#!/bin/bash

usage() {
    echo "Usage   : $0 zerodowndeploy"
    echo "          $0 deploy"
}

zerodownredeploy () {

    if [ $(docker ps -f name=blue -q) ]
    then
        NEW="green"
        OLD="blue"
    else
        NEW="blue"
        OLD="green"
    fi

    docker-compose --project-name=$NEW up -d --build &
    docker-compose --project-name=$OLD kill
    docker-compose --project-name=$OLD rm -f
}

deploy () {
    docker-compose --project-name=blue up -d --build &
}

if [ $# -lt 1 ]
then
    usage
    exit
elif [[ $1 == "deploy" ]]
then
        deploy
elif [[ $1 == "zerodownredeploy" ]]
then
    zerodownredeploy
else
    usage
    exit
fi