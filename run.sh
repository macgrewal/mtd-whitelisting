echo "> creating virtualenv"
sudo virtualenv -p python3 ./venv

echo "> activating virtualenv"
source venv/bin/activate

echo "> installing deps"
sudo -H pip install -r requirements.txt

echo "> whitelistings"
python3 whitelist.py

echo "> deactivating virtualenv"
deactivate