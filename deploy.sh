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

LOG_FILE="$PWD/deploy_logs/$(date +%F).log"

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
        -f|--force)
            FORCE="1"
            shift # past argument
        ;;
    esac
done

create_folder() {
    # Get the pare
    # If folder does not exist create that
    # $1 path to directory
    local DIR=$1
    if [ ! -d "$DIR" ]; then
        logit "CREATE" "FOLDER $DIR"
        mkdir -p $DIR
    fi
}

# Create folder to save logs
create_folder $(dirname $LOG_FILE)

logit() {
    # Save a log, basically a `echo` with format in a file $LOG_FILE
    # First save the date, type of log [INFO, WARN, ERR, ETC.], finallyy a message
    # $1 = Type of log
    # ${@:2} = message to save in log
    echo -e "[ $(date +'%F %X') ][ $1 ] ${@:2}" | tee -a "$LOG_FILE"
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
        podman pod create --name $1 -p 80:5000 -p 5555:5555 -p 5432:5432
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

stop_containers(){
    # Stop pod containers and prune all pods
    echo -e "\n" >> "$LOG_FILE"

    if [[ -n $FORCE ]]; then
        logit "CLEAN" "STOPING CONTAINERS"

        # Stopping pod's containers
        podman pod stop $POD_NAME 2> /dev/null

        return_code=$?
        case $return_code in
            0)
                login "STOP" "PODS CONTAINERS STOPPED";;
            125)
                logit "ERROR $return_code" "NO SUCH POD";;
        esac
    fi

    # Prune containers
    podman pod prune -f
    logit "CLEAN" "REMOVING CONTAINERS\n"
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


# Cleaning POD
stop_containers

# If pod doesn't exist create it
create_pod $POD_NAME

# If volumes don't exist it create them
create_vol $VOL_DB
create_vol $VOL_DB_BAK
create_vol $VOL_REDIS

# If images don't exist it create them
create_img $IMG_DB ./compose/production/postgres/Dockerfile
create_img $IMG_DJANGO ./compose/production/django/Dockerfile

# Creating Data Base
create_service $IMG_DB \
    -v ${POD_NAME}_${VOL_DB}:/var/lib/postgresql/data:Z \
    -v ${POD_NAME}_${VOL_DB_BAK}:/backups:z \
    --env-file ./.envs/.postgres \
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
        --env-file ./.envs/.postgres \
        --env-file ./.envs/.django.production \
        -e POSTGRES_HOST="${POD_NAME}_${IMG_DB}" \
        -e REDIS_URL=redis://"${POD_NAME}_${IMG_REDIS}":6379/0 \
        -e CELERY_BROKER_URL=redis://"${POD_NAME}_${IMG_REDIS}":6379/0 \
        ${POD_NAME}_${IMG_DJANGO}:${VERSION} \
        $2
}

up_django_service django /start
up_django_service celeryworker /start-celeryworker
up_django_service celerybeat /start-celerybeat
up_django_service flower /start-flower

logit "CLEAN" "REMOVING <NONE> IMAGES"
podman rmi $(podman images -f "dangling=true" -q) 2> /dev/null

s=$(printf "%-23s")
echo -e "\n\n${s// /=}\n\n" >> "$LOG_FILE"
