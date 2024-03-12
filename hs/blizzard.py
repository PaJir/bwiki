import os
import json
import requests
import re
import random
import time

MINION_URL = 'https://api.blizzard.com/hearthstone/cards?gameMode=battlegrounds&pageSize=3000&locale=zh_CN'
'https://api.blizzard.com/hearthstone/cards?bgCardType=minion&gameMode=battlegrounds&pageSize=3000&locale=zh_CN' # 随从 手下
MINION_FILE = "./minions.json"
MINION_PATH = "minions"
OUTPUT_FILE = "./blizzard.txt"
headers = {
  'Accept': '*/*', 
  'Accept-Language': 'zh,en;q=0.9,zh-CN;q=0.8,ja;q=0.7,zh-TW;q=0.6,en-US;q=0.5', 
  'Authorization': 'Bearer KRWpkSRImus70XdDJxtFmU78r8l2hXSIpR', 
  'Cache-Control': 'no-cache', 
  'Connection': 'keep-alive', 
  'Content-Type': 'application/json', 
  'DNT': '1', 
  'Origin': 'https://hearthstone.blizzard.com', 
  'Pragma': 'no-cache', 
  'Referer': 'https://hearthstone.blizzard.com/zh-tw/battlegrounds', 
  'Sec-Fetch-Dest': 'empty', 
  'Sec-Fetch-Mode': 'cors', 
  'Sec-Fetch-Site': 'same-site', 
  'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 16_6 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.6 Mobile/15E148 Safari/604.1'
}
def read_json_file(filename, url):
    if os.path.exists(filename):
        with open(filename, "r", encoding="utf-8") as rf:
            lines = rf.readlines()
        lines = "".join(lines)
        return json.loads(lines)
    else:
        req = requests.get(url, headers=headers).text
        with open(filename, "w+", encoding="utf=8") as wf:
            wf.write(req)
        return json.loads(req)

def get_img(img_path, filename, url):
    filename = os.path.join(img_path, filename)
    if os.path.exists(filename) or url == "":
        return
    try:
        myfile = requests.get(url)
    except:
        print("error get file: %s" % filename)
        return
    if myfile.status_code != 200:
        return
    open(filename, "wb").write(myfile.content)
    myfile.close()
    t = 0.2 + random.random()
    time.sleep(t)

wf = open(OUTPUT_FILE, "w+", encoding="utf-8")

minion_type_map = {
    0: "",
    11: "亡灵",
    14: "鱼人",
    15: "恶魔",
    17: "机械",
    18: "元素",
    20: "野兽",
    23: "海盗",
    24: "龙",
    26: "全部",
    43: "野猪人",
    92: "纳迦"
}
def minions_dump():
    cards = read_json_file(MINION_FILE, MINION_URL)
    cards = list(filter(lambda x : x["cardTypeId"] == 4, cards["cards"]))
    cards.sort(key=lambda x : x["id"])
    for card in cards:
        info = []
        get_img(MINION_PATH, str(card["id"])+".png", card["image"])
        # 名称 dbfid 等级 攻 血 类型 跟随随从池 描述
        info.append(card["id"])
        info.append(card["name"])
        info.append(card["id"])
        print(card["name"])
        info.append(card["battlegrounds"]["tier"])
        info.append(card["attack"])
        info.append(card["health"])
        card["minionTypeId"] = card.get("minionTypeId", 0)
        info.append(minion_type_map.get(card["minionTypeId"], card.get("minionTypeId")))
        info.append(minion_type_map.get(card["minionTypeId"], ""))
        info.append(card["text"])
        pattern = re.compile(r'<b>([^</b>]*)</b>')
        results = pattern.findall(card["text"])
        if results:
            keys = set() 
            for r in results:
                r = r.replace("：", "").split("，")
                for key in r:
                    keys.add(key)
            info.append(",".join(keys))
        else:
            info.append("")
        childIds = card.get("childIds", [])
        upgradeId = card["battlegrounds"]["upgradeId"]
        if upgradeId not in childIds:
            childIds.append(upgradeId)
        if len(childIds) > 0:
            child_cards = requests.get(MINION_URL+"&ids="+",".join([str(c) for c in childIds]), headers=headers).text
            child_cards = json.loads(child_cards)["cards"]
            childs = {}
            for child in child_cards:
                get_img(MINION_PATH, str(child["id"])+".png", child["imageGold"] if child["imageGold"] != "" else child["image"])
                childs[child["id"]] = child
            # 金色版dbfid 金色版本描述
            get_img(MINION_PATH, str(upgradeId)+".png", card["battlegrounds"]["imageGold"])
            info.append(upgradeId)
            info.append(childs.get(upgradeId,{}).get("text", ""))
            childIds.remove(upgradeId)
            # 衍生
            info.append(",".join([str(c) for c in childIds]))
        wf.write("\t".join([str(c) for c in info]) + "\n")

def heroes_dump():
    cards = read_json_file(MINION_FILE, MINION_URL)
    cards = list(filter(lambda x : x["cardTypeId"] == 3, cards["cards"]))
    cards.sort(key=lambda x : x["id"])
    for card in cards:
        info = []
        # 名称 dbfid 护甲
        info.append(card["id"])
        info.append(card["name"])
        info.append(card["id"])
        print(card["name"])
        info.append(card["armor"])

        # 技能dbfid 技能名称 技能消耗 技能描述
        skillId = card["childIds"][0]
        skill = requests.get(MINION_URL+"&id="+skillId)
        info.append(skill["id"])
        info.append(skill["name"])
        info.append(skill["text"])

        # 伙伴dbfid 伙伴名称 伙伴等级 伙伴描述
        companionId = card["battlegrounds"]["companionId"]
        companion = requests.get(MINION_URL+"&id="+str(companionId))
        companion = json.loads(companion)["cards"][0]
        info.append(companion["id"])
        info.append(companion["name"])

if __name__ == "__main__":
    # minions_dump()
    heroes_dump()