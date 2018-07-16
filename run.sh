#!/usr/bin/env bash

OPTIONS=()

for key in "$@"; do
    case ${key} in
        -t|--test)
        echo "> TEST mode enabled"
        OPTIONS+=("--test")
        shift # past argument
        shift # past value
        ;;
        -d|--debug)
        echo "> DEBUG mode enabled"
        OPTIONS+=("--debug")
        shift # past argument
        shift # past value
        ;;
        *)
        shift # past argument
        shift # past value
        ;;
    esac
done

echo "> creating virtualenv"
virtualenv -p python3 ./venv

if [ $? -eq 0 ];then
    echo "> activating virtualenv"
    source venv/bin/activate

    echo "> installing dependencies"
    pip3 install --upgrade --quiet -r requirements.txt

    echo "> starting Whitelisting"
    python3 main.py ${OPTIONS[@]}

    echo "[SHUTDOWN] deactivating virtualenv"
    deactivate
else
    echo "[ERROR] virtualenv failed - exiting"
fi