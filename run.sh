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

    echo "> installing deps"
    pip3 install -r requirements.txt

    echo "> starting whitelisting"
    python3 whitelist.py ${OPTIONS[@]}

    echo "> deactivating virtualenv"
    deactivate

    echo "> deleting virtual environment"
    rm -rf venv
else
    echo "[ERROR] virtualenv failed - exiting"
    echo "> deleting virtual environment"
    rm -rf venv
fi