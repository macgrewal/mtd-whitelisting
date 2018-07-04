import sys
import os
import re
import json
import requests
import ruamel.yaml as yaml
from getopt import getopt, GetoptError
from requests.auth import HTTPBasicAuth
from bs4 import BeautifulSoup
from datetime import datetime
from package.cd import cd
from package.git import git
from package.config import config
from package.utils import xstr
from getpass import getpass

# environment variables
CONFLUENCE_HOST = None
WORKSPACE = None

# global variables
CONFLUENCE_USER = None
CONFLUENCE_PASS = None

# CLI options
TEST = False
DEBUG = False

# constants
ET = "external-test"
PROD = "production"
VAT = "vat-api"
SA = "self-assessment-api"
CONFIG_WHITELIST_PREFIX = "Prod.feature-switch.white-list.applicationIds."
ET_WHITELIST_URI = "/rest/api/content/106905709?expand=body.storage,version"
PROD_WHITELIST_URI = "/rest/api/content/106905712?expand=body.storage,version"


def validate_environment_variables():
    # type: () -> None
    """
    Checks that the following are set as environment variables :
        - confluence host name
        - workspace
    """
    if "CONFLUENCE_HOST" in os.environ:
        global CONFLUENCE_HOST
        CONFLUENCE_HOST = os.environ.get("CONFLUENCE_HOST")
    else:
        print("[ERROR] environment variable CONFLUENCE_HOST not set")
        sys.exit()
    
    if "WORKSPACE" in os.environ:
        global WORKSPACE
        WORKSPACE = os.environ.get("WORKSPACE")
    else:
        print("[ERROR] environment variable WORKSPACE not set")
        sys.exit()

    print("[STARTUP] env variables exist")


def http_get(url):
    # type: (str) -> str
    """
    performs a http get request to the confluence url provided
    with basic auth and returns the decoded body
    """
    print("> getting " + url)
    response = requests.get(url, auth=HTTPBasicAuth(CONFLUENCE_USER, CONFLUENCE_PASS))
    if response.status_code == 401:
        print("[ERROR] 401 from confluence API, are your creds correct?")
        sys.exit()
    elif response.status_code == 200:
        return response.content.decode()
    else:
        print("[ERROR] Unexpected response code from confluence API: " + response.status_code)
        sys.exit()


def get_whitelists_from_confluence(url):
    # type: (str) -> list[dict]
    """
    returns a list of dicts in the format
    {"info": info, "id": whitelistId, "project": project}
    """
    response = http_get(url)
    json_response = json.loads(response)
    html = json_response["body"]["storage"]["value"]

    soup = BeautifulSoup(html, "lxml")
    table = soup.find("table")

    whitelists = list()

    for row in table.findAll("tr"):
        cells = row.findAll("td", attrs={'data-highlight-colour': None})
        if len(cells) > 0:
            email = cells[0].find(text=True)
            vendor_name = cells[1].find(text=True)
            dev_name = cells[2].find(text=True)
            info = "%s %s %s" % (xstr(email), xstr(vendor_name), xstr(dev_name))
            whitelistId = cells[3].find(text=True)
            project = cells[4].find(text=True)
            whitelist = {"info": info, "id": whitelistId, "project": project}
            whitelists.append(whitelist)

            if DEBUG:
                print("[DEBUG] %s" % xstr(whitelist))

    return whitelists


def get_next_config_id(config):
    # type: (dict) -> str
    """
    Will iterate through the given `config` items
    to find the last id used and return the next id to use
    """
    currentIds = list()
    for key, value in config.items() :
        if re.search(CONFIG_WHITELIST_PREFIX, key) is not None:
            ids = int(re.split(CONFIG_WHITELIST_PREFIX, key)[1])
            currentIds.append(ids)

    return str(max(currentIds) + 1)


def write_to_app_config(fileName, whitelist):
    # type: (str, dict) -> None
    """
    Writes the id from the given `whitelist` dict
    to the given `fileName` yaml file
    """
    with open(fileName + ".yaml", "r") as read_yaml_file:
        appConfig = yaml.round_trip_load(read_yaml_file)
        hmrcConfig = appConfig['0.0.0']['hmrc_config']
        nextConfigId = get_next_config_id(dict(hmrcConfig))

    with open(fileName + ".yaml", "w") as write_yaml_file:
        hmrcConfig[CONFIG_WHITELIST_PREFIX + nextConfigId] = str(whitelist['id'])
        hmrcConfig.yaml_set_comment_before_after_key(key=(CONFIG_WHITELIST_PREFIX + nextConfigId),
                                                     before=whitelist["info"],
                                                     indent=4)
        yaml.round_trip_dump(appConfig, write_yaml_file)


def write_whitelists(whitelists):
    # type: (list[dict]) -> None
    """
    Writes the given `whitelists` to the correct project
    using the project key in the whitelist
    """
    count = 1
    for whitelist in whitelists:
        project = whitelist["project"]
        if project == "SA":
            print("> writing whitelist %d to %s" % (count, SA))
            count = count + 1
        elif project == "VAT":
            print("> writing whitelist %d to %s" % (count, VAT))
            write_to_app_config(VAT, whitelist)
            count = count + 1
        elif project == "SA/VAT" or project == "VAT/SA":
            print("> writing whitelist %d to %s" % (count, VAT))
            write_to_app_config(VAT, whitelist)
            print("> writing whitelist %d to %s" % (count, SA))
            write_to_app_config(SA, whitelist)
            count = count + 1
        else:
            print("[ERROR] invalid project fetched from confluence table")
            sys.exit()


def validate_confluence_creds():
    # type: () -> None
    """
    Checks local storage for confluence creds
    If absent, requests them from user and validates
    """
    conf = config()
    if conf.get("confluence_username") is None:
        print("> setting up confluence creds")
        valid = False
        while valid is False:
            username = input("enter confluence username: ")
            password = getpass('enter confluence password [hidden]: ')
            response = requests.get(CONFLUENCE_HOST, auth=HTTPBasicAuth(username, password))
            if response.status_code == 200:
                print("[STARTUP] valid confluence creds")
                valid = True
            elif response.status_code == 401:
                print("[ERROR] the username or password provided are wrong - retry")
            else:
                print("[ERROR] unexpected status code returned from confluence API - %d" % response.status_code)
                sys.exit()
        
        conf.insert("confluence_username", username)
        conf.insert("confluence_password", password)
    else:
        print("[STARTUP] confluence creds already in config")

    global CONFLUENCE_USER
    CONFLUENCE_USER = conf.get("confluence_username")
    global CONFLUENCE_PASS
    CONFLUENCE_PASS = conf.get("confluence_password")


def update_confluence_table(url, whitelists):
    # type: (str, list[dict]) -> None
    """
    Updates the confluence resource located at the given `url`
    by changing the colours of all the whitelisted ids to green
    """
    response = http_get(url)
    json_response = json.loads(response)
    html = json_response["body"]["storage"]["value"]

    soup = BeautifulSoup(html, "lxml")
    table = soup.find("table")

    for whitelist in whitelists:
        for row in table.findAll("tr"):
            for cell in row.findAll("td", attrs={'data-highlight-colour': None}):
                if cell.find(text=True) == whitelist["id"]:
                    for cell_to_update in row.findAll("td"):
                        cell_to_update['class'] = "highlight-green"
                        cell_to_update['data-highlight-colour'] = "green"
                        
    json_response["body"]["storage"]["value"] = str(soup.find("body").find("ac:layout"))

    current_version = json_response["version"]["number"]
    json_response["version"] = {'number': current_version + 1}
    
    body = json.dumps(json_response)

    if TEST:
        print("[TEST] updating confluence page")
    else:
        resp = requests.put(url, body,
                            headers={"content-type":"application/json"},
                            auth=HTTPBasicAuth(CONFLUENCE_USER, CONFLUENCE_PASS))

        if resp.status_code is 200:
            print("> updated confluence page to version %s" % (current_version + 1))
        else:
            print("[ERROR] unknown status code when trying to update confluence page: %d" % resp.status_code)


def whitelist(appConfigPath, whitelists):
    # type: (str, list[dict]) -> None
    """
    Orchestrates the whitelisting of the given `whitelists`
    to the given `appConfigPath`
    """
    if os.path.exists(appConfigPath):
        print("> navigating to " + appConfigPath)
        with cd(appConfigPath):
            print("> moving to master")
            git("checkout master --quiet")
            changes = git("diff --quiet HEAD")
            if changes == 1:
                print("> untracked changes detected")
                input("press ENTER to let me stash the changes, press Ctrl+C to exit")
                print("> stashing changes")
                git("stash --quiet")
            print("> pulling latest master")
            git("pull origin master --quiet")
            print("> checking out branch")
            dt = datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
            branch = "mtd-prod-whitelisting-%s" % dt
            git("checkout -b %s --quiet" % branch)
            write_whitelists(whitelists)
            date = datetime.now().strftime('%Y-%m-%d')
            commit_message = "mtd-whitelisting-%s" % date

            if TEST:
                print("[TEST] committing, pushing and pull request")
            else:
                print("> committing and pushing")
                git('commit -am "%s" --quiet' % commit_message)
                git("push origin %s --quiet" % branch)
                print("> raising pull request")
                print("----------")
                git.hub('pull-request -m %s' % commit_message)
                print("----------")
    else:
        print("[ERROR] missing directory: " + appConfigPath)


def validate_command_line_arguments():
    # type: () -> None
    """
    Will inspect and validate the following command line options:
        (-t, --test) - enables test mode so calls to external services are stubbed
        (-d, --debug) - enables debug mode to print out key information for debugging
    """
    try:
        opts, args = getopt(sys.argv[1:], "td", ["test", "debug"])

        for opt, arg in opts:
            if opt in ('-t', "--test"):
                print("[STARTUP] enabling test mode")
                global TEST
                TEST = True
            if opt in ('-d', "--debug"):
                print("[STARTUP] enabling debug mode")
                global DEBUG
                DEBUG = True

    except GetoptError:
        print("[ERROR] unknown arguments supplied")
        sys.exit()


def main():
    validate_environment_variables()
    validate_confluence_creds()
    validate_command_line_arguments()

    print("> checking production")

    prod_whitelist_url = CONFLUENCE_HOST + PROD_WHITELIST_URI
    prod_whitelists = get_whitelists_from_confluence(prod_whitelist_url)

    if len(prod_whitelists) > 0:
        print("> ids to whitelist for production: %d" % len(prod_whitelists))
        prod_path = WORKSPACE + "/app-config-production"
        whitelist(prod_path, prod_whitelists)
        update_confluence_table(prod_whitelist_url, prod_whitelists)
    else:
        print("> no whitelisting required for production")

    print("> checking ET")

    et_whitelist_url = CONFLUENCE_HOST + ET_WHITELIST_URI
    et_whitelists = get_whitelists_from_confluence(et_whitelist_url)
    if len(et_whitelists) > 0:
        print("> ids to whitelist for external test: %d" % len(et_whitelists))
        et_path = WORKSPACE + "/app-config-externaltest"
        whitelist(et_path, et_whitelists)
        update_confluence_table(et_whitelist_url, et_whitelists)
    else:
        print("> no whitelisting required for ET")

    print("> finished whitelisting")


if __name__ == '__main__':
    main()
