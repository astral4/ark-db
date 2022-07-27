import requests
from collections import defaultdict
import json

chars = (
    requests.get("https://raw.githubusercontent.com/Kengxxiao/ArknightsGameData/master/zh_CN/gamedata/excel/character_table.json")
            .json()
)

patch_chars = (
    requests.get("https://raw.githubusercontent.com/Kengxxiao/ArknightsGameData/master/zh_CN/gamedata/excel/char_patch_table.json")
            .json()
            ["patchChars"]
)

modules = (
    requests.get("https://raw.githubusercontent.com/Kengxxiao/ArknightsGameData/master/zh_CN/gamedata/excel/uniequip_table.json")
            .json()
)

name_changes = {
    "char_118_yuki": "Shirayuki",
    "char_196_sunbr": "Gummy",
    "char_115_headbr": "Zima",
    "char_195_glassb": "Istina",
    "char_197_poca": "Rosa",
    "char_1001_amiya2": "Amiya (Guard)"
}

chars.update(patch_chars)

char_data = defaultdict(dict)

def is_operator(char_info):
    return char_info["profession"] != "TOKEN" \
           and char_info["profession"] != "TRAP" \
           and not char_info["isNotObtainable"]

def format_cost(cost):
    return [{k: v for k, v in mat.items() if k != "type"} for mat in cost]

for char_id, char_info in chars.items():
    if is_operator(char_info):
        module_ids = modules["charEquip"].get(char_id, [])[1:]
        char_data[char_id] = {
            "charId": char_id,
            "name": name_changes.get(char_id, char_info["appellation"]),
            "elite": [format_cost(phase["evolveCost"]) for phase in char_info["phases"][1:]],
            "skill": [format_cost(level["lvlUpCost"]) for level in char_info["allSkillLvlup"]],
            "mastery": [[format_cost(mastery["levelUpCost"]) for mastery in skill["levelUpCostCond"]] for skill in char_info["skills"]],
            "module": [[format_cost(cost) for cost in modules["equipDict"][module_id]["itemCost"].values()] for module_id in module_ids],
        }

with open("./src/lib/data/operators.json", "w") as f:
    json.dump(char_data, f)