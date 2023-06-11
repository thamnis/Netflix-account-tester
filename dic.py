from pathlib import Path
from pprint import pprint
import json

data_path = Path.cwd() / "data"
file_path = data_path / "x250 Netfix Accounts.txt"

with open(file_path, "r") as f:
    i = 0
    for _ in f:
        try:
            file = f.readlines(i)
        except:
            pass
    i += 1

accounts_list = [account.removesuffix("\n") for account in file if "\n" in account]
print(accounts_list)
accounts_dict = {}
for account in accounts_list:
    double = account.split(":")
    setter = {double[0]: double[1]}
    accounts_dict |= setter

with open("accounts_2.json", "w") as f:
    json.dump(accounts_dict, f, indent=4)
