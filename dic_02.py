import json
from pathlib import Path

p = Path.cwd() / "data"
file_path = p / "100623.txt"
dico = p / "nf_combos_100623.json"

with open(file_path, "r") as f:
    read = f.read()

line = [line for line in read.split("\n")]
combo_list = [combo.split() for combo in line]
combo = [combo_list[i][0] for i in range(len(combo_list)-1)]

accounts_dict = {}
for account in combo:
    double = account.split(":")
    setter = {double[0]: double[1]}
    accounts_dict.update(setter)

with open(dico, "w") as f:
    json.dump(accounts_dict, f, indent=4)
