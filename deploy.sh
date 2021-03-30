#! /bin/bash

PWD=$(pwd)
POD_NAME=${PWD##*/}
VERSION=latest

VOL_DB=db_data
VOL_DB_BAK=db_backup
VOL_REDIS=redis_data

IMG_DB=postgres
IMG_REDIS=redis
IMG_DJANGO=django

LOG_FILE="$PWD/deploy_$(date +%F).log"

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
        -l|--log)
            LOG_FILE="$2"
            shift # past argument
            shift # past value
        ;;
        -b|--build)
            BUILD="1"
            shift # past argument
        ;;
    esac
done

logit() {
    # Save a log, basically a `echo` with format in a file $LOG_FILE
    # First save the date, type of log [INFO, WARN, ERR, ETC.], finallyy a message
    # $1 = Type of log
    # ${@:2} = message to save in log
    echo -e "[ $(date +'%F %X') ][ $1 ] ${@:2}" >> "$LOG_FILE"
}

not_exist(){
    # Check if podman resourse exist (When format is `podman {resourse} ls`)
    # $1 = resource
    # $2 = resource_name (search)
    logit "CHECK" "RESOURCE: $1 = $2"
    [ ! $(podman $1 ls | grep -Ec $2) -eq 1 ]
}

create_pod(){
    # Create the pod if it doesn't exist
    # Looking for the name with spaces before and after to make it unique
    # $1 = pod_name
    if not_exist "pod" " $1 "; then
        logit "CREATE" "POD: $1\n"
        # echo "podman pod create --name $1 -p 80:5000 -p 5555:5555"
        podman pod create --name $1 -p 80:5000 -p 5555:5555
    else
        logit "EXIST" "POD: $1\n"
    fi
}

create_vol(){
    # Create the volume if it doesn't exist ( prefix = $POD_NAME )
    # Looking for the name with space before and end of the line to make it unique
    # $1 = volume_name
    local NAME="${POD_NAME}_${1}"
    if not_exist "volume" " ${NAME}\$"; then
        logit "CREATE" "VOLUME: $NAME\n"
        # echo "podman volume create $NAME"
        podman volume create $NAME
    else
        logit "EXIST" "VOLUME: $NAME\n"
    fi
}

create_img(){
    # Create the image if it doesn't exist ( prefix = $POD_NAME )
    # Looking for the name adding the version (tag) with undefined spaces to make it unique
    # $1 = image_name
    # $2 = path_to_dockerfile
    local NAME="${POD_NAME}_${1}"
    if [[ $(not_exist "image" "${NAME}\s+$VERSION") || -n $BUILD ]]; then
        logit "CREATE" "IMAGE $NAME from $2\n"
        # echo "podman build -t $NAME:$VERSION -f $2 ."
        podman build -t $NAME:$VERSION -f $2 .
    else
        logit "EXIST" "IMAGE: $NAME\n"
    fi
}

not_running(){
    # Filter all running containers and see if it is running
    # Looking for the container name
    # $1 = container_name
    logit "CHECK" "CONTAINER RUNNING: $1"
    [ ! $(podman ps -af status=running | grep -Ec $1) -eq 1 ]
}

create_service(){
    # Run a conteiner if that isn't running, deatach mode and set to pod ( prefix = $POD_NAME )
    # Warning if container already exists in other status it will fail
    # $1 = container_name
    # $@ = other_params_to_run_container
    local NAME="${POD_NAME}_${1}"
    if not_running " ${NAME}\$"; then
        logit "RUN" "CONTAINER: $NAME"
        logit "INFO" "EXTRA PARAMS: ${@:2}\n"
        # echo "podman run -d --pod $POD_NAME --name $NAME ${@:2}"
        podman run -d --pod $POD_NAME --name $NAME --restart always ${@:2}
    else
        logit "EXIST" " CONTAINER: $NAME\n"
    fi
}

# If pod doesn't exist create it
create_pod $POD_NAME

# If volumes don't exist it create them
create_vol $VOL_DB
create_vol $VOL_DB_BAK
create_vol $VOL_REDIS

# If images don't exist it create them
create_img $IMG_DB ./compose/production/postgres/Dockerfile
create_img $IMG_DJANGO ./compose/production/django/Dockerfile

# Removing containers not running to be able to create new ones
echo -e "\n" >> LOG_FILE
logit "CLEAN" "CONTAINERS STOPED"
podman rm $(eval podman ps -aq) 2> /dev/null
return_code=$?
[ $return_code -ge $return_code ] && \
    logit "ERROR $return_code" "THE CONTAINERS COULD NOT BE ERASE\n"

# Creating Data Base
create_service $IMG_DB \
    -v ${POD_NAME}_${VOL_DB}:/var/lib/postgresql/data:Z \
    -v ${POD_NAME}_${VOL_DB_BAK}:/backups:z \
    --env-file ./.envs/.production/.postgres \
    -e POSTGRES_HOST="${POD_NAME}_${IMG_DB}" \
    ${POD_NAME}_${IMG_DB}:${VERSION}

# Creating Redis container
create_service $IMG_REDIS \
    -v ${POD_NAME}_${VOL_REDIS}:/data \
    redis:6.0.9

up_django_service(){
    # Create the different django services as they are based on the same image
    # $1 = container_name
    # $2 = command
    create_service $1 \
        --env-file ./.envs/.production/.postgres \
        --env-file ./.envs/.production/.django \
        -e POSTGRES_HOST="${POD_NAME}_${IMG_DB}" \
        -e REDIS_URL=redis://"${POD_NAME}_${IMG_REDIS}":6379/0 \
        -e CELERY_BROKER_URL=redis://"${POD_NAME}_${IMG_REDIS}":6379/0
        ${POD_NAME}_${IMG_DJANGO}:${VERSION} \
        $2
}

up_django_service django /start
up_django_service celeryworker /start-celeryworker
up_django_service celerybeat /start-celerybeat
up_django_service flower /start-flower

s=$(printf "%-23s")
echo -e "\n\n${s// /=}\n\n" >> "$LOG_FILE"
