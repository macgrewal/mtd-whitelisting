
echo "> creating virtualenv"
virtualenv -p python3 ./venv

if [ $? -eq 0 ];then
    echo "> activating virtualenv"
    source venv/bin/activate

    echo "> installing deps"
    pip3 install -r requirements.txt

    echo "> whitelistings"
    python3 whitelist.py

    echo "> deactivating virtualenv"
    deactivate

    echo "> deleting virtual environment"
    rm -rf venv
else
    echo "[ERROR] virtualenv failed - exiting"
    echo "> deleting virtual environment"
    rm -rf venv
fi