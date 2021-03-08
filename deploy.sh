#! /bin/bash

PWD=$(pwd)
POD_NAME=${PWD##*/}
VERSION=latest

VOL_DB=db_data
VOL_DB_BAK=db_backup

IMG_DB=postgres
IMG_REDIS=redis
IMG_DJANGO=django


while [[ $# -gt 0 ]]; do
    key="$1"

    case $key in
        -n|--name)
            POD_NAME="$2"
            shift # past argument
            shift # past value
        ;;
        -t|--tag|--version)
            VERSION="$2"
            shift # past argument
            shift # past value
        ;;
    esac
done

not_exist(){
    # Check if podman resourse exist (When format is `podman {resourse} ls`)
    # $1 = resource
    # $2 = resource_name (search)
    [ ! $(podman $1 ls | grep -Ec $2) -eq 1 ]
}

create_pod(){
    # Create the pod if it doesn't exist
    # Looking for the name with spaces before and after to make it unique
    # $1 = pod_name
    not_exist "pod" " $1 " && podman pod create --name $1 -p 80:5000 -p 5555:5555
}

create_vol(){
    # Create the volume if it doesn't exist ( prefix = $POD_NAME )
    # Looking for the name with space before and end of the line to make it unique
    # $1 = volume_name
    local NAME="${POD_NAME}_${1}"
    not_exist "volume" " ${NAME}\$" && podman volume create $NAME
}

create_img(){
    # Create the image if it doesn't exist ( prefix = $POD_NAME )
    # Looking for the name adding the version (tag) with undefined spaces to make it unique
    # $1 = image_name
    # $2 = path_to_dockerfile
    local NAME="${POD_NAME}_${1}"
    not_exist "image" "${NAME}\s+$VERSION" && podman build -t $NAME:$VERSION -f $2 .
}

not_running(){
    # Filter all running containers and see if it is running
    [ ! $(podman ps -af status=running | grep -Ec $1) -eq 1 ]
}

create_service(){
    # Run a conteiner if that isn't running, deatach mode and set to pod ( prefix = $POD_NAME )
    # Warning if container already exists in other status it will fail
    # $1 = container_name
    # $@ = other_params_to_run_container
    local NAME="${1}"
    not_running " ${NAME}\$" && podman run -d --pod $POD_NAME --name $NAME ${@:2}
}

# If pod doesn't exist create it
create_pod $POD_NAME

# If volumes don't exist it create them
create_vol $VOL_DB
create_vol $VOL_DB_BAK

# If volume don't exist it create them
create_img $IMG_DB ./compose/production/postgres/Dockerfile
create_img $IMG_DJANGO ./compose/production/django/Dockerfile

# Removing containers not running to be able to create new ones
podman rm $(eval podman ps -aq)

# Creating Data Base
create_service $IMG_DB \
    -v ${POD_NAME}_${VOL_DB}:/var/lib/postgresql/data:Z \
    -v ${POD_NAME}_${VOL_DB_BAK}:/backups:z \
    --env-file ./.envs/.production/.postgres \
    ${POD_NAME}_${IMG_DB}:${VERSION}

# Creating Redis container
create_service $IMG_REDIS \
    redis:6.0.9

up_django_service(){
    # Create the different django services as they are based on the same image
    # $1 = container_name
    # $2 = command
    create_service $1 \
        --env-file ./.envs/.production/.postgres \
        --env-file ./.envs/.production/.django \
        ${POD_NAME}_${IMG_DJANGO}:${VERSION} \
        $2
}

up_django_service django /start
up_django_service celeryworker /start-celeryworker
up_django_service celerybeat /start-celerybeat
up_django_service flower /start-flower

